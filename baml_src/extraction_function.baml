// Function to extract HSDS-compliant data from a community services flyer image
// Enhanced with better extraction prompts based on real-world flyer analysis

function ExtractHSDSFromImage(flyer_image: image) -> HSDSData {
  client GPT4Vision
  prompt #"
    {{ _.role('system') }}
    You are an expert at extracting structured information from community service flyers
    and organizing it according to the Human Services Data Specification (HSDS).
    
    Pay special attention to:
    - Access requirements and barriers (or lack thereof)
    - Geographic service areas
    - Auxiliary resources and supplies
    - Cross-street references for locations
    - Year-round vs. seasonal operation

    {{ _.role('user') }}
    Please analyze the following community services flyer image and extract all relevant information
    to create HSDS-compliant data.

    {{ flyer_image }}

    Extract the following information:

    1. Organization Information:
       - Name of the organization providing services
       - Description of what they do
       - Website URL if available
       - Tagline or mission statement if present
    
    2. Services and Locations:
       - For each service mentioned in the flyer:
         * Service name
         * Detailed description of the service
         * Who is eligible (age range, target population)
         * Schedule information (days of week, times)
         * Any fees or cost information ("Free" counts as fee information)
         * Application process or how to access
         
         **NEW - Pay special attention to:**
         * ACCESS REQUIREMENTS: Look for phrases like:
           - "No ID Required" / "ID Required"
           - "Free" / "Confidential"
           - "Low-barrier" / "No-barrier" / "Drop-in welcome"
           - "Walk-in" / "Appointment required"
           - "Resources Available On-Site"
           Extract these into the access_requirements field
         
         * SERVICE AREA: Look for geographic coverage like:
           - "University District Seattle"
           - "Downtown" / "Capitol Hill"
           - Neighborhood or district names
           - County or city names
           Extract this into the service_area field
         
         * AUXILIARY RESOURCES: Look for additional items/resources provided:
           - "toiletries, cold weather gear, backpacks"
           - "clothing, hygiene products"
           - "first aid kits, underwear"
           - Any supplies or amenities beyond the main service
           Extract these into the auxiliary_resources field
         
         * YEAR-ROUND OPERATION: Look for:
           - "365 days a year" / "Year-round"
           - "Open every day"
           Set year_round to true if mentioned
         
    3. Location Details:
       - Name of each location where services are provided
       - Full address (street, city, state, postal code)
       - Any location-specific details
       
       **NEW - Also extract:**
       * CROSS STREETS: Look for intersection or cross-street references:
         - Parenthetical references like "(NE 45th & 16th Ave NE)"
         - "Corner of X and Y"
         - "Near the intersection of..."
         Extract these into the cross_streets field
    
    4. Contact Information:
       - Phone numbers with their types
       - Any special instructions about confidentiality or ID requirements

    5. Schedule Formatting:
       - For days of week, use standard abbreviations: MO, TU, WE, TH, FR, SA, SU
       - For multiple specific days (like "Tuesday and Thursday"), use: "TU,TH"
       - For ranges (like "Monday-Friday"), use: "MO,TU,WE,TH,FR"
       - For "7 days a week" or "every day", use: "MO,TU,WE,TH,FR,SA,SU"
       - Use 24-hour time format (HH:MM:SS) - convert PM times correctly (7PM = 19:00:00)
       - Determine frequency: DAILY (every day), WEEKLY (specific days), MONTHLY (specific dates)

    General Guidelines:
    - If information is not clearly stated in the image, use null for optional fields
    - Use "active" as the status for all services unless otherwise indicated
    - For addresses, use "physical" as the address_type
    - Extract phone numbers in their clearest format
    - Set country to "US" for all addresses unless otherwise specified
    - Be thorough in reading all text, including fine print and banner text
    - Look for emphasis text (bold, larger font) as it often contains key information

    {{ ctx.output_format }}
  "#
}
