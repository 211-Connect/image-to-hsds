<div align="center">
  <img src="assets/LOGO.png" alt="Connect 211 Logo" width="400"/>
</div>

# Image to HSDS

<div align="center">
  <img src="assets/README_IMAGE.png" alt="HSDS Extraction Pipeline" width="100%"/>
</div>

Extracts Human Services Data Specification (HSDS) structured data from community services flyer images using BAML and GPT-4 Vision API.

## Overview

This tool automatically converts flyer images into structured, machine-readable HSDS-compliant data. Simply provide an image of a community services flyer, and the system will extract:

- **Organization** information
- **Service** details and descriptions
- **Location** data with addresses
- **ServiceAtLocation** relationships

Perfect for digitizing community resource information and making it accessible through standardized APIs.

## Requirements

- **Python 3.10+**
- **OpenAI API key** - Set as `OPENAI_API_KEY` environment variable
- **Dependencies** - Listed in `requirements.txt`

### Cost Estimate

Using GPT-4 Vision API:
- Typical cost: ~$0.01-0.05 per image
- Based on image size and complexity

> **Looking for a free alternative?** Check out the [`deepseekOCR` branch](../../tree/deepseekOCR) which uses fully local, open-source models with no API costs.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/image-to-hsds.git
cd image-to-hsds
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your OpenAI API Key

**Option A: Using a `.env` file (recommended)**
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

**Option B: Export in your shell**
```bash
export OPENAI_API_KEY=your_key_here
```

> Get your API key at [platform.openai.com](https://platform.openai.com/api-keys)

## Usage

### Basic Usage

Run with the default example image:
```bash
python extract_hsds.py
```

### Custom Image

Run with your own flyer:
```bash
python extract_hsds.py path/to/your_flyer.jpg
```

### What Happens

The script performs the following steps:

1. **Loads the image** from the specified path
2. **Calls GPT-4 Vision API** via BAML function `ExtractHSDSFromImage`
3. **Extracts structured data** following HSDS specification
4. **Prints a summary** to the console for quick review
5. **Saves JSON output** to `hsds_outputs/extracted_hsds_data.json`

### Output Files

- **Console**: Human-readable summary of extracted data
- **JSON File**: `hsds_outputs/extracted_hsds_data.json` - Complete HSDS-compliant structured data

### Example Output

```json
{
  "organization": {
    "name": "Teen Feed",
    "description": "Meals, connections & resources for youth..."
  },
  "services": [
    {
      "name": "U-District Dinner",
      "description": "365 days a year..."
    }
  ],
  "locations": [...],
  "service_at_locations": [...]
}
```

## Project Structure

```
image-to-hsds/
├── extract_hsds.py              # Main extraction script
├── baml_src/                    # BAML definitions
│   ├── clients.baml            # OpenAI GPT-4 Vision client config
│   ├── hsds_types.baml         # HSDS type definitions
│   ├── extraction_function.baml # Extraction function and prompts
│   └── generators.baml         # Python/Pydantic code generation
├── baml_client/                # Auto-generated Python client
├── assets/                     # Branding and documentation images
│   ├── LOGO.png
│   └── README_IMAGE.png
├── images/                     # Sample input flyers
├── hsds_outputs/               # Extracted JSON output
├── requirements.txt            # Python dependencies
├── .env                        # API keys (create this)
└── README.md                   # This file
```

### Key Files

- **`extract_hsds.py`** - Main script that orchestrates the extraction
- **`baml_src/extraction_function.baml`** - Contains the prompt and extraction logic
- **`baml_src/hsds_types.baml`** - Defines the HSDS data structure
- **`baml_client/`** - Auto-generated from BAML files (don't edit directly)

## HSDS Compliance

The extraction produces HSDS-compliant JSON objects including:

- **Organization** - Details about the service provider
- **Service** - Specific programs or services offered
- **Location** - Physical addresses and accessibility info
- **ServiceAtLocation** - Relationships linking services to locations

**Note**: Some fields may be `null` if the information is not present in the flyer or is ambiguous.

## Development

### Modifying BAML Files

BAML generates a Python client (`baml_client/`) from the definitions in `baml_src/`. After editing any `.baml` files, regenerate the client:

```bash
# Install BAML CLI (if not already installed)
npm install -g @boundaryml/baml

# Regenerate the Python client
baml-cli generate
```

### BAML Resources

- **Documentation**: [docs.boundaryml.com](https://docs.boundaryml.com/home)
- **BAML Language Guide**: Learn about types, prompts, and clients
- **Examples**: Check `baml_src/` for working examples

### Customizing Prompts

Edit `baml_src/extraction_function.baml` to:
- Adjust extraction instructions
- Add/remove HSDS fields
- Change the model (e.g., `gpt-4o`, `gpt-4-turbo`)
- Modify temperature or other parameters

### Testing

Before running on production data:

1. **Test with sample images** in the `images/` directory
2. **Verify API key** is set correctly
3. **Check output** in `hsds_outputs/` for quality
4. **Iterate on prompts** if extraction quality needs improvement

## Alternatives

### Looking for a Free, Local Solution?

Check out the **[`deepseekOCR` branch](../../tree/deepseekOCR)** which uses:
- ✅ **DeepSeek OCR** - State-of-the-art document understanding
- ✅ **Ollama (gpt-oss-20b)** - Local LLM for extraction
- ✅ **No API costs** - Runs completely offline
- ✅ **Privacy-first** - Data never leaves your machine

Trade-offs:
- Slower processing (~1-2 minutes vs 5-10 seconds)
- Requires more local resources (16GB+ RAM recommended)
- Slightly lower accuracy on complex layouts

## Contributing

Contributions are welcome! Please feel free to:

- 🐛 Report bugs or issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **[BAML](https://www.boundaryml.com/)** - For structured LLM outputs
- **[OpenAI](https://openai.com/)** - For GPT-4 Vision API
- **[HSDS](https://openreferral.org/)** - Human Services Data Specification
- **Connect 211** - For supporting community resource data digitization

---

<div align="center">
  <p>Built by Connect211 with ❤️ for making community services data more accessible</p>
  <p>
    <a href="https://docs.boundaryml.com">BAML Docs</a> •
    <a href="https://openreferral.org/">HSDS Specification</a> •
    <a href="../../tree/deepseekOCR">Local Alternative Branch</a>
  </p>
</div>