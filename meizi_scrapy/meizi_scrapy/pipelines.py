# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from scrapy.exceptions import DropItem

'''
图片管道
'''


class MeiziScrapyPipeline(ImagesPipeline):

    def process_item(self, item, spider):
        return super().process_item(item, spider)

    def file_path(self, request: Request, response=None, info=None):
        item = request.meta['item']  # 传值
        folder = item['name']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            referer = item['url']
            print(img_url)
            yield Request(img_url, meta={'item': item, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


def strip(path):
    path = re.sub(r'[?\\*|“<>:/]', '', str(path))
    return path


if __name__ == '__main__':
    a = '我是一个?\*|“<>:/错误的字符串'
    print(strip(a))
