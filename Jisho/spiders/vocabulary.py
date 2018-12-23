# -*- coding: utf-8 -*-
import scrapy
from Jisho.items import VocabularyItem

class VocabularySpider(scrapy.Spider):
    name = 'vocabulary'
    allowed_domains = ['jisho.org']
    start_urls = [
        'https://jisho.org/search/%23words%20%23jlpt-n5',
        'https://jisho.org/search/%23words%20%23jlpt-n4',
        'https://jisho.org/search/%23words%20%23jlpt-n3',
        'https://jisho.org/search/%23words%20%23jlpt-n2',
        'https://jisho.org/search/%23words%20%23jlpt-n1',
        ]
    
    custom_settings = {
        'FEED_URI': "vocabulary_full.json"
    }

    def parse(self, response):
        
        for concept in response.xpath('//div[@class="concept_light clearfix"]'):
            Vocabulary = VocabularyItem()
            Vocabulary['kanji'] = self.process_kanji(concept.xpath('.//span[@class="text"]'))
            Vocabulary['hiragana'] = self.process_hiragana(concept.xpath('.//span[@class="furigana"]'))
            Vocabulary['level'] = concept.xpath('.//span[@class="concept_light-tag label"]/text()').extract_first().replace("JLPT", "").strip()
            Vocabulary['meanings'] = [x.strip() for x in concept.xpath('.//span[@class="meaning-meaning"]/text()').extract() if x != '、']
            
            yield Vocabulary

        next_page = response.xpath('//a[@class="more"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def process_kanji(self, content):
        kanji = []
        for item in content.xpath('.//node()'):
            if isinstance(item.root, str) and item.root.strip() != '':
                kanji.append(item.root.strip())
            
        return kanji
    
    def process_hiragana(self, content):
        hiragana = []
        for item in content.xpath('.//node()'):
            if not isinstance(item.root, str):
                temp = ''.join(item.xpath('.//text()').extract())
                hiragana.append(temp)
        return hiragana