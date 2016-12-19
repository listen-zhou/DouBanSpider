# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from bs4 import BeautifulSoup

from DouBanSpider.items import DoubanTop250MovieItem


class DoubanTop250MovieSpider(CrawlSpider):
    name = 'DouBanSpider'
    redis_key = 'douban:start_urls'
    start_urls = ['https://movie.douban.com/top250']

    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanTop250MovieItem()
        body = response.body
        soup = BeautifulSoup(body, 'html.parser')
        with open('movie-1.html', 'w') as f:
            f.write(soup.prettify())
        Movies = soup.find_all('div', 'info')
        for eachMovie in Movies:
            info = eachMovie
            hd = info.find('div', 'hd')
            a = hd.find('a')
            href = a['href']
            titles = a.find_all('span')
            name = ";".join([tit.get_text().strip() for tit in titles])
            bd = info.find('div', 'bd')
            direct = bd.find('p', '').get_text().strip()
            stars = bd.find('div', 'star').find_all('span')
            star = stars[1].get_text().strip() + '/' + stars[2]['content'].strip() + ';' + stars[3].get_text().strip()
            quote = bd.find('p', 'quote')
            if quote:
                inq = quote.find('span', 'inq')
                if inq:
                    quote = inq.get_text().strip()

            item['href'] = href
            item['name'] = name
            item['direct'] = direct
            item['star'] = star
            item['quote'] = quote
            # print item
            yield item

        nextLink = soup.find('span', class_='next')
        if nextLink:
            nextLink = nextLink.find('link')
            if nextLink:
                nextLink = nextLink['href']
                nextLink = self.url + nextLink
                print '############:' + nextLink
                yield Request(nextLink, callback=self.parse)
