import requests
import os
from bs4 import BeautifulSoup

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

def main():
	current_place_id = "ChIJg7HFkZYZ2jERMRl_wxZwEH0"
	venue_details_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + current_place_id + "&key=" + GOOGLE_API_KEY
	details_response = requests.get(venue_details_url)
	details_response_json = details_response.json()
	print details_response_json["result"]["adr_address"]
	soup = BeautifulSoup(details_response_json["result"]["adr_address"], 'html.parser')
	street_array = soup.find_all('span', class_=lambda x: (x != 'country-name') and (x != 'postal-code'))
	country_array =  soup.find_all('span', class_="country-name")
	postal_code_array = soup.find_all('span', class_="postal-code")

	street_string = ', '.join([tag.get_text() for tag in street_array])
	country_string = country_array[0].get_text()
	postal_code = postal_code_array[0].get_text()

	print street_string
	print country_string
	print postal_code

if __name__ == "__main__":
	main()