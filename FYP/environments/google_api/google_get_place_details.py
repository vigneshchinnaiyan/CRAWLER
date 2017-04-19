import requests
import os
from bs4 import BeautifulSoup
import json

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


def google_fetch_details(google_id):
    """
    https://developers.google.com/places/web-service/
    """
    google_details_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + google_id + "&key=" + GOOGLE_API_KEY
    google_response = requests.get(google_details_url)
    google_response_json = google_response.json()
    return google_response_json["result"]


def google_parse(google_venue_info):
    """
    Parameters:
    google_venue_info: dict, from fetcher, using requests.get function

    Outputs:
    company_info: dict , information of the company
    """
    
    if google_venue_info:
        google_id = google_venue_info['place_id'] if ('place_id' in google_venue_info) else None
        company_name = google_venue_info['name'] if ('name' in google_venue_info) else None
        company_phone = google_venue_info['formatted_phone_number'] if ('formatted_phone_number' in google_venue_info) else None
        company_street, company_country, company_postal = google_get_address(google_venue_info['adr_address'])
        company_longitude = google_venue_info['geometry']['location']['lng'] if (google_venue_info.has_key("geometry") and google_venue_info["geometry"].has_key("location") and google_venue_info["geometry"]["location"].has_key("lng")) else None
        company_latitude = google_venue_info['geometry']['location']['lat'] if (google_venue_info.has_key("geometry") and google_venue_info["geometry"].has_key("location") and google_venue_info["geometry"]["location"].has_key("lat")) else None
        company_rating = google_venue_info['rating'] if ('rating' in google_venue_info) else None
        company_category = google_get_category(google_venue_info['types']) if ('types' in google_venue_info) else None
        company_link = google_venue_info['website'] if ('website' in google_venue_info) else None 
        company_intl_number_with_plus = google_venue_info['international_phone_number'] if ('international_phone_number' in google_venue_info) else None

    company_info = {
        'org_name': company_name,
        'address': company_street,
        'country': company_country,
        'postal_code': company_postal,
        'contact_no': company_phone,
        'industry': company_category,
        'google_resource_locator': google_id,
        'longitude': company_longitude,
        'latitude': company_latitude,
        'rating': company_rating,
        'link': company_link,
        'intl_number_with_plus': company_intl_number_with_plus
    }

    return company_info


def google_get_address(google_address_info):
    """
    Parameters:
    "adr_address" field from google_response

    Output:
    company_street: string
    company_country: string
    company_postal: string

    adr-address consists of a string with <span> tags containing street, country, postal-code information
    This function serves to split up the string and obtain the various information
    """
    company_street = company_country = company_postal = None

    if google_address_info:
        address_soup = BeautifulSoup(google_address_info, 'html.parser')
        street_array = address_soup.find_all('span', class_=lambda x: (x != 'country-name') and (x != 'postal-code'))
        country_array = address_soup.find_all('span', class_="country-name")
        postal_code_array = address_soup.find_all('span', class_="postal-code")

        company_street = ', '.join([tag.get_text() for tag in street_array]) if street_array else None
        company_country = country_array[0].get_text() if country_array else None
        company_postal = postal_code_array[0].get_text() if postal_code_array else None

    return company_street, company_country, company_postal      


def google_get_category(types_array):
    """
    Parameters:
    types_array consists of the "types" field that can be found in the google raw_response

    Output:
    categories_string: string

    Returns a concatenated string of the different types
    """
    categories_string = None
    if types_array:
        categories_string = ', '.join(types_array)
    return categories_string 


def google_fetch_nextvenues(google_response):
    """
    https://developers.google.com/places/web-service/

    Parameters:
    google_response: json output from google_fetch()

    Outputs:
    google_nextvenues_ids: array of google place_ids for next venues to explore
    """

    """
    First we find the latitude and longitude of the current venue
    """
    venue_latitude = google_response["geometry"]["location"]["lat"] if (google_response.has_key('geometry') and google_response['geometry'].has_key('location') and google_response['geometry']['location'].has_key('lat')) else None
    venue_longitude = google_response["geometry"]["location"]["lng"] if (google_response.has_key('geometry') and google_response['geometry'].has_key('location') and google_response['geometry']['location'].has_key('lng')) else None

    google_nextvenues_ids = [] 

    if (venue_latitude != None) and (venue_longitude != None):
        """
        We calculate new latitude and longitude to find new place_ids of locations aorund that coordinate

        Here we divide by 222.0 because 1 degree = 111.0km approximately and we want to move
        our search coordinate by 500m approximately

        Positive latitude is above the equator
        Positive longitude is east of the meridian

        We set our search radius as 500m
        """
        new_latitude = float(venue_latitude) + (1.0 / 222.0)
        new_longitude = float(venue_longitude) + (1.0 / 222.0)
        radius = 500
        next_venues_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(new_latitude) + "," + str(new_longitude) + "&radius=" + str(radius) + "&rankby=prominence&key=" + GOOGLE_API_KEY
        response = requests.get(next_venues_url)
        response_json = response.json()
        venues_results = response_json["results"]
        for venue_result in venues_results:
            google_nextvenues_ids.append(venue_result["place_id"])

    return google_nextvenues_ids


def write_to_json_file(contact, google_next_venues):
    f = open('google_place_api_details_data.json', 'w')
    json.dump(contact, f, indent=4)  
    json.dump(google_next_venues, f, indent=4) 


def main():
	current_place_id = "ChIJg7HFkZYZ2jERMRl_wxZwEH0"
	details_response_json = google_fetch_details(current_place_id)
	contact = google_parse(details_response_json)
	google_next_venues = google_fetch_nextvenues(details_response_json)
	write_to_json_file(contact, google_next_venues)

if __name__ == "__main__":
	main()