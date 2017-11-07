# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadolibreItem(scrapy.Item):
    prueba = scrapy.Field()
    titulo = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    main_details = scrapy.Field()
    google_map = scrapy.Field()
    data_holder = scrapy.Field()
    paginacion = scrapy.Field()
    pass

class EbayItem(scrapy.Item):
    precio = scrapy.Field()
    pass