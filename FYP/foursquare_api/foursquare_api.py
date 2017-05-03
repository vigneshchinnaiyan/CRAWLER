import os
import requests
import json

FOURSQUARE_CLIENT_ID = os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET = os.environ.get('FOURSQUARE_CLIENT_SECRET')

venue_memo = set()

def get_next_venues(venue_id, next_venue_list):
	v = '20170101'
	nextvenues_url = "https://api.foursquare.com/v2/venues/" + venue_id + "/nextvenues?client_id=" + FOURSQUARE_CLIENT_ID + "&client_secret=" + FOURSQUARE_CLIENT_SECRET + "&v=" + v
	web_response = requests.get(nextvenues_url)
	resp = web_response.json()
	next_venue_ids = [venue["id"] for venue in resp["response"]["nextVenues"]["items"] if not (venue["id"] in venue_memo)]
	# for next_venue_id in next_venue_ids:
	# 	venue_memo.add(next_venue_id)
	# next_venue_list.extend(next_venue_ids)
	return next_venue_ids


def foursquare_parse(foursquare_venue_info):
    """
    Parameters:
    foursquare_venue_info: dict, from fetcher, using requests.get function

    Outputs:
    company_info: dict , information of the company
    """

    if foursquare_venue_info:
        fsquare_id = foursquare_venue_info['id'] if ('id' in foursquare_venue_info) else None
        company_name = foursquare_venue_info['name'] if ('name' in foursquare_venue_info) else None
        company_about = foursquare_get_categories(foursquare_venue_info["categories"]) if (foursquare_venue_info.has_key("categories")) else None
        company_phone = foursquare_venue_info['contact']['phone'] if (foursquare_venue_info.has_key("contact") and foursquare_venue_info["contact"].has_key("phone")) else None
        company_street = foursquare_venue_info["location"]['address'] if (foursquare_venue_info.has_key("location") and foursquare_venue_info["location"].has_key("address")) else None
        company_country = foursquare_venue_info["location"]['country'] if (foursquare_venue_info.has_key("location") and foursquare_venue_info["location"].has_key("country")) else None
        company_postal = foursquare_venue_info["location"]['postalCode'] if (foursquare_venue_info.has_key("location") and foursquare_venue_info["location"].has_key("postalCode")) else None
        company_longitude = foursquare_venue_info["location"]["lng"] if (foursquare_venue_info.has_key("location") and foursquare_venue_info["location"].has_key("lng")) else None
        company_latitude = foursquare_venue_info["location"]["lat"] if (foursquare_venue_info.has_key("location") and foursquare_venue_info["location"].has_key("lat")) else None
        company_fan_count = foursquare_venue_info["likes"]["count"] if (foursquare_venue_info.has_key("likes") and foursquare_venue_info["likes"].has_key("count")) else None
        company_hours = foursquare_venue_info["hours"]["status"] if (foursquare_venue_info.has_key("hours") and foursquare_venue_info["hours"].has_key("status")) else None
        company_link = foursquare_venue_info["url"] if (foursquare_venue_info.has_key("url")) else None
    """
    TODO
    this section
    """

    company_info = {
        'foursquare_resource_locator': fsquare_id,
        'description': company_about,
        'org_name': company_name,
        'address': company_street,
        'country': company_country,
        'postal_code': company_postal,
        'contact_no': company_phone,
        'longitude': company_longitude,
        'latitude': company_latitude,
        'fan_count': company_fan_count,
        'hours': company_hours,
        'link': company_link
    }

    return company_info 


def foursquare_get_categories(categories_array):
    """
    Parameters:
    categories_array is the categories field found in the foursquare response

    Output:
    categories_string

    Returns a concatenated string of the differnet categories
    """
    categories_string = None
    if categories_array:
        categories_string = ", ".join([category["name"] for category in categories_array])
    return categories_string 


def main():

	next_venue_list = []
	next_venue_result_list = []
	contact_info_array = []
	# here we get the top 20 most recommended places
	v = '20170101'
	near = 'Singapore'
	url = "https://api.foursquare.com/v2/venues/explore?near=" + near + "&client_id=" + FOURSQUARE_CLIENT_ID + "&client_secret=" + FOURSQUARE_CLIENT_SECRET + "&v=" + v + "&limit=20"
	web_response = requests.get(url)
	resp = web_response.json()
	first_venues = resp["response"]["groups"][0]["items"]

	for venue in first_venues:
		next_venue_list.append(venue["venue"]["id"])
		venue_memo.add(venue["venue"]["id"])

	for next_venue in next_venue_list:

		# from each id in next_venue_list we get their details and
		# nextvenues
		print next_venue
		url = "https://api.foursquare.com/v2/venues/" + next_venue + "?client_id=" + FOURSQUARE_CLIENT_ID + "&client_secret=" + FOURSQUARE_CLIENT_SECRET + "&v=" + v
		web_response = requests.get(url)
		resp = web_response.json()
		venue_info = resp["response"]["venue"]
		contact_info = foursquare_parse(venue_info)
		contact_info_array.append(contact_info)
		# here we get the next venues and we add to venue_memo
		next_venue_ids = get_next_venues(next_venue, next_venue_list)	
		next_venue_result_list.append(next_venue_ids)

	f = open('foursquare_data.json', 'w')
	json.dump(contact_info_array, f, indent=4)  
	json.dump(next_venue_result_list, f, indent=4)


if __name__ == "__main__":
	main()