import scrapy


class OLXOfferItem(scrapy.Item):
    link = scrapy.Field()
    full_price = scrapy.Field()
    surface = scrapy.Field()
    photos = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
