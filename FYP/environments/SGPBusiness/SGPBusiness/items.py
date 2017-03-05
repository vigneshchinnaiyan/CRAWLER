# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SgpbusinessItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    registration_type = scrapy.Field()
    company_website = scrapy.Field()
