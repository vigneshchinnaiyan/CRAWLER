from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep
import sys
 
extracted_data = [] 
visited_urls = set()

def linkedin_companies_parser(url, companyurls):
    for i in range(5):
        try:
            headers = {
            #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
            'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"
            }
            sleep(3)
            response = requests.get(url, headers=headers)
            #response = requests.get(url)
            formatted_response = response.content.replace('<!--', '').replace('-->', '')
            doc = html.fromstring(formatted_response)
            print response
            # f_2 = open('response.txt', 'w')
            # f_2.write(response.content)
            # f_2.close() 

            # we obtain urls to other 
            if response.status_code == 200:
                other_companies_link = doc.xpath('//code[@id="stream-right-rail-embed-id-content"]//text()')
                other_companies_data = json.loads(other_companies_link[0])
                also_viewed = other_companies_data['alsoViewed']
                for other_company in also_viewed:
                    companyurls.append(other_company["homeUrl"])

            # print(doc.text_content())
            datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
            # print(datafrom_xpath)
            if datafrom_xpath:
                try:
                    json_formatted_data = json.loads(datafrom_xpath[0])
                    company_name = json_formatted_data['companyName'] if 'companyName' in json_formatted_data.keys() else None
                    size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else None
                    industry = json_formatted_data['industry'] if 'industry' in json_formatted_data.keys() else None
                    description = json_formatted_data['description'] if 'description' in json_formatted_data.keys() else None
                    follower_count = json_formatted_data['followerCount'] if 'followerCount' in json_formatted_data.keys() else None
                    year_founded = json_formatted_data['yearFounded'] if 'yearFounded' in json_formatted_data.keys() else None
                    website = json_formatted_data['website'] if 'website' in json_formatted_data.keys() else None
                    type = json_formatted_data['companyType'] if 'companyType' in json_formatted_data.keys() else None
                    specialities = json_formatted_data['specialties'] if 'specialties' in json_formatted_data.keys() else None

                    if "headquarters" in json_formatted_data.keys():
                        city = json_formatted_data["headquarters"]['city'] if 'city' in json_formatted_data["headquarters"].keys() else None
                        country = json_formatted_data["headquarters"]['country'] if 'country' in json_formatted_data['headquarters'].keys() else None
                        state = json_formatted_data["headquarters"]['state'] if 'state' in json_formatted_data['headquarters'].keys() else None
                        street1 = json_formatted_data["headquarters"]['street1'] if 'street1' in json_formatted_data['headquarters'].keys() else None
                        street2 = json_formatted_data["headquarters"]['street2'] if 'street2' in json_formatted_data['headquarters'].keys() else None
                        zip = json_formatted_data["headquarters"]['zip'] if 'zip' in json_formatted_data['headquarters'].keys() else None
                        street = street1 + ', ' + street2
                    else:
                        city = None
                        country = None
                        state = None
                        street1 = None
                        street2 = None
                        street = None
                        zip = None

                    data = {
                                'company_name': company_name,
                                'size': size,
                                'industry': industry,
                                'description': description,
                                'follower_count': follower_count,
                                'founded': year_founded,
                                'website': website,
                                'type': type,
                                'specialities': specialities,
                                'city': city,
                                'country': country,
                                'state': state,
                                'street': street,
                                'zip': zip,
                                'url': url
                            }
                    # other_companies_link = doc.xpath('//ul[contains(@class,"org-similar-companies-module__company-list)')
                    # print other_companies_link          
                    return data
                except:
                    print "cant parse page", url

                other_companies_link = doc.xpath('//ul[contains(@class,"org-similar-companies-module__company-list)')
                print other_companies_link    
 
            # Retry in case of captcha or login page redirection
            if len(response.content) < 2000 or "trk=login_reg_redirect" in url:
                if response.status_code == 404:
                    print "linkedin page not found"
                else:
                    raise ValueError('redirecting to login page or captcha found')
        
        except KeyboardInterrupt:
            f = open('data.json', 'w')
            json.dump(extracted_data, f, indent=4)  
            sys.exit()
                    
        except :
            print "retrying :",url
 
def readurls():
    companyurls = ['https://www.linkedin.com/company/itaubba']

    while companyurls:
        try:
            if companyurls[0] not in visited_urls:

                # before parsing we add to visited_urls to check that we don't duplicate the
                # URL
                visited_urls.add(companyurls[0])
                extracted_data.append(linkedin_companies_parser(companyurls.pop(0), companyurls))
                sleep(5)

            else:
                companyurls.pop(0)
                continue    
        except KeyboardInterrupt:
            f = open('data.json', 'w')
            json.dump(extracted_data, f, indent=4)        
            sys.exit()
 
if __name__ == "__main__":
    readurls()