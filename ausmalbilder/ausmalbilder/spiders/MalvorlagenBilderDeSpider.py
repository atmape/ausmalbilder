import scrapy
import os

class MalvorlagenBilderDeSpider(scrapy.Spider):
    name = "malvorlagen-bilder.de"
    allowed_domains = ["www.malvorlagen-bilder.de"]
    start_urls = [
        "https://www.malvorlagen-bilder.de/"
    ]

    def parse(self, response):
        for headhref in response.xpath('//ul/li/a/@href').extract():
            if 'malvorlage' or 'ausmalbild' in headhref:
                yield scrapy.Request(
                    url = response.urljoin(headhref),
                    callback = self.parse_select
                )
        
    def parse_select(self, response):
        for headhref in response.xpath('//a/@href').extract():
            if 'ausmalbild' in headhref:
                yield scrapy.Request(
                    url = response.urljoin(headhref),
                    callback = self.parse_pdf_content
                )

    def parse_pdf_content(self, response):
        for pdf in response.xpath('//a/@href').extract():
            print(pdf)
            if not '.pdf' in pdf:
                continue
            self.logger.info('Parse_pdf_content %s', pdf)
            yield scrapy.Request(
                url = response.urljoin(pdf),
                callback = self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        self.logger.info('Saving PDF %s', path)
        with open(os.path.join(self.name,path), 'wb') as f:
            f.write(response.body)

      

