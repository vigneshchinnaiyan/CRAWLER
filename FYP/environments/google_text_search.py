import requests
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
place_ids = []
visited_place_ids = set()

def main():
	newTerm = "Singapore"
	response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + \
        newTerm.replace(" ", "+") + "&key=" + GOOGLE_API_KEY)
	#response = requests.get(google_url)
	response_json = response.json()

	for result in response_json["results"]:
		first_id = result["place_id"]

	place_ids.append(first_id)
	visited_place_ids.add(first_id)	
	radius = 500
	count = 0
	while(place_ids):
		current_place_id = place_ids.pop(0)
		venue_details_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + current_place_id + "&key=" + GOOGLE_API_KEY
		venue_response = requests.get(venue_details_url)
		venue_response_json = venue_response.json()
		#print venue_response_json
		venue_name = venue_response_json["result"]["name"]
		venue_address = venue_response_json["result"]["adr_address"]
		print venue_name
		print venue_address
		count += 1
		print count
		print len(place_ids)
		print len(visited_place_ids)
		venue_latitude = venue_response_json["result"]["geometry"]["location"]["lat"]
		venue_longitude = venue_response_json["result"]["geometry"]["location"]["lng"]

		#print venue_name

		# 222 because 1 degree is 111 km approximately and we want to check 500m
		# from the current venue
		# positive latitude is above the equator
		# positive longitude is east of the prime meridian
		new_latitude = venue_latitude + (1.0 / 222.0)
		new_longitude = venue_longitude + (1.0 / 222.0)
		#google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(new_latitude) + "," + str(new_longitude) + "&radius=" + str(radius) + "&key=" + GOOGLE_API_KEY
		google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(new_latitude) + "," + str(new_longitude) + "&radius=" + str(radius) + "&rankby=prominence&key=" + GOOGLE_API_KEY
		response = requests.get(google_url)
		response_json = response.json()
		#print response_json
		venues_results = response_json["results"]
		#print venues_results
		for venue_result in venues_results:
			#if venue_result["place_id"] not in visited_place_ids:
			place_ids.append(venue_result["place_id"])
			visited_place_ids.add(venue_result["place_id"])

if __name__ == "__main__":
	main()

