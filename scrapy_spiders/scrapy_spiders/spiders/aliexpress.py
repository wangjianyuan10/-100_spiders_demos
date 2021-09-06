import scrapy
from scrapy import Request
import re
import json
from ..items import AliexpressItem
# import pyperclip
from urllib.parse import urljoin, urlencode


class AliexpressSpider(scrapy.Spider):
    name = 'aliexpress'
    allowed_domains = ['www.aliexpress.com']
    query_url = 'https://www.aliexpress.com/wholesale?SearchText='


    def __init__(self, keyword='hat', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword

    def start_requests(self):
        page  = 1
        yield Request(self.query_url+self.keyword,callback = self.parse, meta = {'page':1})


    def parse(self, response):
        page = response.meta['page']
        text = response.text
        goods_json = re.search(
            'window.runParams = \{\};\s*?window.runParams =\s*?(\{.*?});\s*?window.runParams.csrfToken', text).group(1)
        # pyperclip.copy(goods_json)
        goods = json.loads(goods_json)
        total_goods_num = goods['resultCount']
        size = goods['resultSizePerPage']
        goodlist = goods['mods']['itemList']['content']
        for good in goodlist:
            item = AliexpressItem()
            item['goods_title'] = good['title']['displayTitle']
            item['goods_img_url'] = urljoin(response.url , good['image']['imgUrl'] )
            compare_fileds = dict([field.split(':') for field in good['trace']['pdpParams']['compareFields'].split(';')])
            item['goods_price'] = compare_fileds['formatted_price']
            try:
                item['goods_order_num'] = int(compare_fileds['trade_order'])
            except:
                item['goods_order_num'] = 0
            try:
                item['goods_comment_star'] = good['evaluation']['starRating']
            except:
                item['goods_comment_star'] = 0

            yield item
        if page * size < total_goods_num:
            page = page + 1
            params = {
                'trafficChannel': 'main',
                'd' : 'y',
                'CatId': '0',
                'ltype': 'wholesale',
                'SearchText':self.keyword,
                'SortType': 'default',
                'page': str(page)
            }
            yield Request(url=response.url.split('?')[0]+'?'+urlencode(params), 
                    callback=self.parse, meta={'page': page, })


