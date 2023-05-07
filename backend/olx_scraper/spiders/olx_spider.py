import sys

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup

district_ids = {
    'Śródmieście': 351,
    'Mokotów': 353,
    'Ochota': 355,
    'Włochy': 357,
    'Wola': 359,
    'Rembertów': 361,
    'Żoliborz': 363,
    'Białołęka': 365,
    'Bemowo': 367,
    'Bielany': 369,
    'Ursus': 371,
    'Ursynów': 373,
    'Wilanów': 375,
    'Targówek': 377,
    'Praga-Północ': 379,
    'Praga-Południe': 381,
    'Wawer': 383,
    'Wesoła': 533
}


def float_value(value):
    return float(''.join(filter(lambda x: x.isdigit() or x in ['.', ','], value)).replace(',', '.'))


def tile_value(offer_soup, tile_name):
    offer_tiles = offer_soup.find_all('p', class_='css-b5m1rv er34gjf0')
    found_tile = ([p.text for p in offer_tiles if p.text.startswith(tile_name)][0])
    tile_without_name = found_tile.replace(tile_name, '')
    return tile_without_name.replace(',', '.')


def selector_value(class_name, selector, offer_soup):
    return offer_soup.find(selector, class_=class_name).text


class OLXSpider(scrapy.Spider):
    name = 'olx_spider'

    def __init__(self, filter_start, filters_single_page, scraped_items, **kwargs):
        super().__init__(**kwargs)
        self.filter_start = filter_start
        self.filters_single_page = filters_single_page
        self.scraped_items = scraped_items

    def start_requests(self):
        starter = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/"
        surface_min = self.filter_start['surface']['min']
        surface_max = self.filter_start['surface']['max']
        price_min = self.filter_start['price']['min']
        price_max = self.filter_start['price']['max']
        localization = self.filter_start['localization']
        furnished = self.filter_start['furnished']

        if localization:
            starter = f"{starter}?search%5Bdistrict_id%5D={district_ids[localization]}"
        if price_min:
            starter = f"{starter}&search%5Bfilter_float_price:from%5D={price_min}"
        if price_max:
            starter = f"{starter}&search%5Bfilter_float_price:to%5D={price_max}"
        if surface_min:
            starter = f"{starter}&search%5Bfilter_float_m:from%5D={surface_min}"
        if surface_max:
            starter = f"{starter}&search%5Bfilter_float_m:to%5D={surface_max}"
        if furnished:
            starter = f"{starter}&search%5Bfilter_enum_furniture%5D%5B0%5D=yes"
        yield Request(starter, callback=self.parse)

    def parse(self, response, **kwargs):
        # Pobranie diva z wszystkimi ofertami na danej stronie
        offers = response.css('div[data-cy="l-card"]')
        for offer in offers:
            # Pobranie linku do oferty
            link = offer.css('a[class="css-rc5s2u"]::attr(href)').get()
            # Jeżeli link zaczyna się od /d/ jest to relatywny link do oferty na olx.pl
            if not link.startswith('/d/'):
                continue
            # Opcja w której po tej ofercie będą tylko oferty z poza wybranej lokalizacji
            # Powinniśmy wtedy przerwać całkowicie parsowanie następnych stron
            if not link.endswith('html'):
                break
            # Stworzenie linku na podstawie relative url z oferty
            link = f"https://www.olx.pl{link}"
            # Przekazanie linku do funkcji parsującej stronę oferty
            yield Request(link, callback=self.parse_offer_page)

        next_page = response.css('a[data-cy="pagination-forward"]::attr(href)').get()
        if next_page != response.url:
            yield response.follow(next_page, callback=self.parse)

    def is_offer_valid(self, item):
        remove_offers = self.filters_single_page['remove_offers']
        date_min = self.filters_single_page['offer_date']['min']
        date_max = self.filters_single_page['offer_date']['max']
        price_min = self.filters_single_page['full_price']['min']
        price_max = self.filters_single_page['full_price']['max']
        surface_min = self.filters_single_page['surface']['min']
        surface_max = self.filters_single_page['surface']['max']

        if remove_offers and item['offer_url'] in remove_offers:
            return False
        if date_min and item['offer_date'] < date_min:
            return False
        if date_max and item['offer_date'] > date_max:
            return False
        if price_min and item['full_price'] < price_min:
            return False
        if price_max and item['full_price'] > price_max:
            return False
        if surface_min and item['surface'] < surface_min:
            return False
        if surface_max and item['surface'] > surface_max:
            return False
        return True

    def parse_offer_page(self, response):
        def surface():
            return float_value(tile_value(offer_soup, 'Powierzchnia: '))

        def full_price():
            rent_price = float_value(tile_value(offer_soup, 'Czynsz (dodatkowo): '))
            flat_price = float_value(selector_value('h3', 'css-ddweki er34gjf0', offer_soup))
            return rent_price + flat_price - 1

        def offer_date():
            return selector_value('span', 'css-19yf5ek', offer_soup)

        item = dict()
        offer_url = response.url
        offer_soup = BeautifulSoup(response.text, 'html.parser')

        try:
            item['surface'] = surface()
            item['full_price'] = full_price()
            item['offer_url'] = offer_url
            item['offer_date'] = offer_date()
        # Catching exception if anything goes wrong
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_msg = f"Error while parsing offer {offer_url}: {e}\n{exc_traceback}"
            self.logger.error(error_msg)

        if self.is_offer_valid(item):
            # There we will create a new item for each offer
            self.scraped_items.append(item)
            yield
