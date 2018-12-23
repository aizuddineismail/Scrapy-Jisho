# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JishoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class KanjiItem(scrapy.Item):
    level = scrapy.Field()
    kanji = scrapy.Field()
    english = scrapy.Field()
    kun = scrapy.Field()
    on = scrapy.Field()
    stroke = scrapy.Field()
    radical = scrapy.Field()
    on_reading = scrapy.Field()
    kun_reading = scrapy.Field()

class KanjiReadingItem(scrapy.Item):
    level = scrapy.Field()
    kanji = scrapy.Field()
    hiragana = scrapy.Field()

class VocabularyItem(scrapy.Item):
    kanji = scrapy.Field()
    hiragana = scrapy.Field()
    level = scrapy.Field()
    meanings = scrapy.Field()