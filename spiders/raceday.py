import re
import csv
from datetime import datetime, date
from time import strftime
import pprint
from datetime import time
import logging

import scrapy
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from dateutil.relativedelta import relativedelta
from time import sleep
# from ..textxml import *
from scrapy.log import ScrapyFileLogObserver

from hkdata.items import RacedayItemLoader

pp = pprint.PrettyPrinter(indent=4)



# USAGE:

# scrapy crawl raceday -a date=20150201 -a coursecode='ST'
# or latest event scrapy crawl raceday



class Racedayspider(scrapy.Spider):
    name = "raceday"
    allowed_domains = ["hkjc.com"]
    start_url = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/English/Local/%s/%s/1"

    ###NEEDS TO USE **kwargs) and get
    def __init__(self, **kwargs):
        self.historical = True
        self.filename = kwargs.pop('filename', None)
        if not self.filename:
            self.racedate = kwargs.pop('date')
            self.racecode = kwargs.pop('coursecode')

    def start_requests(self):
        if self.historical:
            if self.filename:
                with open(self.filename, mode='r') as inh:
                    for row in csv.reader(inh):
                        yield Request(self.start_url % (row[0], row[1]))
            else:
                yield Request(self.start_url % (self.racedate, self.racecode))
        else:
            yield Request("http://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/")

    def parse(self, response):

        if "No race meeting" in response.body:
            log.msg("Results page not ready, waiting 2 secs...", logLevel=log.INFO)
            sleep(2)
            yield Request(response.url, dont_filter=True)
        else:
            from scrapy.shell import inspect_response
            inspect_response(response, self)
            bl = RacedayItemLoader(response=response)
            racedate, course, num = response.url.split('/')[-3:]
            bl.add_value('RaceDate', racedate)
            bl.add_value('RacecourseCode', course)
            bl.add_value('RaceNumber', num)
            bl.add_xpath('RaceDateTime', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[3]",
                         re=r",.+?(\S+\s+\d{2},\s+\d{4}),.+?,.+?(\d{2}:\d{2})")
            bl.add_xpath('RaceName', "//table[@class='font13 lineH20 tdAlignL']//td[1]/span[@class='bold']/text()",
                         re="\xa0-\xa0(.+)")
            bl.add_xpath('Surface', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[4]")
            bl.add_xpath('RailType', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[4]")
            bl.add_xpath('Distance', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[4]")
            # bl.add_xpath('Going', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[4]")
            bl.add_xpath('Prizemoney', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[5]",
                         re=r'Prize Money: \$(\d*)')
            bl.add_xpath('Raceratingspan', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[5]",
                         re=r'Rating:.*?([\d\-]+)')
            bl.add_xpath('Raceclass', "(//table[@class='font13 lineH20 tdAlignL']//td[1]/text())[5]",
                         re=r'Class.*?(\d+)')
            bl.add_xpath('file_urls', '//table[@class="tdAlignL"]//a[2]/@href', re=r'http.+pdf')
            base_item = bl.load_item()
            for row in response.xpath("//table[@class='tableBorderBlue tdAlignC']//table/tr[position()>1]"):
                l = RacedayItemLoader(item=base_item, selector=row)
                l.add_xpath('HorseNumber', './td[1]/text()')
                l.add_xpath('Last6runs', './td[2]/text()')
                l.add_xpath('Horsename', './td[4]/a/text()')
                l.add_xpath('Horsecode', './td[5]/text()')
                l.add_xpath('Jockeyname', './td[7]/text()', re=r"(.+?)\(")
                l.add_xpath('Jockeycode', './td[7]/text()', re=r"\((.+)\)")
                l.add_xpath('JockeyWtOver', './td[8]/text()')
                l.add_xpath('Draw', './td[9]/text()')
                l.add_xpath('Trainername', './td[10]/text()')
                l.add_xpath('Rating', './td[11]/text()')
                l.add_xpath('RatingChangeL1', './td[12]/text()')
                l.add_xpath('DeclarHorseWt', './td[13]/text()')
                l.add_xpath('HorseWtDeclarChange', './td[14]/text()')
                l.add_xpath('Age', './td[16]/text()')
                l.add_xpath('WFA', './td[17]/text()')
                l.add_xpath('Sex', './td[18]/text()')
                l.add_xpath('SeasonStakes', './td[19]/text()')
                l.add_xpath('Priority', './td[20]/text()')
                l.add_xpath('Gear', './td[21]/text()')
                l.add_xpath('Owner', './td[22]/text()')
                l.add_xpath('SireName', './td[23]/text()')
                l.add_xpath('DamName', './td[24]/text()')
                l.add_xpath('ImportType', './td[25]/text()')
                yield l.load_item()
                break







"""

            #extract links receives Response returns a list of scrapy.link,Link objs
            #use instead of a crawl spider!
            for link in LinkExtractor(restrict_xpaths="//div[contains(@class,'raceNum')]",
                                      deny=(r'.*/Simulcast/.*')).extract_links(response)[:-1]:
                yield Request(link.url)


            # racedate = response.xpath("//html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table/tbody/tr/td[4]/text()").extract()
            # racecoursecode = response.xpath("//html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table/tbody/tr/td[4]/nobr/text()").extract()
            # racenumber = re.sub("\D", "", response.xpath('//td[@class="content"]/strong/text()').extract())
            # racenumber = 1

            #local page response.xpath("//a[@class='blueBtn']/text()").extract() data DD MMM - Raeccoursename

            #use URL for racedate
            dd = response.url.split("/")
            racecoursecode = dd[-2]
            racenumber = dd[-1]
            racedate = datetime.strptime(dd[-3], "%Y%m%d")
            localjumptime = re.sub(r'([^\s\w:]|_)+', '',
                                   response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/text()").extract()[
                                       2]).strip()[-5:]
            localjumptime = datetime.strptime(localjumptime, "%H:%M").time()
            racedatetime = datetime.combine(racedate, localjumptime)
            # racedate1 = response.xpath("//a[@class='blueBtn']/text()").extract()[0][:6]
            # racedateobj = datetime.strptime(racedate1, "%d %b").date().replace(year=datetime.today().year)

            #rc
            # rc= response.xpath("//a[@class='blueBtn']/text()").extract()[0][7:]
            # racecoursecode = 'HV' if re.sub(ur"[\W_]+", "", rc) == "HappyValley" else 'ST'
            #new race data
            #THE TABLE  response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]").extract() 
            #ALT re.sub(r"[\D]+", "", response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/span/text()").extract()[0])
            # racenumber = response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/span/text()").extract()[0].split()[1]
            # racename = response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/span/text()").extract()[0].split()


            racename = re.sub(r'([^\s\w]|_)+', '',
                              response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/span/text()").extract()[0])
            racename = re.sub(r'Race [\d]+', '', racename)
            # time format hh:mm

            ### RACE INFO
            r2 = response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/text()").extract()

            #TURF/AWT
            surface = re.sub(r'([^\s\w:]|_)+', '', r2[3]).strip().split(u" ")[0].upper()
            #format A B C D+2 etc..
            railtype = re.sub(r'([^\s\w:]|_)+', '', r2[3]).strip().split(u" ")[1]
            distance = re.sub(r'([^\s\w:]|_)+', '', r2[3]).strip().split(u" ")[3].replace('M', '')
            prizemoney = re.sub(r'([^\s\w:]|_)+', '', r2[4]).strip().split(u" ")[2]
            raceratingspan = re.sub(r'([^\s\w-]|_)+', '', r2[4]).strip().split(u" ")[3].replace("Rating", "")
            if re.sub(r'([^\s\w-]|_)+', ' ', r2[4]).strip().split(u" ")[-2] == "Class":
                raceclass = re.sub(r'([^\s\w-]|_)+', ' ', r2[4]).strip().split(u" ")[-1]
                raceclass = "Class " + str(raceclass)
            else:
                raceclass = None
                # if no racebook url -> http://www.hkjc.com/english/racing/No_PDF_Download_all.html
            #response.xpath("//img[@alt='Download Race Form (All Races)']").extract() selenium

            #d/l to store as image URL
            #harcode http://racing.hkjc.com/racing/content/PDF/RaceCard/20150101_starter_all.pdf
            #replace _r1 re match r' _r\d
            # http://racing.hkjc.com/racing/content/PDF/RaceCard/20130101_starter_all.pdf GET ALL
            #construct racebookurl from date
            file_urls = ["http://racing.hkjc.com/racing/content/PDF/RaceCard/" + racedate.strftime("%Y%m%d") + "_starter_all.pdf"]

            # racebook_race = response.xpath("//img[contains(@src,\"/racing/Info/StaticFile/English/images/print_btn_all.gif\")]/preceding::a[1]/@href").extract()[0]

            meta = dict(
                Racecoursecode=racecoursecode,
                Racenumber=racenumber,
                RaceName=racename,
                Surface=surface,
                RailType=railtype,
                Distance=distance,
                Prizemoney=prizemoney,
                Raceratingspan=raceratingspan,
                Raceclass=raceclass,
                Racedate=racedate,
                Racedatetime=racedatetime,
                file_urls=file_urls
            )
            runners = response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")

            for r in runners:
                item = items.RacedayItem()
                horsenumber = r.xpath("td[1]/text()").extract()[0].strip()
                item['HorseNumber'] = try_int(horsenumber)
                item['Last6runs'] = r.xpath("td[2]/text()").extract()[0].strip()
                #HorseColors here
                item['image_urls'] = [r.xpath("td[3]/img/@src").extract()[0].strip()]
                item['Horsename'] = r.xpath("td[4]/a/text()").extract()[0].strip()
                item['Horsecode'] = r.xpath("td[5]/text()").extract()[0].strip()
                item['ActualWt'] = int(r.xpath("td[6]/text()").extract()[0].strip())

                #what if jockeyname has '()' 
                jockeyname = r.xpath("td[7]/a/text()").extract()[0].strip()
                if u'(' in jockeyname:
                    weightdiff = int(jockeyname.split('(')[1].replace(')', '').strip())
                    jockeyname = jockeyname.split('(')[0].strip()
                    item['ActualWt'] += weightdiff
                jockeyname = jockeyname if u'(' not in jockeyname else jockeyname.split('(')[0].strip()
                item['Jockeyname'] = jockeyname
                item['Jockeycode'] = re.search(r'.*jockeycode=(.*)\',', r.xpath("td[7]/a/@href").extract()[0].strip()).group(1)
                item['JockeyWtOver'] = r.xpath("td[8]/text()").extract()[0].strip()
                draw = r.xpath("td[9]/text()").extract()[0].strip()
                item['Draw'] = try_int(draw)
                item['Trainername'] = r.xpath("td[10]/a/text()").extract()[0].strip()
                item['Trainercode'] = re.search(r'.*trainercode=(.*)\',', r.xpath("td[10]/a/@href").extract()[0].strip()).group(1)
                rating = r.xpath("td[11]/text()").extract()[0].strip()
                item['Rating'] = try_int(rating)
                ratingchangel1 = r.xpath("td[12]/text()").extract()[0].strip()
                item['RatingChangeL1'] = try_int(ratingchangel1)
                declarhorsewt = r.xpath("td[13]/text()").extract()[0].strip()
                item['DeclarHorseWt'] = try_int(declarhorsewt)
                horsewtdeclarchange = r.xpath("td[14]/text()").extract()[0].strip()
                item['HorseWtDeclarChange'] = try_int(horsewtdeclarchange)
                age = int(r.xpath("td[16]/text()").extract()[0].strip())
                yearofbirth = meta['Racedate'] - relativedelta(years=age)
                item['Age'] = age
                item['YearofBirth'] = yearofbirth.year
                wfa = r.xpath("td[17]/text()").extract()[0].strip()
                item['WFA'] = try_int(wfa) if wfa != '-' else None
                item['Sex'] = r.xpath("td[18]/text()").extract()[0].strip()
                seasonstakes = r.xpath("td[19]/text()").extract()[0].strip()
                item['SeasonStakes'] = try_int(seasonstakes)
                item['Priority'] = r.xpath("td[20]/text()").extract()[0].strip().replace(u'\xa0', u'')
                item['Gear'] = r.xpath("td[21]/text()").extract()[0].strip()
                item['Owner'] = r.xpath("td[22]/text()").extract()[0].strip()
                item['SireName'] = r.xpath("td[23]/text()").extract()[0].strip()
                item['DamName'] = r.xpath("td[24]/text()").extract()[0].strip()
                item['ImportType'] = r.xpath("td[25]/text()").extract()[0].strip()

                item['RaceName'] = meta['RaceName']
                item['RaceDate'] = meta['Racedate']
                item['RaceDateTime'] = meta['Racedatetime']
                item['RaceNumber'] = meta['Racenumber']
                item['RacecourseCode'] = meta['Racecoursecode']
                item['Surface'] = meta['Surface']
                item['RailType'] = meta['RailType']
                item['Distance'] = meta['Distance']
                item['Prizemoney'] = meta['Prizemoney']
                item['Raceratingspan'] = meta['Raceratingspan']
                item['Raceclass'] = meta['Raceclass']
                item['file_urls'] = meta['file_urls']
                yield item

"""