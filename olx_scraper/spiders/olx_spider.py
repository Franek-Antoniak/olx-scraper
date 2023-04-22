import sys

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from ..items import OLXOfferItem


class OLXSpider(scrapy.Spider):
    name = 'olx_spider'

    def __init__(self, url, max_price, scraped_items, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.max_price = int(max_price)
        self.scraped_items = scraped_items

    def start_requests(self):
        yield Request(self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        offers = response.css('div[data-cy="l-card"]')

        for offer in offers:
            link = offer.css('a[class="css-rc5s2u"]::attr(href)').get()
            if not link.startswith('/d/'):
                continue
            if not link.endswith('html'):
                break
            link = f"https://www.olx.pl{link}"
            yield Request(link, callback=self.parse_offer_page)

        next_page = response.css('a[data-cy="pagination-forward"]::attr(href)').get()
        if next_page != response.url:
            yield response.follow(next_page, callback=self.parse)

    def find_full_price(self, offer_soup):
        price_text = offer_soup.find('h3', class_='css-ddweki er34gjf0').text
        price = float(''.join(filter(lambda x: x.isdigit() or x in ['.', ','], price_text)).replace(',', '.'))
        rent_text = self.get_tile_value(offer_soup, 'Czynsz (dodatkowo): ')
        rent = float(''.join(filter(lambda x: x.isdigit() or x in ['.', ','], rent_text)).replace(',', '.'))
        return price + (0 if rent == 1 else rent)

    def get_tile_value(self, offer_soup, tile_name):
        offer_tiles = offer_soup.find_all('p', class_='css-b5m1rv er34gjf0')
        return (''.join([p.text for p in offer_tiles if p.text.startswith(tile_name)][0]).replace(',', '.')).replace(
            tile_name, '')

    def parse_offer_page(self, response):
        link = response.url
        offer_html = response.text
        offer_soup = BeautifulSoup(offer_html, 'html.parser')

        try:
            total_price = self.find_full_price(offer_soup)
            surface = self.get_tile_value(offer_soup, 'Powierzchnia: ')
            photos = [photo['src'] for photo in offer_soup.find_all('img', class_='css-1bmvjcs')]
            date = offer_soup.find('span', class_='css-19yf5ek').text
            description = offer_soup.find('div', class_='css-bgzo2k er34gjf0').text
            title = offer_soup.find('h1', class_='css-1soizd2 er34gjf0').text

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_msg = f"Error while parsing offer {link}: {e}\n{exc_traceback}"
            self.logger.error(error_msg)
            return

        if total_price <= self.max_price:
            item = OLXOfferItem()
            item['link'] = link
            item['full_price'] = total_price
            item['surface'] = surface
            item['photos'] = photos
            item['date'] = date
            item['description'] = description
            item['title'] = title
            self.scraped_items.append(item)
            yield
