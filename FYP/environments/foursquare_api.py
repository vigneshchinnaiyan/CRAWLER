import os
import requests

FOURSQUARE_CLIENT_ID = os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET = os.environ.get('FOURSQUARE_CLIENT_SECRET')

venue_memo = set()

def get_next_venues(venue_id, next_venue_list):
	v = '20170101'
	nextvenues_url = "https://api.foursquare.com/v2/venues/" + venue_id + "/nextvenues?client_id=" + FOURSQUARE_CLIENT_ID + "&client_secret=" + FOURSQUARE_CLIENT_SECRET + "&v=" + v
	web_response = requests.get(nextvenues_url)
	resp = web_response.json()
	next_venue_ids = [venue["id"] for venue in resp["response"]["nextVenues"]["items"] if not (venue["id"] in venue_memo)]
	for next_venue_id in next_venue_ids:
		venue_memo.add(next_venue_id)
	next_venue_list.extend(next_venue_ids)
	return

def main():

	next_venue_list = []

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
	

	#"https://api.foursquare.com/v2/venues/venue_id?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20170101"

	while(next_venue_list):

		# from each id in next_venue_list we get their details and
		# nextvenues
		venue_id = next_venue_list.pop(0)
		url = "https://api.foursquare.com/v2/venues/" + venue_id + "?client_id=" + FOURSQUARE_CLIENT_ID + "&client_secret=" + FOURSQUARE_CLIENT_SECRET + "&v=" + v
		web_response = requests.get(url)
		resp = web_response.json()
		venue_info = resp["response"]
		print venue_info
		print venue_info["venue"]["name"]

		# here we get the next venues and we add to venue_memo
		get_next_venues(venue_id, next_venue_list)	


if __name__ == "__main__":
	main()