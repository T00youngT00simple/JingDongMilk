### 爬虫（初级）
###### 爬取京东进口牛奶信息
##### 1、任务一：爬取商品信息
在商品分类中直接找到进口牛奶分类可看到page1的60条商品条目，虽为动态加载页面，仍可看到商品信息中的商品民称，id，以及详情页链接。
##### 2、任务二：获得商品venderID
在商品的详情页中透过分析页面的js请求可得到加载商家名称以及价格的url，对其原始地址分析后其修改参数为venderID以及商品id，其中venderID可以在页面中通过正则表达式匹配得到。
##### 3、任务三：获得商品商家名称以及价格
解析json串可以得到商家名称以及价格，其中json键值对的键并不固定，分为两种情况。得到评论信息的js请求参数只有商品id。
##### 4、任务四：获得评论数
解析json串可以得到评论数
##### 5、任务五：格式化输出
添加excel数据输出格式
```
scrapy crawl JingDong -t excel -o milk.xls
```
