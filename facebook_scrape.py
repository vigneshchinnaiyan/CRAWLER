import urllib2
import json
from bs4 import BeautifulSoup

def main():
	list_companies = ["walmart", "cisco", "pepsi", "facebook"]
	url = "https://www.facebook.com/benjamin.soon.5"

	web_response = urllib2.urlopen(url)
	readable_page = web_response.read()
	soup = BeautifulSoup(readable_page, "html.parser")
	person_name_id = "fb-timeline-cover-name"
	person_name = soup.find(id=person_name_id)

	print person_name

if __name__ == "__main__":
	main()
