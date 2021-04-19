import scrapy

class imdbSpider(scrapy.Spider):
    name = 'tugas'
    start_urls = ['https://www.imdb.com/search/title/?country_of_origin=id&ref_=tt_dt_dt']

    def parse_item(self, response):
        tes_ambil = response.css('h1 span a::text').get()
        if tes_ambil is None:
            item = {
                'title': response.css('h1::text').get().strip(),
                'year': response.css('div.table.full-width a::text')[1].get(),
                'rating': response.css('div.ratingValue span::text').get(),
                'director': response.css('div.credit_summary_item a::text').get(),
                'stars': response.css('div.credit_summary_item a::text')[-4:-1].getall()

            }
        else:
            item = {
                'title': response.css('h1::text').get().strip(),
                'year': response.css('h1 span a::text').get(),
                'rating': response.css('div.ratingValue span::text').get(),
                'director': response.css('div.credit_summary_item a::text').get(),
                'stars': response.css('div.credit_summary_item a::text')[-4:-1].getall()

            }
            yield item

    def parse(self, response):
        for post in response.css('div.lister-item-content'):
            dict_url = {
                'url': post.css('h3 a::attr(href)').get()
            }
            link = "https://www.imdb.com" + dict_url.get('url')
            if link is not None:
                yield scrapy.Request(url=link, callback=self.parse_item)

        next_page = response.css('div.desc ::attr(href)')[-1].get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

