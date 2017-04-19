import requests
import json
import re
from bs4 import BeautifulSoup

# TO-DO : 1) Find better way to get "Find US" Section
#		  2) Get all content from location

PHONE_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yx/r/DVV3ImUW0WS.png"
WEBSITE_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/upNlw510Jd7.png"
MAIL_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yg/r/wLlG5cEEIuu.png"
LOCATION_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yF/r/kS8eNysxft5.png"

def determine_field_and_value(current_section):
	image_tag = current_section.find('img')
	image_src = image_tag['src']
	key = ""
	value = ""
	text_content = image_tag.parent.next_sibling

	while(text_content.find('div') != None):
		text_content = text_content.find('div')

	value = text_content.string

	if image_src == PHONE_ICON:
		key = "Phonenumber"

	elif image_src == WEBSITE_ICON:
		key = "Website"	

	elif image_src == MAIL_ICON:
		key = "Mail"	

	elif image_src == LOCATION_ICON:
		key = "Location"	

	return key, value	

def search_contact_info_section(contact_info):
	#print contact_info
	# NEED TO FIND BETTER WAY TO LOCATE "FIND US" SECTION
	find_us_title = contact_info[0].find('span')
	#print find_us_title
	contact_info_title = contact_info[0].find('div', text = re.compile('CONTACT DETAILS'))

	retrieved_contact_info = {}

	if find_us_title:
		current_section = find_us_title.parent

		while current_section.next_sibling != None:
			current_section = current_section.next_sibling
			#print current_section
			key, value = determine_field_and_value(current_section)
			retrieved_contact_info[key] = value	

	if contact_info_title:
		current_section = contact_info_title

		while current_section.next_sibling != None:
			current_section = current_section.next_sibling
			key, value = determine_field_and_value(current_section)
			retrieved_contact_info[key] = value
	print(retrieved_contact_info)	


def main():
	# Change URL to scrape the different page
	url = "https://www.facebook.com/GreatEasternLifeSG/about"

	web_response = requests.get(url)
	readable_page = web_response.text
	soup = BeautifulSoup(readable_page, "html.parser")

	contact_info = soup.findAll("div", id = re.compile('PagesProfileAboutFullColumnPagelet'))

	contact_info_array = search_contact_info_section(contact_info)

if __name__ == "__main__":
	main()
