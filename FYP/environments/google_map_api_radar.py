import requests
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

place_ids = []
def main():
	radius = 40000	# in metres
	latitude = "1.290270"
	longitude = "103.851959"
	google_url = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=" + latitude + "," + longitude + "&radius=" + str(radius) + "&key=" + GOOGLE_API_KEY + "&type=bank"
	#google_url = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=" + latitude + "," + longitude + "&radius=" + str(radius) + "&key=" + GOOGLE_API_KEY + "&keyword=Singapore"
	#google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latitude + "," + longitude + "&radius=" + str(radius) + "&key=" + GOOGLE_API_KEY
	google_url = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=latitude,longitude&radius=radius&key=GOOGLE_API_KEY&type=bank"

	response = requests.get(google_url)
	response_json = response.json()
	print response.json()
	venues_results = response_json["results"]
	place_ids = [venue_result["place_id"] for venue_result in venues_results]

	for place_id in place_ids:
		venue_details_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + GOOGLE_API_KEY
		venue_response = requests.get(venue_details_url)
		venue_response_json = venue_response.json()
		venue_name = venue_response_json["result"]["name"]
		place_id = venue_response_json["result"]["place_id"]
		print place_id


"https://maps.googleapis.com/maps/api/place/details/json?placeid=place_id&key=GOOGLE_API_KEY"
if __name__ == "__main__":
	main()