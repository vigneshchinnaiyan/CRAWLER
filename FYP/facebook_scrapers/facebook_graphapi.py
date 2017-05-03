import facebook
import os
import json

FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')


def facebook_fetch(graph, facebook_id):
    """
    Parameters:
    graph: graph object
    facebook_id: string

    Outputs:
    facebook_company_info: dict
    """

    facebook_company_info = graph.get_object(id=facebook_id, fields='name, about, location, phone, category, description, fan_count, hours, link, call_to_actions')
    if facebook_company_info.has_key("call_to_actions") and facebook_company_info["call_to_actions"].has_key("data"):
        for obj in facebook_company_info["call_to_actions"]["data"]:
            if obj.has_key("type") and obj["type"] == "CALL_NOW":
                facebook_call_now = graph.get_object(id=obj["id"], fields='from,id,intl_number_with_plus,status,type')
                if facebook_call_now.has_key("intl_number_with_plus"):
                    facebook_company_info["intl_number_with_plus"] = facebook_call_now["intl_number_with_plus"]
    facebook_company_info["connections"] = graph.get_connections(id=facebook_id, connection_name='likes')['data']

    return facebook_company_info    


def facebook_parse(fb_id, facebook_company_info):
    """
    Parameters:
    facebook_company_info: dict, from fetcher, using get_object function
    fb_id: string

    Outputs:
    company_info: dict , information of the company
    potential leads: array
    """

    if facebook_company_info:
        company_name = facebook_company_info['name'] if ('name' in facebook_company_info) else None
        company_about = facebook_company_info['about'] if ('about' in facebook_company_info) else None
        company_phone = facebook_company_info['phone'] if ('phone' in facebook_company_info) else None
        company_category = facebook_company_info['category'] if ('category' in facebook_company_info) else None
        company_street = facebook_company_info["location"]['street'] if (facebook_company_info.has_key("location") and facebook_company_info["location"].has_key("street")) else None
        company_longitude = facebook_company_info["location"]['longitude'] if (facebook_company_info.has_key("location") and facebook_company_info["location"].has_key("longitude")) else None
        company_latitude = facebook_company_info["location"]['latitude'] if (facebook_company_info.has_key("location") and facebook_company_info["location"].has_key("latitude")) else None
        company_country = facebook_company_info["location"]['country'] if (facebook_company_info.has_key("location") and facebook_company_info["location"].has_key("country")) else None
        company_postal = facebook_company_info["location"]['zip'] if (facebook_company_info.has_key("location") and facebook_company_info["location"].has_key("zip")) else None
        company_fan_count = facebook_company_info['fan_count'] if ('fan_count' in facebook_company_info) else None
        company_hours = facebook_company_info['hours'] if ('hours' in facebook_company_info) else None
        company_link = facebook_company_info['link'] if ('link' in facebook_company_info) else None
        company_intl_number_with_plus = facebook_company_info['intl_number_with_plus'] if ('intl_number_with_plus' in facebook_company_info) else None

    potential_leads = []

    """
    TODO
    this section
    """
    for companies in facebook_company_info["connections"]:
        potential_leads.append(companies["id"])

    company_info = {
        'org_name': company_name,
        'description': company_about,
        'address': company_street,
        'country': company_country,
        'postal_code': company_postal,
        'contact_no': company_phone,
        'industry': company_category,
        'facebook_resource_locator': fb_id,
        'longitude': company_longitude,
        'latitude': company_latitude,
        'fan_count': company_fan_count,
        'hours': company_hours,
        'link': company_link,
        'intl_number_with_plus': company_intl_number_with_plus
    }

    return company_info, potential_leads


def write_to_json_file(contact, potential_leads):
    f = open('facebook_graph_api_data.json', 'w')
    json.dump(contact, f, indent=4)  
    json.dump(potential_leads, f, indent=4)    


def call_facebook_graph_api():
    """
    Main function of the program
    """
    FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')

    graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
    facebook_id = '10084673031'

    facebook_company_info = facebook_fetch(graph, facebook_id)
    contact, potential_leads = facebook_parse(facebook_id, facebook_company_info)

    write_to_json_file(contact, potential_leads)


if __name__ == "__main__":
    call_facebook_graph_api()