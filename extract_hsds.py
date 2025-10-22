#!/usr/bin/env python3
"""
HSDS Extraction with DeepSeek OCR + gpt-oss-20b
Two-stage extraction pipeline:
1. DeepSeek OCR extracts text from community services flyer image
2. gpt-oss-20b (via Ollama) extracts HSDS structured data from the text
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import torch

# Import BAML client
from baml_client.baml_client.sync_client import b
from baml_client.baml_client.types import HSDSData

# Load environment variables from .env file if it exists
load_dotenv()

from unittest.mock import patch
from transformers.dynamic_module_utils import get_imports

# Work around for flash_attn dependency on non-GPU environments
def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    imports = get_imports(filename)
    if not torch.cuda.is_available() and "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports


def extract_text_with_deepseek_ocr(image_path: str) -> str:
    """
    Use DeepSeek OCR to extract text from an image.

    Args:
        image_path: Path to the image file

    Returns:
        Extracted text/markdown from the image
    """
    import torch
    from transformers import AutoModel, AutoTokenizer
    
    print(f"\n{'='*80}")
    print("STAGE 1: DeepSeek OCR - Text Extraction")
    print(f"{'='*80}")
    print(f"Loading image from: {image_path}")
    
    # Load DeepSeek OCR model
    model_name = 'deepseek-ai/DeepSeek-OCR'
    print(f"\nLoading DeepSeek OCR model: {model_name}")
    print("This may take a moment on first run as the model is downloaded...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    with patch("transformers.dynamic_module_utils.get_imports", fixed_get_imports):
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            use_safetensors=True
        )
    
    # Move to appropriate device
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    if device == "cuda":
        model = model.eval().cuda().to(torch.bfloat16)
    elif device == "mps":
        model = model.eval().to(device)
    else:
        model = model.eval()
    
    # Prepare prompt for OCR
    # Using the document conversion prompt from DeepSeek OCR documentation
    prompt = "<image>\n<|grounding|>Convert the document to markdown."
    
    print(f"\nExtracting text from image...")
    print(f"Prompt: {prompt}")
    
    # Create temporary output directory
    temp_output = Path("./temp_ocr_output")
    temp_output.mkdir(parents=True, exist_ok=True)
    
    # Run OCR inference
    # Using Gundam mode (base_size=1024, image_size=640, crop_mode=True) for best quality
    ocr_result = model.infer(
        tokenizer,
        prompt=prompt,
        image_file=str(image_path),
        output_path=str(temp_output),
        base_size=1024,
        image_size=640,
        crop_mode=True,
        save_results=False,
        test_compress=True
    )
    
    print(f"\n{'='*80}")
    print("OCR Extraction Complete")
    print(f"{'='*80}")
    print(f"\nExtracted text length: {len(ocr_result)} characters")
    print(f"\nFirst 500 characters of extracted text:")
    print("-" * 80)
    print(ocr_result[:500])
    print("-" * 80)
    
    return ocr_result


def extract_hsds_data_from_text(ocr_text: str) -> HSDSData:
    """
    Extract HSDS-compliant data from OCR'd text using gpt-oss-20b via Ollama.
    
    Args:
        ocr_text: Text extracted from the flyer image
        
    Returns:
        Structured HSDS data
    """
    print(f"\n{'='*80}")
    print("STAGE 2: gpt-oss-20b - HSDS Extraction")
    print(f"{'='*80}")
    print("\nExtracting structured HSDS data from OCR text...")
    print("Using gpt-oss-20b via Ollama...")
    print("This may take a moment as the AI analyzes the text...\n")
    
    # Call the BAML function to extract structured data from text
    hsds_data = b.ExtractHSDSFromText(ocr_text=ocr_text)
    
    return hsds_data


def hsds_to_dict(hsds_data: HSDSData) -> dict:
    """
    Convert HSDS Pydantic model to a dictionary for JSON serialization.
    
    Args:
        hsds_data: HSDS data object
        
    Returns:
        Dictionary representation
    """
    # Pydantic v2 uses model_dump()
    return hsds_data.model_dump()


def print_summary(hsds_data: HSDSData):
    """
    Print a human-readable summary of the extracted HSDS data.
    """
    print("=" * 80)
    print("HSDS DATA EXTRACTION SUMMARY")
    print("=" * 80)
    
    print(f"\nORGANIZATION")
    print(f"   Name: {hsds_data.organization.name}")
    print(f"   Description: {hsds_data.organization.description}")
    if hsds_data.organization.url:
        print(f"   Website: {hsds_data.organization.url}")
    
    print(f"\nSERVICES & LOCATIONS ({len(hsds_data.services_at_locations)} found)")
    
    for idx, sal in enumerate(hsds_data.services_at_locations, 1):
        print(f"\n   [{idx}] SERVICE: {sal.service.name}")
        print(f"       Description: {sal.service.description}")
        print(f"       Status: {sal.service.status}")
        
        if sal.service.eligibility:
            print(f"       Eligibility: {sal.service.eligibility}")
        
        if sal.service.fees:
            print(f"       Fees: {sal.service.fees}")
        
        if sal.service.schedules:
            print(f"       Schedules:")
            for schedule in sal.service.schedules:
                print(f"         - {schedule.description or 'Schedule'}")
                print(f"           Frequency: {schedule.freq}")
                if schedule.byday:
                    print(f"           Days: {schedule.byday}")
                print(f"           Hours: {schedule.opens_at} - {schedule.closes_at}")
        
        if sal.service.phones:
            print(f"       Phone Numbers:")
            for phone in sal.service.phones:
                print(f"         - {phone.number} ({phone.phone_type})")
        
        print(f"\n       LOCATION: {sal.location.name}")
        if sal.location.description:
            print(f"          Description: {sal.location.description}")
        
        if sal.location.addresses:
            for addr in sal.location.addresses:
                print(f"          Address: {addr.address_1}")
                print(f"                   {addr.city}, {addr.state_province} {addr.postal_code}")
                print(f"                   Type: {addr.address_type}")
    
    print("\n" + "=" * 80)


def save_to_json(hsds_data: HSDSData, output_path: str):
    """
    Save the extracted HSDS data to a JSON file.
    """
    data_dict = hsds_to_dict(hsds_data)
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\nHSDS data saved to: {output_path}")


def save_ocr_text(ocr_text: str, output_path: str):
    """
    Save the OCR extracted text to a file for reference.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    
    print(f"OCR text saved to: {output_path}")


