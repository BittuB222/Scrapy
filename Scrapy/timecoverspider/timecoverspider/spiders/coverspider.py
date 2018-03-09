# -*- coding: utf-8 -*-
# import the necessary packages
from timecoverspider.items import MagazineCover
import datetime
import scrapy
import traceback
 
class CoverSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ["http://brickset.com/sets/year-2016"]

    def parse(self, response):
        try:
            SET_SELECTOR = '.set'
            for brickset in response.css(SET_SELECTOR):
                NAME_SELECTOR = 'h1 a ::text'
                PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
                MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
                IMAGE_SELECTOR = 'img ::attr(src)'
                yield {
                    'name': brickset.css(NAME_SELECTOR).extract_first(),
                    'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                    'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                    'image': brickset.css(IMAGE_SELECTOR).extract_first(),
                }
            NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page),callback=self.parse)
        except Exception as e:
            print str(e)
            formatted_lines = traceback.format_exc().splitlines()
            print formatted_lines