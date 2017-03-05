import facebook


def concatenate_facebook_location(company_location_dict):
	company_street = company_location_dict['street'] if ('street' in company_location_dict) else ''
	company_country = company_location_dict['country'] if ('country' in company_location_dict)  else ''
	company_postal = company_location_dict['zip'] if ('zip' in company_location_dict) else ''
	company_location = company_street + ', ' + company_country + ' ' + company_postal
	company_location = company_location.strip()
	company_location = company_location.strip(',')

	return company_location


access_token = 'access token here'

graph = facebook.GraphAPI(access_token)

company = 'some random company'

timbreplus_profile = graph.get_object(company)
print timbreplus_profile['id']
company_data = graph.get_connections(id=timbreplus_profile['id'], connection_name='likes')['data']
print company_data
for company in company_data:
	print "===Company info==="
	company_info = graph.get_object(id=company['id'], fields='name, about, location, phone, business, category, company_overview')
	if company_info:
		company_name = company_info['name'] if ('name' in company_info) else ''
		company_about = company_info['about'] if ('about' in company_info) else ''
		company_phone = company_info['phone'] if ('phone' in company_info) else ''
		company_category = company_info['category'] if ('category' in company_info) else ''
		if ('location' not in company_info):
			company_location = ''
		else:	
			company_location = concatenate_facebook_location(company_info['location'])
	
	company_details = {
		'name': company_name,
		'about': company_about,
		'location': company_location,
		'contact_number': company_phone,
		'category': company_category
	}
	print company_details