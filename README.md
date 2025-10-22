<div align="center">
  <img src="assets/LOGO.png" alt="Connect 211 Logo" width="400"/>
</div>

# Image to HSDS - DeepSeek OCR + Ollama Branch

<div align="center">
  <img src="assets/README_IMAGE.png" alt="HSDS Extraction Pipeline" width="100%"/>
</div>

This branch extracts Human Services Data Specification (HSDS) structured data from community services flyer images using a two-stage pipeline:

1. **DeepSeek OCR** - Extracts text/markdown from images (runs locally via Hugging Face)
2. **gpt-oss-20b** - Extracts structured HSDS data from text (runs locally via Ollama)

## Why This Approach?

This pipeline replaces the OpenAI GPT-4 Vision API with **fully local, open-source models**:

- ✅ **No API costs** - Both models run locally
- ✅ **No API keys needed** - No OpenAI account required
- ✅ **Privacy-first** - Data never leaves your machine
- ✅ **High quality** - DeepSeek OCR is state-of-the-art for document understanding
- ✅ **Flexible** - Can run on CPU (slower) or GPU (faster)

## Requirements

### Hardware
- **Minimum**: 16GB RAM, modern CPU (will be slow)
- **Recommended**: 16GB+ RAM, GPU with 8GB+ VRAM (for DeepSeek OCR)
- **Note**: DeepSeek OCR can run on CPU, but will be significantly slower

### Software
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- CUDA 11.8+ (optional, for GPU acceleration)

## Setup

### 1. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com/).

Then download the gpt-oss-20b model:
```bash
ollama pull gpt-oss:20b
```

To test Ollama is working:
```bash
ollama run gpt-oss:20b
# Type a message to test, then type /bye to exit
```

### 2. Set Up Python Environment

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements_ollama.txt
```

**Optional - Flash Attention (for faster inference on CUDA GPUs):**
```bash
pip install flash-attn==2.7.3 --no-build-isolation
```

### 3. Set Up BAML

Copy the new BAML files to your `baml_src/` directory:
```bash
# Copy the Ollama client configuration
cp clients_ollama.baml baml_src/clients.baml

# Copy the text-based extraction function
cp extraction_function_ollama.baml baml_src/extraction_function.baml
```

If you need to regenerate the BAML client:
```bash
# Install BAML CLI if you haven't
npm install -g @boundaryml/baml

# Regenerate client
baml-cli generate
```

## Usage

### Basic Usage

Start Ollama in one terminal:
```bash
ollama serve
```

In another terminal, run the extraction:
```bash
python extract_hsds_ollama.py
```

### With Custom Image

```bash
python extract_hsds_ollama.py path/to/your_flyer.jpg
```

### What Happens

The script performs a two-stage extraction:

**Stage 1 - OCR Extraction:**
- Loads the flyer image
- Uses DeepSeek OCR to extract text/markdown
- Saves OCR output to `hsds_outputs/ocr_extracted_text.txt`
- Shows preview of extracted text

**Stage 2 - Structure Extraction:**
- Sends OCR'd text to gpt-oss-20b via Ollama
- Uses BAML prompting for structured extraction
- Extracts HSDS-compliant data
- Saves result to `hsds_outputs/extracted_hsds_data_ollama.json`

### Output Files

- `hsds_outputs/ocr_extracted_text.txt` - Raw text extracted by DeepSeek OCR
- `hsds_outputs/extracted_hsds_data_ollama.json` - Final HSDS structured data

## Project Structure

```
.
├── extract_hsds_ollama.py           # Main script (two-stage pipeline)
├── baml_src/
│   ├── clients_ollama.baml          # Ollama client config
│   ├── extraction_function_ollama.baml  # Text-based extraction function
│   ├── hsds_types.baml              # HSDS type definitions (unchanged)
│   └── generators.baml              # Code generation config (unchanged)
├── images/                          # Input images
├── hsds_outputs/                    # Output directory
│   ├── ocr_extracted_text.txt      # OCR output
│   └── extracted_hsds_data_ollama.json  # Final HSDS data
├── requirements_ollama.txt          # Dependencies for this branch
└── README_OLLAMA.md                 # This file
```

## Model Configuration

### DeepSeek OCR Settings

The script uses "Gundam" mode for high-quality extraction:
- `base_size=1024` - Base resolution
- `image_size=640` - Crop resolution
- `crop_mode=True` - Multi-crop for better quality

You can adjust these in `extract_hsds_ollama.py` for different speed/quality tradeoffs:

| Mode   | base_size | image_size | crop_mode | Speed | Quality |
|--------|-----------|------------|-----------|-------|---------|
| Tiny   | 512       | 512        | False     | Fast  | OK      |
| Small  | 640       | 640        | False     | Good  | Good    |
| Base   | 1024      | 1024       | False     | Slow  | Better  |
| Gundam | 1024      | 640        | True      | Slow  | Best    |

### Ollama Settings

The BAML client is configured in `clients_ollama.baml`:
```baml
client<llm> OllamaGPTOSS {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "gpt-oss:20b"
    temperature 0.1
  }
}
```

You can adjust:
- `temperature` - Lower = more deterministic (0.0-1.0)
- `base_url` - Change if Ollama runs on different port/host
- `model` - Use different Ollama model if desired

## Performance Notes

### Speed

**On M1/M2 Mac (16GB RAM):**
- DeepSeek OCR: ~30-60 seconds per image
- gpt-oss-20b: ~10-30 seconds for extraction
- **Total**: ~1-2 minutes per flyer

**On CUDA GPU (8GB+ VRAM):**
- DeepSeek OCR: ~10-20 seconds per image
- gpt-oss-20b: ~5-15 seconds for extraction
- **Total**: ~20-40 seconds per flyer

**On CPU only:**
- Much slower (5-10x), but still works!

### Memory Usage

- DeepSeek OCR: ~4-6GB GPU memory (or 8-12GB RAM if CPU)
- gpt-oss-20b: ~12-16GB RAM
- **Total**: ~20-25GB RAM for CPU-only mode

## Troubleshooting

### Ollama Connection Issues

**Error**: Connection refused to localhost:11434

**Solution**: 
```bash
# Make sure Ollama is running
ollama serve

