# Image to HSDS

Extracts Human Services Data Specification (HSDS) structured data from a community services flyer image using BAML and an LLM vision model.

## Requirements
- Python 3.10+
- OpenAI API key (`OPENAI_API_KEY`)
- Packages in [requirements.txt](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/requirements.txt:0:0-0:0)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Set your OpenAI key:
   - Create a `.env` file with:
     OPENAI_API_KEY=your_key_here
   - Or export in your shell before running.

## Usage
Run with the default example image:
python extract_hsds.py

Run with a custom image:
python extract_hsds.py path/to/your_flyer.jpg

The script:
- Loads the image
- Calls the BAML function `ExtractHSDSFromImage`
- Prints a human-readable summary
- Writes structured HSDS JSON to `hsds_outputs/extracted_hsds_data.json`

## Project Structure
- [extract_hsds.py](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/extract_hsds.py:0:0-0:0) — main script
- `baml_src/` — BAML definitions
  - [clients.baml](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/baml_src/clients.baml:0:0-0:0) — OpenAI client config
  - [hsds_types.baml](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/baml_src/hsds_types.baml:0:0-0:0) — HSDS-related types
  - [extraction_function.baml](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/baml_src/extraction_function.baml:0:0-0:0) — extraction function and prompt
  - [generators.baml](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/baml_src/generators.baml:0:0-0:0) — codegen target (Python/Pydantic)
- `images/` — sample input images
- `hsds_outputs/` — extracted JSON output
- [requirements.txt](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/requirements.txt:0:0-0:0) — dependencies
- [README.md](cci:7://file:///Users/davidbotos/Desktop/9-BearHug_Product/4-Data_Orchestration/image-to-hsds/README.md:0:0-0:0) — this file

## Notes
- The extraction aims for HSDS-compliant objects:
  - Organization
  - Service
  - Location
  - ServiceAtLocation
- Some fields may be `null` if not present or ambiguous.

## Development
- BAML generates a Python client (`baml_client`) from `baml_src/`.
- If you edit `.baml` files, regenerate the client with your local BAML tooling.
- Ensure `OPENAI_API_KEY` is set before running.

## License
MIT License