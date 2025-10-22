#!/usr/bin/env python3
"""
Standalone DeepSeek OCR Test Script
Simple script to test DeepSeek OCR in isolation with different settings
"""

import os
import sys
import time
import torch
from pathlib import Path
from unittest.mock import patch
from transformers.dynamic_module_utils import get_imports

# Work around for flash_attn dependency on non-GPU environments
def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    imports = get_imports(filename)
    if not torch.cuda.is_available() and "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports


def test_deepseek_ocr(image_path: str, mode: str = "tiny"):
    """
    Test DeepSeek OCR with different speed/quality modes.
    
    Args:
        image_path: Path to the image file
        mode: One of "tiny", "small", "base", "gundam"
              - tiny: Fastest, lowest quality (base_size=512, no crop)
              - small: Fast, good quality (base_size=640, no crop)
              - base: Slower, better quality (base_size=1024, no crop)
              - gundam: Slowest, best quality (base_size=1024, crop_mode=True)
    
    Returns:
        Extracted text
    """
    from transformers import AutoModel, AutoTokenizer
    
    print("\n" + "="*80)
    print("DEEPSEEK OCR TEST")
    print("="*80)
    
    # Mode configurations
    modes = {
        "tiny": {"base_size": 512, "image_size": 512, "crop_mode": False},
        "small": {"base_size": 640, "image_size": 640, "crop_mode": False},
        "base": {"base_size": 1024, "image_size": 1024, "crop_mode": False},
        "gundam": {"base_size": 1024, "image_size": 640, "crop_mode": True}
    }
    
    if mode not in modes:
        print(f"Invalid mode: {mode}. Using 'tiny' instead.")
        mode = "tiny"
    
    config = modes[mode]
    
    print(f"\nMode: {mode.upper()}")
    print(f"  Base size: {config['base_size']}")
    print(f"  Image size: {config['image_size']}")
    print(f"  Crop mode: {config['crop_mode']}")
    print(f"\nImage: {image_path}")
    
    # Check device
    if torch.cuda.is_available():
        device = "cuda"
        device_name = torch.cuda.get_device_name(0)
    elif torch.backends.mps.is_available():
        device = "mps"
        device_name = "Apple Metal (MPS)"
    else:
        device = "cpu"
        device_name = "CPU"
    
    print(f"Device: {device} ({device_name})")
    print("\n" + "-"*80)
    
    # Load model
    model_name = 'deepseek-ai/DeepSeek-OCR'
    print(f"\nLoading model: {model_name}")
    print("This may take a moment on first run (downloading ~2-3GB)...")
    
    load_start = time.time()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    with patch("transformers.dynamic_module_utils.get_imports", fixed_get_imports):
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            use_safetensors=True
        )
    
    # Move to device
    if device == "cuda":
        model = model.eval().cuda().to(torch.bfloat16)
    elif device == "mps":
        model = model.eval().to(device)
    else:
        model = model.eval()
    
    load_time = time.time() - load_start
    print(f"✓ Model loaded in {load_time:.1f}s")
    
    # Prepare prompt
    prompt = "<image>\n<|grounding|>Convert the document to markdown."
    
    # Create output directory
    output_dir = Path("./test_ocr_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run OCR
    print(f"\nRunning OCR...")
    print(f"  Prompt: {prompt}")
    
    ocr_start = time.time()
    
    result = model.infer(
        tokenizer,
        prompt=prompt,
        image_file=str(image_path),
        output_path=str(output_dir),
        base_size=config['base_size'],
        image_size=config['image_size'],
        crop_mode=config['crop_mode'],
        save_results=False,
        test_compress=True
    )
    
    ocr_time = time.time() - ocr_start
    
    print(f"✓ OCR completed in {ocr_time:.1f}s")
    
    # Print results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    print(f"\nExtracted text length: {len(result)} characters")
    print(f"Total time: {load_time + ocr_time:.1f}s (load: {load_time:.1f}s, ocr: {ocr_time:.1f}s)")
    
    print(f"\nFirst 500 characters:")
    print("-"*80)
    print(result[:500])
    print("-"*80)
    
    # Save full result
    output_file = output_dir / f"ocr_result_{mode}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"\nFull text saved to: {output_file}")
    
    return result


def main():
    """Main function with command-line interface."""
    
    print("\n" + "="*80)
    print("DeepSeek OCR Test Script")
    print("="*80)
    
    # Default image path
    default_image = "./images/20251020_100526.jpg"
    
    # Parse command-line arguments
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = default_image
    
    if len(sys.argv) > 2:
        mode = sys.argv[2].lower()
    else:
        mode = "tiny"  # Default to fastest mode for testing
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"\nError: Image file not found: {image_path}")
        print("\nUsage:")
        print(f"  python {sys.argv[0]} [image_path] [mode]")
        print("\nModes:")
        print("  tiny   - Fastest, for quick testing (default)")
        print("  small  - Fast, good quality")
        print("  base   - Slow, better quality")
        print("  gundam - Slowest, best quality")
        print("\nExample:")
        print(f"  python {sys.argv[0]} ./images/myimage.jpg small")
        sys.exit(1)
    
    try:
        result = test_deepseek_ocr(image_path, mode)
        
        print("\n" + "="*80)
        print("TEST COMPLETE")
        print("="*80)
        print("\nTips for your M2 Mac:")
        print("  • 'tiny' or 'small' modes are recommended for speed")
        print("  • First run is slow due to model download (~2-3GB)")
        print("  • Subsequent runs are much faster")
        print("  • Close other apps to free up memory")
        print("  • If too slow, consider using a smaller base_size")
        
        print("\nNext steps:")
        print("  • Try different modes to find speed/quality balance")
        print("  • Once satisfied, integrate with full extraction pipeline")
        print("  • Check the saved .txt file for full results")
        
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