# Or just run the model directly
ollama run gpt-oss:20b
```

### Out of Memory

**For DeepSeek OCR:**
- Try smaller resolution modes (Tiny or Small)
- Close other applications
- Use CPU mode instead of GPU

**For gpt-oss-20b:**
- Make sure you have 16GB+ RAM
- Try a smaller model: `ollama pull llama3:8b`
- Update the model in `clients_ollama.baml`

### DeepSeek OCR Installation Issues

**Flash Attention fails to install:**
```bash
# Skip flash attention, use default attention
# The model will still work, just slightly slower
```

**Transformer version conflicts:**
```bash
pip install transformers==4.46.3 --force-reinstall
```

### Slow Performance

- Use GPU if available
- Use smaller DeepSeek OCR mode (Tiny or Small)
- Consider using fewer crops in DeepSeek OCR
- Ensure Ollama is using GPU (check with `ollama ps`)

## Comparison with Original

| Feature | Original (OpenAI) | This Branch (Local) |
|---------|------------------|---------------------|
| Vision Model | GPT-4 Vision | DeepSeek OCR |
| Language Model | GPT-4o | gpt-oss-20b |
| Cost | ~$0.01-0.05/image | Free |
| Speed | ~5-10 sec | ~1-2 min |
| Privacy | Data sent to OpenAI | Fully local |
| API Key | Required | Not needed |
| Internet | Required | Not required |
| Quality | Excellent | Very Good |

## Advanced Usage

### Batch Processing

Process multiple flyers:
```python
import os
from pathlib import Path

image_dir = Path("./images")
for image_file in image_dir.glob("*.jpg"):
    print(f"Processing {image_file}")
    os.system(f"python extract_hsds_ollama.py {image_file}")
```

### Custom Prompts

Edit `extraction_function_ollama.baml` to customize the extraction prompt:
- Add specific instructions for your use case
- Adjust field priorities
- Change normalization rules

### Using Different Models

Try different Ollama models:
```bash
# Download alternative models
ollama pull llama3:70b  # Larger, more capable
ollama pull mistral:7b  # Smaller, faster

# Update clients_ollama.baml
client<llm> OllamaGPTOSS {
  options {
    model "llama3:70b"  # Change this
  }
}
```

## Development

### Regenerating BAML Client

After modifying `.baml` files:
```bash
baml-cli generate
```

### Testing Changes

Test with a single flyer:
```bash
python extract_hsds_ollama.py images/test_flyer.jpg
```

## Notes

- **First run**: DeepSeek OCR will download the model (~2-3GB)
- **Accuracy**: Results may vary vs GPT-4 Vision, but are generally very good
- **Customization**: Both stages are independently tunable
- **Offline**: Once models are downloaded, works completely offline

## License

MIT License (same as original project)

## Acknowledgments

- [DeepSeek AI](https://github.com/deepseek-ai/DeepSeek-OCR) - For the excellent OCR model
- [Ollama](https://ollama.com/) - For easy local LLM deployment
- [BAML](https://www.boundaryml.com/) - For structured LLM outputs
- Original HSDS extraction project