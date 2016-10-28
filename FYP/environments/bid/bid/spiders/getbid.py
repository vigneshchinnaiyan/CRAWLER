# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bid.items import BidItem

class GetbidSpider(CrawlSpider):
    name = 'getbid'
    allowed_domains = ['businessideadaily.com']
    start_urls = ['http://businessideadaily.com/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        href = BidItem()
        href['url'] = response.url
        return href
