import scrapy

from linkedInScraper.items import LinkedinscraperItem

class linkedInSpider(scrapy.Spider):
	name = 'linkedIn'
	handle_httpstatus_list = [999]
	allowed_domains = ['linkedin.com']
	start_urls = [
		"https://www.linkedin.com/company/great-eastern-life",
	] 

	def parse(self, response):
		item = LinkedinscraperItem()
		item['company_website'] = response.xpath('/div[@class="basic-info-about"]/ul/li[@class="website"]/p/a/@href').extract()
		item['company_location'] = response.xpath('/div[@class="basic-info-about"]/ul/li[@class="vcard hq"]/p//span/text()').extract()
		print item
		yield item


