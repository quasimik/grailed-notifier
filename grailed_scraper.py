import scrapy
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime

GRAILED_URL = 'https://www.grailed.com'
GRAILED_SHOP_URL = GRAILED_URL + '/shop'

class GrailedScraper():

  def __init__(self, query_ids):
    self.query_ids = query_ids

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    self.driver = webdriver.Firefox(firefox_options=options)
  
  def __del__(self):
    self.driver.quit()

  def get_queries(self):
    for query_id in self.query_ids:

      # load URL in selenium webdriver
      url = GRAILED_SHOP_URL + query_id
      self.driver.get(url)
      WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'feed-item')))
      response = scrapy.http.HtmlResponse(url=self.driver.current_url, 
                                          body=self.driver.page_source, 
                                          encoding='utf-8')

      # build return dict
      now = datetime.now()
      refinements = [label.get() for label in response.css('.-refinement-label::text')]
      items = [item for item in self.get_items(response)]
      yield {
        'timestamp': now.timestamp(),
        'datetime_str': now.strftime('%x %X'),
        'query_id': query_id,
        'refinements': refinements,
        'items': items,
      }

  def get_items(self, response):
    for item in response.css('div.feed-item'):
      new_price = item.css('p.new-price span::text')
      original_price = item.css('p.original-price span::text')
      price = new_price.get() if new_price else original_price.get()
      yield {
        'url': GRAILED_URL + item.css('a::attr(href)').get(),
        'img_url': item.css('img::attr(src)').get(),
        'designer': item.css('p.listing-designer::text').get(),
        'size': item.css('p.listing-size::text').get(),
        'title': item.css('div.listing-metadata div.truncate::text').get(),
        'price': price,
      }

with open('query_ids.json', 'r') as file:
  query_ids = json.load(file)
s = GrailedScraper(query_ids)
for query in s.get_queries():
  with open('out/out-' + query['query_id'] + '.json', 'w') as file:
    json.dump(query, file)
