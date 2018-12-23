# -*- coding: utf-8 -*-
import scrapy
import re
from Jisho.items import KanjiItem, KanjiReadingItem

class KanjiSpider(scrapy.Spider):
    name = 'kanji'
    allowed_domains = ['jisho.org']
    start_urls = [
        'https://jisho.org/search/%23jlpt-n5%20%23kanji',
        'https://jisho.org/search/%23jlpt-n4%20%23kanji',
        'https://jisho.org/search/%23jlpt-n3%20%23kanji',
        'https://jisho.org/search/%23jlpt-n2%20%23kanji',
        'https://jisho.org/search/%23jlpt-n1%20%23kanji',

    ]
    custom_settings = {
        'FEED_URI': "kanji_full.json"
    }

    def parse(self, response):
        #follow details link
        for href in response.xpath('//a[contains(@class, "details_link")]/@href'):
            yield response.follow(href, self.parse_kanji)

        #follow pagination link
        for href in response.xpath('//a[@class="more"]/@href'):
            yield response.follow(href, self.parse)

    def parse_kanji(self, response):

        # PART 1: Scrapy KanjiItem

        Kanji = KanjiItem()
        Kanji['level'] = response.xpath('//div[@class="jlpt"]/strong/text()').extract_first()
        Kanji['kanji'] = response.xpath('//h1[@class="character"]/text()').extract_first()
        Kanji['english'] = [kanji.strip() for kanji in ''.join(response.xpath('//div[contains(@class, "details__main-meanings")]/text()').extract()).split(',')]
        Kanji['kun'] = response.xpath('//div[contains(@class, "readings")]/dl[contains(@class, "kun_yomi")]/dd/a/text()').extract()
        Kanji['on'] = response.xpath('//div[contains(@class, "readings")]/dl[contains(@class, "on_yomi")]/dd/a/text()').extract()
        Kanji['stroke'] = response.xpath('//div[contains(@class, "stroke_count")]/strong/text()').extract_first()
        Kanji['radical'] = [radical.strip() for radical in response.xpath('//div[@class="radicals"]/dl/dd/span/span/text()').extract_first().split(',')]
        Kanji['on_reading'], Kanji['kun_reading'] = self.process_reading_compound(response.xpath('//div[@class="row compounds"]/div'))
        
        yield Kanji

        # PART 2: Scrap KanjiReadingItem

        # e.g: https://jisho.org/search/*%E5%A4%A7*%20%23jlpt-n5
        url = 'https://jisho.org/search/*' + Kanji['kanji'] + '*%20%23jlpt-' + Kanji['level'].lower()
        
        yield scrapy.Request(url=url, callback=self.parse_kanjireading, meta={'level': Kanji['level']})

    def parse_kanjireading(self, response):
        content = response.xpath('//div[@class="concepts"]')
        hiraganas = []
        kanjis = []
        
        for info in content.xpath('.//div/div/div[contains(@class, "japanese")]/div[contains(@class, "representation")]'):
            hiraganas.append(''.join([x.strip() for x in info.xpath('.//span[@class="furigana"]/span/text()').extract()]))
            kanjis.append(''.join([x.strip() for x in info.xpath('.//span[@class="text"]/text() | .//span[@class="text"]/span/text()').extract()]))

        for item in zip(kanjis, hiraganas):
            KanjiReading = KanjiReadingItem()
            KanjiReading['level'] = response.meta['level']
            KanjiReading['kanji'] = item[0]
            KanjiReading['hiragana'] = item[1]

            yield KanjiReading

        next_page = response.xpath('//a[@class="more"]/@href')
        if next_page is not None:
            yield response.follow(next_page, self.parse_kanjireading)


    def process_reading_compound(self, reading_list):
        on_reading = []
        kun_reading = []

        for reading in reading_list:
            if re.search('On', reading.xpath('.//h2/text()').extract_first()):
                for read in reading.xpath('.//ul/li/text()').extract():
                    read = re.sub(r'】', '【', read)
                    on_read = [on.strip() for on in read.split('【')]
                    on_reading.append(
                        dict(
                            kanji = on_read[0],
                            hiragana = on_read[1],
                            english = on_read[2]
                        )
                    )
            else:
                for read in reading.xpath('.//ul/li/text()').extract():
                    read = re.sub(r'】', '【', read)
                    kun_read = [kun.strip() for kun in read.split('【')]
                    kun_reading.append(
                        dict(
                            kanji = kun_read[0],
                            hiragana = kun_read[1],
                            english = kun_read[2]
                        )
                    )
        
        return on_reading, kun_reading

    