def main():
    """Main execution function."""
    
    # Default to the uploaded image
    default_image = "./images/20251020_100526.jpg"
    
    # Allow command-line override
    image_path = sys.argv[1] if len(sys.argv) > 1 else default_image
    
    try:
        # Check if Ollama is running
        print("\nChecking Ollama connection...")
        print("Make sure Ollama is running with: ollama run gpt-oss:20b")
        print("If not started, open a terminal and run:")
        print("  ollama run gpt-oss:20b")
        input("\nPress Enter when Ollama is ready (or Ctrl+C to cancel)...")
        
        # Stage 1: Extract text using DeepSeek OCR
        ocr_text = extract_text_with_deepseek_ocr(image_path)
        
        # Save OCR text for reference
        ocr_output_file = "./hsds_outputs/ocr_extracted_text.txt"
        save_ocr_text(ocr_text, ocr_output_file)
        
        # Stage 2: Extract HSDS data from text using gpt-oss-20b
        hsds_data = extract_hsds_data_from_text(ocr_text)
        
        # Print summary
        print_summary(hsds_data)
        
        # Save to JSON file
        output_file = "./hsds_outputs/extracted_hsds_data_ollama.json"
        save_to_json(hsds_data, output_file)
        
        print(f"\n{'='*80}")
        print("TWO-STAGE EXTRACTION COMPLETE")
        print(f"{'='*80}")
        print("\nPipeline Summary:")
        print("  1. ✓ DeepSeek OCR extracted text from image")
        print("  2. ✓ gpt-oss-20b extracted HSDS structured data")
        print(f"\nOutputs:")
        print(f"  - OCR Text: {ocr_output_file}")
        print(f"  - HSDS JSON: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()