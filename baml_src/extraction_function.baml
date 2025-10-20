// Function to extract HSDS-compliant data from a community services flyer image

function ExtractHSDSFromImage(flyer_image: image) -> HSDSData {
  client GPT4Vision
  prompt #"
    {{ _.role('system') }}
    You are an expert at extracting structured information from community service flyers
    and organizing it according to the Human Services Data Specification (HSDS).

    {{ _.role('user') }}
    Please analyze the following community services flyer image and extract all relevant information
    to create HSDS-compliant data.

    {{ flyer_image }}

    Extract the following information:

    1. Organization Information:
       - Name of the organization providing services
       - Description of what they do
       - Website URL if available
    
    2. Services and Locations:
       - For each service mentioned in the flyer:
         * Service name
         * Detailed description of the service
         * Who is eligible (age range, target population)
         * Schedule information (days of week, times)
         * Any fees or cost information
         * Application process or how to access
         
    3. Location Details:
       - Name of each location where services are provided
       - Full address (street, city, state, postal code)
       - Any location-specific details
    
    4. Contact Information:
       - Phone numbers with their types
       - Any special instructions about confidentiality or ID requirements

    Guidelines:
    - If information is not clearly stated in the image, use null for optional fields
    - For schedules, use 24-hour time format (HH:MM:SS)
    - For schedule frequency, determine if it's DAILY, WEEKLY, or MONTHLY
    - Use "active" as the status for all services unless otherwise indicated
    - For addresses, use "physical" as the address_type
    - Extract phone numbers in their clearest format
    - For eligibility, include age ranges and target populations mentioned
    - Set country to "US" for all addresses unless otherwise specified

    {{ ctx.output_format }}
  "#
}
