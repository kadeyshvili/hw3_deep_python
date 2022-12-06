import scrapy
from spider_steam.items import SpiderSteamItem


class SteamproductspiderSpider(scrapy.Spider):
    name = 'SteamProductSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = [
        'https://store.steampowered.com/search/?g=n&SearchText=indie&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=indie&page=2',
        'https://store.steampowered.com/search/?g=n&SearchText=strategy&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=strategy&page=2',
        'https://store.steampowered.com/search/?g=n&SearchText=adventure&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=adventure&page=2']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, response):
        games = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for link in games:
            if 'agecheck' not in link:
                yield scrapy.Request(link, callback=self.parse_for_game)

    def parse_for_game(self, response):
        items = SpiderSteamItem()
        product_name = response.xpath('//span[@itemprop="name"]/text()').extract()
        product_category = response.xpath('//span[@data-panel]/a/text()').extract()
        product_number_of_reviews = response.xpath('//span[@class = "responsive_reviewdesc_short"]/text()').extract()
        product_date_of_reliase = response.xpath('//div[@class="date"]/text()').extract()
        product_developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        product_tags = response.xpath('//a[@class="app_tag"]/text()').extract()
        product_price = response.xpath('//div[@class="game_purchase_price price"]/text()')[0].extract()

        product_date_of_reliase = ''.join(product_date_of_reliase).strip()
        platforms = set()
        for platform in response.css('div').xpath('@data-os'):
            platforms.add(platform.get().strip())

        if product_name != '' and product_date_of_reliase > '2000':
            items['product_name'] = ''.join(product_name).strip().replace('™', '')
            items['product_category'] = ', '.join(product_category).strip()
            items['product_number_of_reviews'] = items['product_number_of_reviews'] = ', '.join(
                map(lambda x: x.strip(), product_number_of_reviews)).strip().replace('(', '').replace(')', '')
            items['product_date_of_reliase'] = ''.join(product_date_of_reliase).strip()
            items['product_developer'] = ', '.join(map(lambda x: x.strip(), product_developer)).strip()
            items['product_tags'] = ', '.join(map(lambda x: x.strip(), product_tags)).strip()
            items['product_price'] = ''.join(product_price).strip().replace('уб', '')
            items['product_platforms'] = list(platforms)
        yield items
