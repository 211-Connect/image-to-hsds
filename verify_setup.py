#!/usr/bin/env python3
"""
Setup verification script for DeepSeek OCR + Ollama pipeline
Checks that all dependencies and services are correctly configured
"""

import sys
import subprocess
from pathlib import Path

def check_mark(success):
    return "✓" if success else "✗"

def check_python_version():
    """Check Python version is 3.10+"""
    version = sys.version_info
    success = version.major == 3 and version.minor >= 10
    print(f"{check_mark(success)} Python version: {version.major}.{version.minor}.{version.micro}")
    return success

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"{check_mark(True)} Package '{package_name}' installed")
        return True
    except ImportError:
        print(f"{check_mark(False)} Package '{package_name}' NOT installed")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"{check_mark(True)} Ollama is installed and running")
            
            # Check if gpt-oss:20b is available
            if "gpt-oss:20b" in result.stdout or "gpt-oss" in result.stdout:
                print(f"{check_mark(True)} Model 'gpt-oss:20b' is available")
                return True
            else:
                print(f"{check_mark(False)} Model 'gpt-oss:20b' NOT found")
                print("  Run: ollama pull gpt-oss:20b")
                return False
        else:
            print(f"{check_mark(False)} Ollama returned error")
            return False
    except FileNotFoundError:
        print(f"{check_mark(False)} Ollama is NOT installed")
        print("  Install from: https://ollama.com/")
        return False
    except subprocess.TimeoutExpired:
        print(f"{check_mark(False)} Ollama command timed out")
        return False
    except Exception as e:
        print(f"{check_mark(False)} Error checking Ollama: {e}")
        return False

def check_ollama_connection():
    """Check if Ollama API is accessible"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"{check_mark(True)} Ollama API is accessible at localhost:11434")
            return True
        else:
            print(f"{check_mark(False)} Ollama API returned status {response.status_code}")
            return False
    except ImportError:
        print(f"{check_mark(False)} 'requests' package not installed (needed for check)")
        return False
    except Exception as e:
        print(f"{check_mark(False)} Cannot connect to Ollama API: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False

def check_gpu():
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"{check_mark(True)} CUDA GPU available: {torch.cuda.get_device_name(0)}")
            print(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        elif torch.backends.mps.is_available():
            print(f"{check_mark(True)} Apple Metal (MPS) GPU available")
            return True
        else:
            print(f"{check_mark(False)} No GPU detected (will use CPU - slower)")
            return False
    except ImportError:
        print(f"{check_mark(False)} PyTorch not installed (cannot check GPU)")
        return False

def check_baml_files():
    """Check if BAML files exist"""
    required_files = [
        "baml_src/clients.baml",
        "baml_src/extraction_function.baml",
        "baml_src/hsds_types.baml",
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        print(f"{check_mark(exists)} BAML file: {file_path}")
        all_exist = all_exist and exists
    
    return all_exist

def main():
    print("=" * 80)
    print("DeepSeek OCR + Ollama Setup Verification")
    print("=" * 80)
    print()
    
    checks = []
    
    print("--- System Requirements ---")
    checks.append(("Python 3.10+", check_python_version()))
    print()
    
    print("--- Python Packages ---")
    critical_packages = [
        "torch",
        "transformers",
        "baml_py",
        "pydantic",
        "dotenv",
        "PIL",
    ]
    for package in critical_packages:
        checks.append((f"Package: {package}", check_package(package)))
    print()
    
    print("--- GPU/Acceleration ---")
    checks.append(("GPU Available", check_gpu()))
    print()
    
    print("--- Ollama Setup ---")
    checks.append(("Ollama Installed", check_ollama()))
    checks.append(("Ollama API", check_ollama_connection()))
    print()
    
    print("--- BAML Configuration ---")
    checks.append(("BAML Files", check_baml_files()))
    print()
    
    # Summary
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✓ All checks passed! You're ready to run the extraction.")
        print("\nNext steps:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Run extraction: python extract_hsds_ollama.py")
    else:
        print("\n✗ Some checks failed. Please address the issues above.")
        print("\nCommon fixes:")
        print("  - Install missing packages: pip install -r requirements_ollama.txt")
        print("  - Install Ollama: https://ollama.com/")
        print("  - Pull model: ollama pull gpt-oss:20b")
        print("  - Start Ollama: ollama serve")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())