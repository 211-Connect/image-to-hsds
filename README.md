# HSDS Extraction Demo - Project Overview

## What This Project Does

This demo pipeline extracts structured Human Services Data Specification (HSDS) compliant data from community service flyer images using:

1. **BAML** - For type-safe prompt engineering and structured extraction
2. **OpenAI GPT-4 Vision** - To read and interpret the flyer image
3. **Python + Pydantic** - For application logic and data validation

## Problem It Solves

Community service organizations often share information through flyers that have:
- Non-standard text formatting
- Varied layouts and typography
- Multiple services and locations
- Complex schedule information
- Critical access information (free, no ID required, etc.)
- Geographic service areas distinct from physical addresses

Manually entering this data into structured formats (like HSDS) is:
- Time-consuming
- Error-prone
- Difficult to scale
- Risks losing important details (like "No ID Required")

This pipeline automates the extraction process while ensuring data quality through:
- Type-safe validation
- HSDS schema compliance
- Structured prompting with BAML
- Enhanced extraction of real-world flyer information

## Architecture

```
┌─────────────────┐
│  Flyer Image    │
│  (JPG/PNG)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  BAML Function              │
│  (ExtractHSDSFromImage)     │
│                             │
│  • Loads image              │
│  • Sends to OpenAI GPT-4    │
│  • Applies extraction prompt│
│  • Enhanced field detection │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  OpenAI Vision API          │
│  (gpt-4o)                   │
│                             │
│  • Analyzes flyer layout    │
│  • Reads all text           │
│  • Interprets information   │
│  • Detects access barriers  │
│  • Identifies service areas │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  BAML Type System           │
│                             │
│  • Validates structure      │
│  • Ensures HSDS compliance  │
│  • Generates Pydantic models│
│  • Enhanced with quick wins │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Structured Output          │
│                             │
│  • Organization info        │
│  • Services & schedules     │
│  • Locations & addresses    │
│  • Access requirements      │
│  • Service areas            │
│  • Auxiliary resources      │
│  • All HSDS-compliant       │
└─────────────────────────────┘
```

## Key Features

### 1. Type Safety
- BAML generates Python Pydantic models from type definitions
- Automatic validation ensures data integrity
- IDE autocomplete for all HSDS fields

### 2. Enhanced HSDS Compliance
- Core objects: Organization, Service, Location, ServiceAtLocation
- Supporting objects: Address, Schedule, Phone
  - Access requirements (free, no ID, confidential)
  - Service areas (geographic coverage)
  - Auxiliary resources (supplies, gear)
  - Cross-street references (location helpers)
  - Year-round operation indicators
- Extensible to full HSDS specification

### 3. Separation of Concerns
- Prompt engineering in `.baml` files
- Application logic in Python
- Easy to modify prompts without changing code

### 4. Robust Extraction
- Handles varied layouts and formats
- Works with wrinkled, photographed flyers
- Extracts complex schedule information
- Identifies multiple services and locations
- Captures critical access details from real flyers

## HSDS Coverage

This demo implements core HSDS objects with enhancements:

✅ **Organization**
- Name, description, URL

✅ **Service**
- Name, description, status
- Eligibility, fees, application process
- Schedules (with RRULE support)
- Phone numbers
- Access requirements (No ID, Free, Confidential, Low-barrier)
- Service area (Geographic coverage)
- Auxiliary resources (Toiletries, gear, supplies)

✅ **Location**
- Name, description
- Addresses (with full address breakdown)
- Geographic coordinates (optional)
- Cross streets (Intersection references)

✅ **Schedule**
- Frequency, days, times
- Year-round indicator (365 days operation)
- Enhanced: Better multi-day handling (TU,TH format)

✅ **ServiceAtLocation**
- Links services to specific locations
- Location-specific descriptions

### Quick Wins Implemented

Based on real-world flyer analysis (Teen Feed case study), we added:

1. **Access Requirements** - Captures "No ID Required", "Free", "Confidential", "Low-barrier"
2. **Service Area** - Geographic coverage like "University District Seattle"
3. **Auxiliary Resources** - Additional supplies: toiletries, gear, backpacks
4. **Cross Streets** - Location helpers: "(NE 45th & 16th Ave NE)"
5. **Year-Round Flag** - Identifies "365 days a year" operations

These enhancements capture critical information that appears on real flyers but wasn't in the original simplified types.

### Extensibility

The structure is ready to add:
- Contacts (with roles and departments)
- Accessibility information
- Funding sources
- Languages and interpretation services
- Cost options and fee structures
- Email addresses and social media
- Transit directions

## Technical Highlights

### BAML Benefits

1. **Structured Prompting**
   - Prompts are separate from code
   - Version controlled
   - Testable in BAML Playground

2. **Type Generation**
   - Automatic Pydantic model generation
   - Type-safe Python code
   - No manual JSON parsing

3. **Multi-Model Support**
   - Easy to switch between OpenAI models
   - Add fallback providers
   - A/B test different approaches

4. **Quick Win Fields**
   - Optional fields = backward compatible
   - Easy to add new extraction targets
   - Prompt enhancements guide AI to find info

### Python Integration

