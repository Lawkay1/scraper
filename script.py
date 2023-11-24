import sys
from scrapy.crawler import CrawlerProcess
import scrapy

class QuoraSpider(scrapy.Spider):
    name = 'quora'

    def parse(self, response):
        h1_tags = response.css('h1::text').getall()
        h2_tags = response.css('h2::text').getall()

        yield {
            'url': response.url,
            'h1_tags': h1_tags,
            'h2_tags': h2_tags
        }

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': sys.argv[sys.argv.index('--output') + 1],
        'RETRY_TIMES' : 3,  # Retry a failed request up to 3 times
        'RETRY_HTTP_CODES' : [429] , # Retry on HTTP 429 responses
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    })

    # Add your URLs to scrape
    start_urls = sys.argv[sys.argv.index('--urls') + 1].split(',')
    process.crawl(QuoraSpider, start_urls=start_urls)
    process.start()
