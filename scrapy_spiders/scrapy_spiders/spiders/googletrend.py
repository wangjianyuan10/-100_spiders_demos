import scrapy
from scrapy import Request , FormRequest
from urllib.parse import urljoin, urlencode
import json
import chompjs


class GoogletrendSpider(scrapy.Spider):
    name = 'googletrend'
    allowed_domains = ['trends.google.com']
    start_urls = ['https://trends.google.com/trends/explore?q=hat&geo=CN']
    token_url = 'https://trends.google.com/trends/api/explore?'
    trend_url =  'https://trends.google.com/trends/api/widgetdata/multiline?'
    headers = {
            'authority': 'trends.google.com',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'x-client-data': 'CJC2yQEIo7bJAQjEtskBCKmdygEIi/3KAQiMnssBCKegywEI8PDLAQis8ssBCNzyywEI8PLLAQjv98sBCLT4ywEInvnLAQiv+ssBCLH6ywEYuvLLARiQ9csB',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://trends.google.com/trends/explore?q=hat&geo=CN',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '__utmz=10102256.1626429382.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=10102256.343699485.1626429382.1626949297.1627024060.4; __utmc=10102256; __utmt=1; __utmb=10102256.1.10.1627024060; HSID=AzbAhLGjWNBnaeSg5; SSID=AbCtluR_Fke88ijZ_; APISID=wWv3y4ORv3Nfei-i/AC3BTttxU99t5IOQA; SAPISID=M7WAvaTw62jm9rCx/AJOFjbbTIM353MMbT; __Secure-3PAPISID=M7WAvaTw62jm9rCx/AJOFjbbTIM353MMbT; SEARCH_SAMESITE=CgQIr5IB; SID=_Ac1s4eJ00tERsfuV7j4h9BIM-7q_eSR5ITGiKPDHuYhMe-vqqWO-BsPjem9iahGfYugXw.; __Secure-3PSID=_Ac1s4eJ00tERsfuV7j4h9BIM-7q_eSR5ITGiKPDHuYhMe-vaU1E9dNhztOYYpMT0xNdIw.; 1P_JAR=2021-07-23-03; NID=219=o5ojNMPZk-VDvmoEpRCGbhARHKeFUd7SUI8jV5feTLZSHZ1jZYzDbaPOfyZQyfd1H3_HQbdaSwZNNdmrUh6jDYFGLL_KLeaGxXJpDtH-JFH9DYWMDoV8MxaaOTaIcNAyvSA5n92HF-txYfkbmjK7EZJpgLzhhk84QTNCcSSi-7Wzx2bc34X45sKe3MGVLGEREFhLWpaUtKBAvNhLwg7ndhrPjGe90jpNpyTeIy4XkJBdGGB-SZWDWtWrOPtl3WEHl8HoIXI5; SIDCC=AJi4QfGxAl6XeAfEqVwTUQEK5YprfGuMyvM0wz3HaXJntjSPk5owPm0f_LongSeWD5NJzwglXg; __Secure-3PSIDCC=AJi4QfGAtKHhFIhaNqN72X4V93Ra39nFF4CFzZ84xOoITLIUvD6Sn0R3zLq9c5zhYcpZNMv7Bw',
        }

    def __init__(self, keywords='hat',geo='CN' ,resolution='WEEK',*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords.split(',')
        self.geo = geo
        self.resolution = resolution
    def parse(self, response):
        """
        获取 token
        """

        req = {"comparisonItem": [{"keyword": keyword, "geo": self.geo, "time": "today 12-m"} for keyword in self.keywords],
               "category": 0,
               "property": ""
               }

        params = (
            ('hl', 'zh-CN'),
            ('tz', '-480'),
            ('req', json.dumps(req)),
        )
        params = urlencode(params)
        yield Request(self.token_url+params,callback = self.parse_token, headers = self.headers)
    def parse_token(self, response):

        # print(unquote(response.url))
        token = chompjs.parse_js_object(response.text)[
            'widgets'][0]['token']
        print(token)
        time_duration = chompjs.parse_js_object(response.text)[
            'widgets'][0]['request']['time']
        print(time_duration)
        
        start_date , end_date = time_duration.split()
        req = {
            "time": f"{start_date} {end_date}",
                "resolution": self.resolution,
                "locale": "zh-CN",
                "comparisonItem": [{"geo": {"country": self.geo}, "complexKeywordsRestriction": {"keyword": [{"type": "BROAD", "value": keyword}]}}
                                   for keyword in self.keywords],
                "requestOptions": {"property": "", "backend": "IZG", "category": 0}
        }
        # return token, time_duration 
        params = (
            ('hl', 'zh-CN'),
            ('tz',  '-480'),
            ('req', json.dumps(req)),
            ('token', token),
        )
        yield Request(self.trend_url+urlencode(params),callback = self.parse_trend,headers = self.headers )
    def parse_trend(self, response):
        text = response.text
        data_list = chompjs.parse_js_object(text)['default']['timelineData']
        for data in data_list:
            yield data
        