```python
from baml_client.baml_client.sync_client import b
from baml_py import Image

# Load image
img = Image.from_url(f"file://{image_path}")

# Extract HSDS data (guaranteed to return HSDSData type)
hsds_data = b.ExtractHSDSFromImage(flyer_image=img)

# Type-safe access to enhanced fields
print(hsds_data.organization.name)
for sal in hsds_data.services_at_locations:
    print(f"Service: {sal.service.name}")
    print(f"Location: {sal.location.name}")
    
    # Quick win fields
    if sal.service.access_requirements:
        print(f"Access: {sal.service.access_requirements}")
    if sal.service.service_area:
        print(f"Serves: {sal.service.service_area}")
    if sal.service.auxiliary_resources:
        print(f"Also provides: {sal.service.auxiliary_resources}")
    if sal.location.cross_streets:
        print(f"Near: {sal.location.cross_streets}")
```

### Enhanced Extraction Prompts

The extraction function now includes specific guidance for:

- **Access barriers**: Looks for "No ID Required", "Free", "Confidential", "Low-barrier", "Walk-in"
- **Geographic coverage**: Identifies neighborhood, district, and regional service areas
- **Auxiliary resources**: Finds supply lists and additional resources
- **Cross streets**: Captures intersection and location helper information
- **Day formatting**: Better handling of "Tuesday and Thursday" → "TU,TH"
- **Time conversion**: Explicit PM to 24-hour format reminders

## Example: Teen Feed Flyer

Input: Photographed flyer with multiple text blocks, varied formatting

Output: Structured HSDS data containing:
- 1 Organization (Teen Feed)
- 2 Services (U-District Dinner, In-Reach Drop-In)
- 2 Locations (Church, Shelter)
- Complete schedule information (daily 7-8pm, Tue/Thu 4:30-6:30pm)
- Eligibility (ages 13-25)
- Contact details
- **NEW: Access info** ("Free & Confidential - No ID Required")
- **NEW: Service area** ("University District Seattle")
- **NEW: Auxiliary resources** ("toiletries, cold weather gear, backpacks, first aid kits, underwear")
- **NEW: Cross streets** ("NE 45th & 16th Ave NE")
- **NEW: Year-round flag** (365 days a year)

All extracted automatically with proper HSDS structure + enhanced real-world fields.

## Production Considerations

To deploy this for production use:

1. **Error Handling**
   - Add retry logic for API failures
   - Handle malformed images
   - Validate extracted data against HSDS schema

2. **Batch Processing**
   - Process multiple flyers concurrently
   - Queue system for large volumes
   - Progress tracking and reporting

3. **Data Quality**
   - Human review workflow
   - Confidence scoring
   - Validation against known patterns
   - Field completeness metrics (new fields often present?)

4. **Export Formats**
   - Generate HSDS CSV files
   - Create JSON-LD for web publishing
   - API integration with resource directories

5. **Monitoring**
   - Track extraction accuracy
   - Monitor API costs
   - Log errors and edge cases
   - Track quick win field population rates

## Cost Estimation

Using OpenAI GPT-4o:
- Input: ~$2.50 per 1M tokens
- Output: ~$10.00 per 1M tokens

Typical flyer extraction:
- Image tokens: ~500-1000 tokens
- Output: ~500-2500 tokens (more with quick win fields)
- **Cost per flyer: $0.01-0.05**

For 1000 flyers/month: **$10-50/month**

Enhanced extraction adds minimal cost (~10% more output tokens) but captures significantly more valuable information.

## Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| OCR + Rules | Fast, deterministic | Breaks on varied formats |
| Traditional ML | No API costs | Requires training data |
| Manual Entry | 100% accurate | Slow, expensive |
| **BAML + LLM Vision** | **Robust, flexible, captures nuance** | **API costs** |

The enhanced quick win fields particularly benefit from LLM vision's ability to understand semantic meaning (e.g., recognizing "No ID Required" as an access requirement).

## Future Enhancements

1. **Multi-Language Support**
   - Extract services in multiple languages
   - Translate to English for HSDS

2. **Image Preprocessing**
   - Auto-rotate images
   - Enhance contrast/readability
   - Crop to relevant sections

3. **Validation Pipeline**
   - Check addresses against geocoding API
   - Verify phone numbers
   - Validate URLs

4. **Learning System**
   - Track corrections
   - Improve prompts based on feedback
   - Build domain-specific examples

5. **Web Interface**
   - Upload flyers via web form
   - Review and edit extracted data
   - Export in multiple formats

6. **Additional Quick Wins** (from future flyer analysis)
   - Email addresses
   - Social media links
   - Accessibility information
   - Languages spoken
   - Transit directions

## Getting Started

1. Read `QUICKSTART.md` for setup instructions
2. Run `verify_setup.py` to check configuration
3. Execute `python extract_hsds.py` to extract data
4. Review `README.md` for detailed documentation
5. Check `QUICK_WINS_SUMMARY.md` for enhancement details

## Files Included

- `baml_src/` - BAML definitions (types, functions, clients)
  - `hsds_types_enhanced.baml` - Enhanced types with quick wins
  - `extraction_function_enhanced.baml` - Enhanced prompts
- `extract_hsds.py` - Main extraction script
- `verify_setup.py` - Setup verification
- `example_output.json` - Sample output structure
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation
- `QUICKSTART.md` - Quick start guide
- `QUICK_WINS_SUMMARY.md` - Enhancement details
- `.env.example` - Environment template

## Success Criteria

This demo achieves:
- ✅ Loads images from local files
- ✅ Uses OpenAI vision models
- ✅ Structures extraction with BAML
- ✅ Outputs HSDS-compliant data
- ✅ Handles non-standard formatting
- ✅ Type-safe Python implementation
- ✅ Extensible architecture
- ✅ Captures real-world access barriers
- ✅ Identifies geographic service areas
- ✅ Extracts auxiliary resources
- ✅ Includes location helpers
- ✅ Better schedule parsing