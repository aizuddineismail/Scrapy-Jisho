# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
from Jisho.items import KanjiItem, KanjiReadingItem

class JishoPipeline(object):
    def process_item(self, item, spider):
        return item

# class KanjiItemPipeline(object):

#     def open_spider(self, spider):
#         self.file = open('KanjiItem.json', 'w', encoding='utf-8')
    
#     def close_spider(self, spider):
#         self.file.close()
    
#     def process_item(self, item, spider):
#         if isinstance(item, KanjiItem):
#             line = json.dumps(dict(item)) + "\n"
#             self.file.write(line)
#             return item
#         else:
#             raise DropItem("N/A")

# class KanjiReadingItemPipeline(object):

#     def open_spider(self, spider):
#         self.file = open('KanjiReadingItem.json', 'w', encoding='utf-8')
    
#     def close_spider(self, spider):
#         self.file.close()
    
#     def process_item(self, item, spider):
#         if isinstance(item, KanjiReadingItem):
#             line = json.dumps(dict(item)) + "\n"
#             self.file.write(line)
#             return item
#         else:
#             raise DropItem("N/A")

