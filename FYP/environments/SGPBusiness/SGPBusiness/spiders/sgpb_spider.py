import scrapy
from bs4 import BeautifulSoup
from SGPBusiness.items import SgpbusinessItem
import sys

class SGPBSpider(scrapy.Spider):
	name = "SGPB"
	allowed_domains = ["sgpbusiness.com"]
	start_urls = [
		"https://www.sgpbusiness.com/company/Great-Eastern-Holdings-Limited"
	]

	#parsed_pages = 0

	def get_address(self, response):
		address_string = ''
		for address_line in response.xpath("//div[contains(concat(' ', normalize-space(@class),' '),' list-group-item ')]/div[contains(@itemprop, 'address')]//span").extract():
			#address_line = address_line.replace("\n", " ")
			address_line = BeautifulSoup(address_line, "lxml")
			address_line = address_line.text.replace("\n", " ").strip() + ", "
			address_string = address_string + address_line
		address_string = address_string.strip().strip(",")
		
		return address_string	


	def get_next_urls(self, response):
		next_urls = []
		for url_string in response.xpath("//h4[contains(@class, 'panel-title')][./text()=' EXPLORE']/parent::*/following-sibling::div//a//@href").extract():
			next_urls.append(url_string)	

		return next_urls


	def parse(self, response):
		# filename = response.url.split("/")[-2] + '.html'
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)
		#
		# parsed_pages = parsed_pages + 1

		# if parsed_pages == 5:
		# 	sys.exit()
		item = SgpbusinessItem()
		item["company_name"] = response.xpath("//div[contains(concat(' ', normalize-space(@class),' '),' list-group-item ')]/div[./text()='Name']/following-sibling::div/child::node()/text()").extract_first()
		item["company_website"] = response.xpath("//div[contains(concat(' ', normalize-space(@class),' '),' list-group-item ')]/div[./text()='Name']/following-sibling::div/child::node()/@href").extract_first()
		item["registration_type"] = response.xpath("//div[contains(concat(' ', normalize-space(@class),' '),' list-group-item ')]/div[./text()='Registration Type']/following-sibling::div/text()").extract_first()
		item["company_address"] = self.get_address(response)

		next_urls = self.get_next_urls(response)

		if len(next_urls) > 0:
			for next_url in next_urls:
				#print str(next_url)

				yield scrapy.Request(next_url, callback=self.parse)
		print "\n=== COMPANY INFO ==== \n"
		yield item
