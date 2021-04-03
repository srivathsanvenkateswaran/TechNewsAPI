import scrapy
import json

class VentureBeatSpider(scrapy.Spider):
    
    name = "VentureBeat"
    # This is the name of this particular spider.. name must be unique for every spider 

    start_urls = [
        'https://venturebeat.com/'
    ]
    # These are all the list of urls needed to be crawled by the spider 

    dictList = []
    # This is the List which contains all the dictionaries [JSON Objects] which we will finally convert into a JSON Array

    def parse(self, response):
        # Parsing the required data from response

        titles = response.css('.ArticleListing__title a::text').getall()
        descriptions = titles
        urls = response.css('.ArticleListing__title a::attr(href)').getall()

        images = response.css('.ArticleListing__image::attr(src)').getall()
        images.insert(18, "")
        images.insert(13, "")
        images.insert(31, "")
        images.insert(37, "")

        authors = response.css('.ArticleListing__author::text').getall()
        authors.insert(18, "")
        authors.insert(13, "")
        authors.insert(31, "")
        authors.insert(37, "")

        dates = response.css('.ArticleListing__time::attr(datetime)').getall()
        dates.insert(18, "")
        dates.insert(13, "")
        dates.insert(31, "")
        dates.insert(37, "")

        for item in zip(titles, descriptions, urls, images, authors, dates):
            d = {
                'Title': item[0],
                'Desc': item[1],
                'Url': item[2],
                'Img': item[3],
                'Author': item[4],
                'Source': "Venture Beat",
                'Date' : item[5]
            }
            # Here we are creating a JSON Object from the parsed data 
            self.dictList.append(d)
            # We are appending the dictionary to the list so that we can finally convert it into a JSON Array

        with open("results/VentureBeat.json", 'w') as f:
            f.write(json.dumps(self.dictList)) 
            #json.dumps converts the List of dictionaries into a Json Array
            # writing the json array into a file 

            # Either we can write into a file here or we can specify the command in shell [direct the output flag towards file.json]
            # E.g:
            # scrapy crawl Beebom -o Beebom.json 
