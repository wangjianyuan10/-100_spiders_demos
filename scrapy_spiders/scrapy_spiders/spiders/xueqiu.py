import scrapy
from scrapy import Request
from urllib.parse import urlencode
from ..items import XueqiuItem
class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?'
    top_rank = 100
    cookies = {
            'acw_tc': '2760826716305686015054271e891195c601cf7b07472077e71fffcff67b75',
            's': 'cj126vsv70',
            'xq_a_token': '6f2a74dcaf567c87c45208248c683353242d4781',
            'xq_r_token': 'e67040a2f1e5303a2266b2483d501c3bb806b337',
            'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYzMTk4NjEwMiwiY3RtIjoxNjMwNTY4NTY4MjEwLCJjaWQiOiJkOWQwbjRBWnVwIn0.A0cN-NJc2Y7zpEQYiH1ZNA_DbWEmxexX803VZXxtHa_Eg4tbLqu6b-ApO33tdcJ-FbyDECIOOLZOEB7oYeR2Co-jGxajgOgQszUtu1V4v1a-ddvXPyLUTDDSndSQ1vwiPogAYBR8M4bwoJ5GJgTKmbVkZcW_R2jgVqWPAvJObm2FdEK0MEEsz8YGmjhJnT5MAQZNWuHQ3g6h5jm-JG7g9aMoBiloHlbb6gXFSktWmv4anl9CNPII2ihJSIZCmTtnVgwXyrByrhk0Gjgg6rO0zeNpg8pLv2ysv4wOnpVhFNQON3cclBfeRBYZPzMWX9H0GW_fmKOpWZY9OTw3GwdSgQ',
            'u': '591630568602539',
            'device_id': '6695cc470b956bbca010e55c107ba9e1',
            'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1630568603',
            '__utma': '1.1317222602.1630568603.1630568603.1630568603.1',
            '__utmc': '1',
            '__utmz': '1.1630568603.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '__utmt': '1',
            'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1630569042',
            '__utmb': '1.2.10.1630568603',
        }

    headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': '*/*',
            'cache-control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://xueqiu.com/hq',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }


    def start_requests(self):

        params = (
            ('page', '1'),
            ('size', '90'),
            ('order', 'desc'),
            ('orderby', 'percent'),
            ('order_by', 'percent'),
            ('market', 'US'),
            ('type', 'us'),
        )

        yield Request(''.join((self.start_url, urlencode(params))), headers=self.headers,cookies=self.cookies, meta={'page':1})
    def parse(self,response):
        page = response.meta['page']
        data = response.json()
        for stock  in data.get('data',{}).get('list',[]):
            item = XueqiuItem()
            item['stock_name'] = stock['name']
            item['stock_code'] = stock['symbol']
            item['stock_price'] = stock['current']
            item['stock_daily_return'] = stock['percent']
            item['stock_market_value'] = stock['market_capital']
            item['stock_TTM'] = stock['pe_ttm']
            if self.top_rank>0:
                yield item
            self.top_rank = self.top_rank - 1

        if self.top_rank > 0:
            page = page + 1
            params = (
                ('page', str(page)),
                ('size', '90'),
                ('order', 'desc'),
                ('orderby', 'percent'),
                ('order_by', 'percent'),
                ('market', 'US'),
                ('type', 'us'),
            )
            yield Request(''.join((self.start_url, urlencode(params))), headers=self.headers,cookies=self.cookies, meta={'page':1})
