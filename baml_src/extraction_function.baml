// Function to extract HSDS-compliant data from a community services image
// Enhanced version with improved clarity and examples

function ExtractHSDSFromImage(image: image) -> HSDSData {
  client GPT4Vision
  prompt #"
  {{ _.role('system') }}
  You extract structured data from images and format it to HSDS. Produce accurate, complete HSDS data for service directories. Carefully distinguish organization info from services and locations.

  {{ _.role('user') }}
  Analyze the image and output HSDS-compliant data.

  {{ image }}
  
  ## EXTRACTION INSTRUCTIONS
  
  ### KEY OBJECTIVE
  Extract HSDS data strictly per {{ ctx.output_format }} and types in baml_src/hsds_types.baml. Return complete, accurate data with no extra commentary.

  ### HIGH-IMPACT RULES
  - **Cardinality**: One ServiceAtLocation per unique service-location pair.
  - **Org vs Service**: Org description = mission/impact/approach. Service description = what/how of that service only.
  - **Access vs Application**: Barriers/attributes vs steps to obtain service.
  - **Completeness**: Extract all services and locations; do not merge distinct items.

  ### NORMALIZATION
  - **Schedules**:
    - `freq`: DAILY (every day), WEEKLY (specific days), MONTHLY (specific dates).
    - `byday` (WEEKLY only): MO, TU, WE, TH, FR, SA, SU (list or range, e.g., MO,TU,WE,TH,FR).
    - `opens_at`/`closes_at`: HH:MM:SS 24h (e.g., 19:00:00 for 7 PM).
    - `year_round`: true if “365 days”/“year‑round”/“open every day”; else null/false.
    - `description`: concise human-readable summary.
  - **Phones**: Include type and optional description; [] if none.
  - **Cross_streets**: Use exact phrasing if present (e.g., "NE 45th & 16th Ave NE"); infer only if unambiguous.
  - **Latitude/Longitude**: null.
  - **Fees**: “Free”, “Sliding scale”, specific amount, or null.
  - **Auxiliary_resources**: Only if explicitly mentioned; comma-separated.

  ### AMBIGUITY RESOLUTION
  - Prefer explicit labels/headers.
  - If conflicting, use the most local/specific context.
  - When uncertain, set field to null rather than guessing.

  ### DATA QUALITY
  - Read all visible text (headers, fine print, banners).
  - Use exact wording where possible.
  - Avoid duplication across fields.
  - Ensure coverage of all services and locations shown.

  ### MINIMAL SCHEDULE EXAMPLE
  {
    description: "Daily 7:00 PM–8:00 PM, year-round",
    freq: "DAILY",
    byday: "MO,TU,WE,TH,FR,SA,SU",
    opens_at: "19:00:00",
    closes_at: "20:00:00",
    year_round: true
  }

  ### FIELD PRIORITY
  1. **Explicit labels/headers**
  2. **Context clues**
  3. **HSDS conventions** (fees in fees, etc.)

  {{ ctx.output_format }}
  "#
}