import requests
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


def main():
	radius = 40000
	latitude = "1.3329"
	longitude = "103.7436"
	google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(latitude) + "," + str(longitude) + "&radius=" + str(radius) + "&key=" + GOOGLE_API_KEY
	response = requests.get(google_url)
	response_json = response.json()

	for result in response_json["results"]:
		print result["name"]
		print result["place_id"]


if __name__ == "__main__":
	main()