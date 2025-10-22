#!/usr/bin/env python3
"""
HSDS Extraction Demo
Extracts Human Services Data Specification (HSDS) compliant data from a community services flyer image.
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Import BAML client
from baml_client.baml_client.sync_client import b
from baml_client.baml_client.types import HSDSData
from baml_py import Image

# Load environment variables from .env file if it exists
load_dotenv()


def load_image_from_file(image_path: str) -> Image:
    """
    Load an image from a local file path and convert to base64.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        BAML Image object with base64-encoded data
    """
    import base64
    import mimetypes
    
    image_path = Path(image_path).resolve()
    
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    print(f"Loading image from: {image_path}")
    
    # Detect MIME type from file extension
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith('image/'):
        # Default to common image types
        ext = image_path.suffix.lower()
        mime_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_map.get(ext, 'image/jpeg')
    
    # Read and encode image as base64
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
    
    print(f"Encoded image as base64 ({len(base64_data)} chars, MIME: {mime_type})")
    
    # Create Image from base64 data
    img = Image.from_base64(mime_type, base64_data)
    
    return img


def extract_hsds_data(image_path: str) -> HSDSData:
    """
    Extract HSDS-compliant data from a community services flyer image.
    
    Args:
        image_path: Path to the flyer image
        
    Returns:
        Structured HSDS data
    """
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it in a .env file or export it in your shell."
        )
    
    # Load the image
    img = load_image_from_file(image_path)
    
    print("\nExtracting HSDS data from flyer...")
    print("This may take a moment as the AI analyzes the image...\n")
    
    # Call the BAML function to extract structured data
    hsds_data = b.ExtractHSDSFromImage(flyer_image=img)
    
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


def main():
    """Main execution function."""
    
    # Default to the uploaded image
    default_image = "./images/20251020_100526.jpg"
    
    # Allow command-line override
    image_path = sys.argv[1] if len(sys.argv) > 1 else default_image
    
    try:
        # Extract HSDS data from the image
        hsds_data = extract_hsds_data(image_path)
        
        # Print summary
        print_summary(hsds_data)
        
        # Save to JSON file
        output_file = "./hsds_outputs/extracted_hsds_data.json"
        save_to_json(hsds_data, output_file)
        
        print("\nExtraction complete.")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()