import scrapy


class SpiderSteamItem(scrapy.Item):
    product_name = scrapy.Field()
    product_category = scrapy.Field()
    product_number_of_reviews = scrapy.Field()
    product_date_of_reliase = scrapy.Field()
    product_developer = scrapy.Field()
    product_tags = scrapy.Field()
    product_price = scrapy.Field()
