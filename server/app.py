from crochet import setup, wait_for
from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from olx_scraper.spiders.olx_spider import OLXSpider

app = Flask(__name__)
configure_logging()
settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
}
setup()
runner = CrawlerRunner(settings)


@wait_for(timeout=300.0)
def run_crawler(parameters, items):
    return runner.crawl(OLXSpider, url=parameters['url'], max_price=parameters['max_price'], scraped_items=items)


@app.route('/scrape', methods=['POST'])
def scrape():
    scraped_items = []
    data = request.json
    run_crawler(data, scraped_items)
    json_data = [dict(item) for item in scraped_items]
    return jsonify(json_data)


if __name__ == '__main__':
    app.run()
