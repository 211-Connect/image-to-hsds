// HSDS Core Types - Simplified for demo purposes

class Organization {
  name string @description("The official or public name of the organization")
  alternate_name string? @description("Alternative or commonly used name for the organization")
  description string @description("A brief summary about the organization")
  url string? @description("The URL for the organization's website")
}

class Location {
  name string @description("The name of the location")
  description string? @description("A description of this location")
  latitude float? @description("Y coordinate of location expressed in decimal degrees in WGS84 datum")
  longitude float? @description("X coordinate of location expressed in decimal degrees in WGS84 datum")
  addresses Address[] @description("The addresses at which this location operates")
}

class Address {
  address_1 string @description("The first line of the address")
  city string @description("The city in which the address is located")
  state_province string @description("The state or province in which the address is located")
  postal_code string @description("The postal code for the address")
  country string @description("The country in which the address is located")
  address_type "physical" | "postal" | "virtual" @description("The type of address")
}

class Service {
  name string @description("The official or public name of the service")
  description string @description("A detailed description of the service")
  status "active" | "inactive" | "defunct" | "temporarily closed" @description("The current status of the service")
  interpretation_services string? @description("A description of any interpretation services available for accessing this service")
  application_process string? @description("The steps needed to access the service")
  wait_time string? @description("Time a client may expect to wait before receiving a service")
  fees string? @description("Details of any charges for service users to access this service")
  accreditations string? @description("Details of any accreditations held by the service")
  eligibility string? @description("The requirements to receive the service")
  schedules Schedule[] @description("The details of when a service or location is open")
  phones Phone[] @description("Phone numbers for the service")
}

class Schedule {
  description string? @description("Human-readable description of the schedule")
  freq "WEEKLY" | "MONTHLY" | "DAILY" @description("How often the service is open")
  byday string? @description("Which days of the week (e.g. MO, TU, WE, TH, FR, SA, SU) or day of month")
  bymonthday int? @description("The day of the month when service is open")
  opens_at string @description("The time when service begins (HH:MM:SS format)")
  closes_at string @description("The time when service ends (HH:MM:SS format)")
}

class Phone {
  number string @description("The phone number")
  extension string? @description("The extension for the phone number")
  phone_type "voice" | "fax" | "cell" | "video" | "pager" | "text" | "textphone" | "toll_free" @description("The type of phone number")
  description string? @description("A description of the phone number")
}

class ServiceAtLocation {
  service Service @description("The service provided at this location")
  location Location @description("The location where the service is provided")
  description string? @description("A description of the service at this specific location")
}

// Top-level extraction result
class HSDSData {
  organization Organization @description("The organization providing the services")
  services_at_locations ServiceAtLocation[] @description("The services and their locations")
}
