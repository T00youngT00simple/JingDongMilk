import scrapy
from scrapy import Selector
from JingDong_Milk.items import JingdongMilkItem
import json
import re
import logging
class milk_spider(scrapy.Spider):
    name = 'JingDong'
    start_urls = ['https://list.jd.com/list.html?cat=1320,5019,12215']

    #在商品列表页面上获得商品名称、id以及详情页链接
    def parse(self,response):
        sel = Selector(response)
        milks = sel.xpath('//li[@class="gl-item"]')
        for milk in milks:
            item1 = JingdongMilkItem()
            item1['ID'] = milk.xpath('./div/@data-sku').extract()
            item1['name'] = milk.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
            #item1['shop_name'] = milk.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract()
            item1['link'] = milk.xpath('./div/div[@class="p-img"]/a/@href').extract()
            url = "http:" + item1['link'][0]
            yield scrapy.Request(url = url,meta= {'item':item1} ,callback= self.parse_detail)

    #在详情页上获得商品venderID
    def parse_detail(self,response):
        item1 = response.meta['item']
        ids = re.findall(r"venderId:(.*?),\s.*?shopId:'(.*?)'", response.text)
        if not ids:
            ids = re.findall(r"venderId:(.*?),\s.*?shopId:(.*?),", response.text)
        vender_id = '&venderId='+ids[0][0]
        skuId = 'skuId=' + str(item1['ID'][0])
        getShopnameandPrice_url = 'http://c0.3.cn/stock?'+skuId+'&cat=1320,5019,12215'+vender_id+'&area=5_274_49707_0'
        yield scrapy.Request(url = getShopnameandPrice_url ,meta={'item': item1},callback= self.parse_getShopnameandPrice)

    #根据verderID以及商品ID获得商家民称以及价格的js请求url，解析json
    def parse_getShopnameandPrice(self,response):
        item1 = response.meta['item']
        js = json.loads(response.body.decode('gbk'))
        if js['stock'].get('self_D'):          #json键值对的键有两种
            item1['shop_name']= js['stock']['self_D']['vender']
        else:
            item1['shop_name'] = js['stock']['D']['vender']
        item1['price'] = js['stock']['jdPrice']['p']
        getComment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='+ str(item1['ID'][0])
        yield scrapy.Request(url =getComment_url,meta= {'item':item1},callback= self.parse_getComment)

    # 根据商品ID获得评价js请求url，解析json
    def parse_getComment(self,response):
        item1 = response.meta['item']
        js = json.loads(response.body.decode('gbk'))
        item1['CommentsCount'] = js['CommentsCount'][0]['CommentCount']
        item1['GoodCount'] = js['CommentsCount'][0]['GoodCount']
        item1['GeneralCount'] = js['CommentsCount'][0]['GeneralCount']
        item1['PoorCount'] = js['CommentsCount'][0]['PoorCount']
        item1['AfterCount'] = js['CommentsCount'][0]['AfterCount']
        return item1



