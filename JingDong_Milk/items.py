# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongMilkItem(scrapy.Item):
    # define the fields for your item here like:
    ID = scrapy.Field()
    name = scrapy.Field()
    shop_name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    CommentsCount = scrapy.Field()
    GoodCount = scrapy.Field()
    GeneralCount =scrapy.Field()
    PoorCount =scrapy.Field()
    AfterCount =scrapy.Field()
    pass
