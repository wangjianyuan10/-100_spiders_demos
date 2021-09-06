import scrapy
from scrapy import FormRequest
from ..items import FashionnovaItem


class FashionnovaSpider(scrapy.Spider):
    name = 'fashionnova'
    allowed_domains = ['www.fashionnova.com']
    # start_urls = ['http://www.fashionnova.com/']

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-algolia-application-id': 'XN5VEPVD4I',
        'x-algolia-api-key': '0e7364c3b87d2ef8f6ab2064f0519abb',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://www.fashionnova.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.fashionnova.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    query_url = 'https://xn5vepvd4i-1.algolianet.com/1/indexes/products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.3.0)%3B%20Browser'


    def start_requests(self):
        page = 0
        data = '{"query":"","userToken":"anonymous-5f4d1d5f-b364-4b54-8a50-1848166f6599","ruleContexts":["all"],"analyticsTags":["all","desktop","Returning","Singapore"],"clickAnalytics":true,"distinct":1,"page":%s,"hitsPerPage":48,"facetFilters":[],"facetingAfterDistinct":true,"attributesToRetrieve":["handle","image","title"],"personalizationImpact":0}'
        data = data % page
        yield FormRequest(self.query_url,callback=self.parse,method='POST',headers=self.headers,body=data,meta={'page':page})


    def parse(self, response):
        page = response.meta['page']
        result = response.json()
        hits = result['hits']
        for hit in hits:
            item = FashionnovaItem()
            item['goods_title'] = hit['title'] 
            item['goods_img_url'] = hit['image']
            item['goods_object_id'] = hit['objectID']
            yield item
        page_count = result['nbPages']
        page = page + 1
        if page < page_count:
            data = '{"query":"","userToken":"anonymous-5f4d1d5f-b364-4b54-8a50-1848166f6599","ruleContexts":["all"],"analyticsTags":["all","desktop","Returning","Singapore"],"clickAnalytics":true,"distinct":1,"page":%s,"hitsPerPage":48,"facetFilters":[],"facetingAfterDistinct":true,"attributesToRetrieve":["handle","image","title"],"personalizationImpact":0}'
            data = data % page
            yield FormRequest(self.query_url,callback=self.parse,method='POST',headers=self.headers,body=data,meta={'page':page},
                    dont_filter=True)
