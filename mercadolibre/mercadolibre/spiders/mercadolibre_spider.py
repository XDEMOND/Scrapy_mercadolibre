from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from mercadolibre.items import MercadolibreItem
from time import time
import csv
import re
import string
import sys
import json

class MercadolibreSpiderSpider(CrawlSpider):
	name = 'mercadolibre_spider'
	allowed_domains = ["inmuebles.mercadolibre.com.mx","casa.mercadolibre.com.mx","departamento.mercadolibre.com.mx","terreno.mercadolibre.com.mx","inmueble.mercadolibre.com.mx"]
	start_urls =['http://inmuebles.mercadolibre.com.mx/*']
	rules = [
			Rule(LinkExtractor(allow=[r'.*_JM']), callback='parse_inmuebles'),
			Rule(LinkExtractor(allow=[r'.*_Desde_[0-9]+$']), callback='parse_paginacion',follow=True),
		]
	def parse_paginacion(self,response):
		item = MercadolibreItem()
		item['paginacion'] = response.url
		#yield item

	def parse_inmuebles(self, response):
		concatena = ""
		item = MercadolibreItem()
		item['titulo'] = response.xpath('//title/text()').extract()[0].encode('utf-8')
		concatena+=response.xpath('//title/text()').extract()[0].encode('utf-8').decode('utf-8')+";"
		item['url'] = response.url
		concatena+=response.url+";"
		item['name'] = map(str,b' '.join([x.encode('utf-8') for x in response.xpath('//h1[@itemprop="name"]/text()').extract()]).strip())

		#Forma alterna de obtener el precio
		#response.xpath('//div[@class="product-info"]/fieldset/article[@class="price ch-price price-without-cents"]/strong/text()').extract()
		item['price'] = b' '.join([x.encode('utf-8') for x in response.xpath('//article[@class="vip-price ch-price"]/strong/text()').extract() ]).strip()
		#concatena+=b' '.join([x.encode('utf-8') for x in response.xpath('//article[@class="vip-price ch-price"]/strong/text()').extract() ]).strip()+";"
		item['main_details'] = response.xpath('//div[@class="card-section"]').extract()[0].encode('utf-8')
		try:
			item['data_holder'] = response.xpath('//div[@class="card-section"]').extract()[1].encode('utf-8')
		except:
			item['data_holder'] = ''

		try:
			item['google_map'] = response.xpath('//div[@id="sectionDynamicMap"]/noscript/img/@src').extract()
		except:
			item['google_map'] = ''
		try:
			pattern = re.compile(r"var dynamicMapProperties = ({.*?});", re.MULTILINE | re.DOTALL)
			locations = response.xpath('//script[contains(., "var dynamicMapProperties")]/text()').re(pattern)[0]
			var_corrd = locations.split(",")
			print(var_corrd)
			item['google_map'] = (var_corrd[0],var_corrd[1])
			concatena+=(var_corrd[0],var_corrd[1])
		except:
			#print("No tiene coordenadas :(")
			item['google_map'] = ''
			concatena+=''
		print(concatena)
		yield item	
