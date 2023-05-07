from crochet import setup, wait_for
from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from backend.olx_scraper.spiders.olx_spider import OLXSpider

# Create Flask app
app = Flask(__name__)
# Configure Crochet for scrapy
# This needs to be done before creating the crawler object
configure_logging()
settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
}
setup()
runner = CrawlerRunner(settings)


# Run the crawler in a blocking manner - this will create a new thread
# and block the current one until the crawling is finished
# This is done to prevent the Flask app from ending the request before the crawling is finished
@wait_for(timeout=300.0)
def run_crawler(filter_start, filters_single_page, scraped_items):
    return runner.crawl(OLXSpider, filter_start=filter_start,
                        filters_single_page=filters_single_page, scraped_items=scraped_items)


# Create comparator based on user sort_by preference
def create_comparator(sort_by):
    def comparator(item):
        result = []
        for key, value in sort_by.items():
            if value == "asc":
                result.append(item[key])
            elif value == "desc":
                result.append(-item[key])
        return tuple(result)

    return comparator


# Get scrapped data from the crawler and return it as a JSON format
def find_best_offers(filters_start, sort_by, filters_single_page):
    scraped_items = []
    for filter_start in filters_start:
        run_crawler(filter_start, filters_single_page, scraped_items)
    # Get the data when the crawling is finished
    output_data = [dict(item) for item in scraped_items]
    # Sort the items by preference
    sorted_result = sorted(output_data, key=create_comparator(sort_by))


# Create a comparator function to sort the items
# It can be changed to sort by different criteria and include more criteria than one
# For example first sort by price and then by area

# Scrape endpoint for the API
@app.route('/scrape', methods=['POST'])
def scrape():
    (filters_start, sort_by, filters_single_page) = request.json
    return find_best_offers(filters_start, sort_by, filters_single_page)


if __name__ == '__main__':
    app.run()
