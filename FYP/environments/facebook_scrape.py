import urllib2
import json
import re
from bs4 import BeautifulSoup

PHONE_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yD/r/29f4AUE0XdF.png"
WEBSITE_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/upNlw510Jd7.png"
MAIL_ICON = "https://static.xx.fbcdn.net/rsrc.php/v3/yg/r/wLlG5cEEIuu.png"

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

	return key, value	

def search_contact_info_section(contact_info):
	contact_info_title = contact_info[0].find('div', text = re.compile('CONTACT INFO'))
	contact_info = {}
	current_section = contact_info_title

	while current_section.next_sibling != None:
		current_section = current_section.next_sibling
		key, value = determine_field_and_value(current_section)
		contact_info[key] = value
	print(contact_info)	

	"""
	sections = contact_info_title.parent.findAll('div')
	found_strings = []
	for section in sections:
		section_string = str(section)
	print(found_strings)	
	"""

def main():
	# Change URL to scrape the different page
	url = "https://www.facebook.com/DeloitteSingapore/about/"

	web_response = urllib2.urlopen(url)
	readable_page = web_response.read()
	soup = BeautifulSoup(readable_page, "html.parser")

	contact_info = soup.findAll("div", id = re.compile('PagesProfileAboutFullColumnPagelet'))

	contact_info_array = search_contact_info_section(contact_info)

if __name__ == "__main__":
	main()
