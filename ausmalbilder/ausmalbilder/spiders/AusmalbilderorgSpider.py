import scrapy
import os
import fitz

class MalvorlagenBilderDeSpider(scrapy.Spider):
    name = "ausmalbilder.org"
    allowed_domains = ["www.ausmalbilder.org"]
    start_urls = [
        "https://www.ausmalbilder.org/"
    ]

    def parse(self, response):
        for headhref in response.xpath('//a/@href').extract():
            if str(headhref).startswith('./cat'):
                yield scrapy.Request(
                    url = response.urljoin(headhref),
                    callback = self.parse_cat
                )
        
    def parse_cat(self, response):
        for headhref in response.xpath('//a/@href').extract():
            if str(headhref).startswith('./img'):
                yield scrapy.Request(
                    url = response.urljoin(headhref),
                    callback = self.parse_img
                )

    def parse_img(self,response):
        for img in response.xpath('//img/@src').extract():
            if str(img).startswith('https://www.ausmalbilder.org'):
                yield scrapy.Request(
                    url = img,
                    callback = self.save_pdf
                )


    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        if not os.path.exists(os.path.join('/tmp/',self.name)):
            os.mkdir(os.path.join('/tmp/',self.name))
        self.logger.info('Saving Image %s to /tmp', path)
        with open(os.path.join('/tmp/',self.name,path), 'wb') as f:
            f.write(response.body)       
        self.logger.info('Creating PDF %s', path)

        pdfdoc = fitz.open()
        pdfpage = pdfdoc.new_page()
        pdfpage.insert_image(pdfpage.rect, filename=os.path.join('/tmp/',self.name,path))
        pdfname = os.path.splitext(os.path.join(self.name,path))[0] + '.pdf'
        self.logger.info('Creating new PDF %s', pdfname)
        pdfdoc.ez_save(pdfname)
        os.remove(os.path.join('/tmp/',self.name,path))

