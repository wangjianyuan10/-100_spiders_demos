# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy




class XueqiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    stock_price = scrapy.Field()
    stock_daily_return = scrapy.Field()
    stock_market_value = scrapy.Field()
    stock_TTM = scrapy.Field()

class AliexpressItem(scrapy.Item):
    goods_title = scrapy.Field()
    goods_img_url = scrapy.Field()
    goods_price = scrapy.Field()
    goods_comment_star = scrapy.Field()
    goods_order_num = scrapy.Field()

class FashionnovaItem(scrapy.Item):
    goods_title = scrapy.Field()
    goods_img_url = scrapy.Field()
    goods_object_id = scrapy.Field()
