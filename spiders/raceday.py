import scrapy
import re
from .. import items 
from scrapy.contrib.spiders import Rule, CrawlSpider
from datetime import datetime, date
from time import strftime
from scrapy import log
import pprint
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import time
from dateutil.relativedelta import relativedelta
import logging
# from ..textxml import *
from scrapy.log import ScrapyFileLogObserver
pp = pprint.PrettyPrinter(indent=4)


def tf(values, encoding="utf-8"):
    value = ""
    for v in values:
        if v is not None and v != "":
            value = v
            break
    return value.encode(encoding).strip()


#USAGE: 

# scrapy crawl raceday -a date=20150201 -a coursecode='ST'
# or latest event scrapy crawl raceday



class Racedayspider(scrapy.Spider):
    name = "raceday"
    allowed_domains = ["hkjc.com"]
    # 20150201 %Y%m%d
    # start_url = "http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/%s/1"
    start_url = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/English/Local/%s/%s/1"

    ###NEEDS TO USE **kwargs) and get
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.historical = True
            self.racedate = kwargs.get('date')
            self.racecode = kwargs.get('coursecode')

    # def __init__(self, date=None, coursecode=None):
    #     if date is None or coursecode is None:
    #         self.historical = False
    #         # start_url = "http://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/"
    #         # raise ValueError("Invalid spider parameters")
    #     else:
    #         self.racedate = date
    #         self.racecode = coursecode
    #         self.historical = True
    #     logfile = open('testlog.log', 'w')
    #     log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
    #     log_observer.start()

# class OddsSpider(CrawlSpider):
#     name = "raceday"
#     allowed_domains = ["racing.hkjc.com"]



#     start_urls = [
#         "http://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/"
#     ]

#     rules = (
    
#     Rule(LinkExtractor(allow=('/racing/Info/Meeting/RaceCard/English/Local/.*', ), deny=('subsection\.php',)), \
#         callback='parse_raceday', follow=True),
    

#     )

    
    # RE_VAL  = re.compile(r"^:*\s*")
    # RE_DIGITS = re.compile(r"\D")


    def start_requests(self):
        if self.historical:
            return [Request(self.start_url % (self.racedate, self.racecode))]
        return [Request("http://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/")]
        

    def parse(self, response):

        if "No race meeting" in response.body:
            log.msg("No meeting")
        try:
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
            localjumptime = re.sub(r'([^\s\w:]|_)+', '',response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/text()").extract()[2]).strip()[-5:]
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


            racename = re.sub(r'([^\s\w]|_)+', '',response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/span/text()").extract()[0])
            racename = re.sub(r'Race [\d]+', '', racename)
            # time format hh:mm

            ### RACE INFO
            r2 = response.xpath("//table[@class=\"font13 lineH20 tdAlignL\"]/tr/td/text()").extract()
            
              #TURF/AWT
            surface = re.sub(r'([^\s\w:]|_)+', '',r2[3]).strip().split(u" ")[0].upper()
            #format A B C D+2 etc..
            railtype = re.sub(r'([^\s\w:]|_)+', '',r2[3]).strip().split(u" ")[1]
            distance = re.sub(r'([^\s\w:]|_)+', '',r2[3]).strip().split(u" ")[3].replace('M', '')
            prizemoney = re.sub(r'([^\s\w:]|_)+', '',r2[4]).strip().split(u" ")[2]
            raceratingspan = re.sub(r'([^\s\w-]|_)+', '',r2[4]).strip().split(u" ")[3].replace("Rating", "")
            if re.sub(r'([^\s\w-]|_)+', ' ',r2[4]).strip().split(u" ")[-2] =="Class":
                raceclass = re.sub(r'([^\s\w-]|_)+', ' ',r2[4]).strip().split(u" ")[-1]
                raceclass = "Class "+ str(raceclass)
            else:
                raceclass = None  
            # if no racebook url -> http://www.hkjc.com/english/racing/No_PDF_Download_all.html
            #response.xpath("//img[@alt='Download Race Form (All Races)']").extract() selenium

            #d/l to store as image URL
            #harcode http://racing.hkjc.com/racing/content/PDF/RaceCard/20150101_starter_all.pdf
            #replace _r1 re match r' _r\d
            # http://racing.hkjc.com/racing/content/PDF/RaceCard/20130101_starter_all.pdf GET ALL
            #construct racebookurl from date
            file_urls=  ["http://racing.hkjc.com/racing/content/PDF/RaceCard/" + racedate.strftime("%Y%m%d") + "_starter_all.pdf"]

            # racebook_race = response.xpath("//img[contains(@src,\"/racing/Info/StaticFile/English/images/print_btn_all.gif\")]/preceding::a[1]/@href").extract()[0]

            meta = dict(
                Racecoursecode = racecoursecode,
                Racenumber = racenumber,
                RaceName = racename, 
                Surface = surface,
                RailType = railtype,
                Distance = distance,
                Prizemoney = prizemoney,
                Raceratingspan = raceratingspan,
                Raceclass = raceclass,
                Racedate = racedate,
                Racedatetime = racedatetime,
                file_urls = file_urls 
                )
            #THE TABLE
            #eachhorse is response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")[i].extract()
            #horseno is response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")[0].xpath("td[1]").extract()
            #tablesel = response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")

            #add items
            # item = items.HkOddsItem(**meta)
            # oddsdata = Vividict()
            # racecoursecode = 'ST' if meta["Racecoursecode"] == 'Sha Tin' else 'HV'
            # oddsdata = getOddsData(item["Racecoursecode"], racedate, 8)
            #oddsdata is a dict. race, [place|win], horseno odds, 

            #get runners each race
            pp.pprint(meta)


            runner_items= []
            # runner_items.append(item)
            # pprint(runner_items)
            runners= response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")

            for r in runners:
                item = items.RacedayItem()
                item['HorseNumber'] = r.xpath("td[1]/text()").extract()[0].strip()
                item['Last6runs'] = r.xpath("td[2]/text()").extract()[0].strip()
                #HorseColors here
                item['image_urls'] = [r.xpath("td[3]/img/@src").extract()[0].strip(),]
                item['Horsename'] = r.xpath("td[4]/a/text()").extract()[0].strip()
                item['Horsecode'] = r.xpath("td[5]/text()").extract()[0].strip()
                item['ActualWt'] = r.xpath("td[6]/text()").extract()[0].strip()
                item['Jockeyname'] = r.xpath("td[7]/a/text()").extract()[0].strip()
                item['Jockeycode'] = re.search(r'.*jockeycode=(.*)\',', r.xpath("td[7]/a/@href").extract()[0].strip()).group(1) 
                item['JockeyWtOver'] = r.xpath("td[8]/text()").extract()[0].strip()
                item['Draw'] = r.xpath("td[9]/text()").extract()[0].strip() 
                item['Trainername'] = r.xpath("td[10]/a/text()").extract()[0].strip()
                item['Trainercode'] = re.search(r'.*trainercode=(.*)\',', r.xpath("td[10]/a/@href").extract()[0].strip()).group(1)
                item['Rating'] = r.xpath("td[11]/text()").extract()[0].strip()
                item['RatingChangeL1'] = r.xpath("td[12]/text()").extract()[0].strip()
                item['DeclarHorseWt'] = r.xpath("td[13]/text()").extract()[0].strip()
                item['HorseWtDeclarChange'] = r.xpath("td[14]/text()").extract()[0].strip()
                age = int(r.xpath("td[16]/text()").extract()[0].strip())
                yearofbirth = meta['Racedate'] - relativedelta(years=age)
                item['Age'] = age
                item['YearofBirth'] = yearofbirth.year
                wfa = r.xpath("td[17]/text()").extract()[0].strip()
                item['WFA'] = wfa if wfa != '-' else None
                item['Sex'] = r.xpath("td[18]/text()").extract()[0].strip()
                item['SeasonStakes'] = r.xpath("td[19]/text()").extract()[0].strip()
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
                runner_items.append(item)

            return runner_items 


#             for row, r in enumerate(response.xpath("//table[@class=\"draggable hiddenable\"]/tr[contains(@class, 'font13 tdAlignC')]")):
#                 if row:
#                     for j, k in enumerate(('Horseno','Last6runs','image_url', 'Horsename','Horsecode', 'Jockeywt','Jockeyname','Jockeycode','Jockeywtover','Draw', 'Trainer', 'Trainercode','Rating' \
#                     ,'RatingChangeL1', 'Horsewtdeclaration','Horsewtdeclarationchange', 'Besttime','Age', 'WFA', 'Sex', 'SeasonStakes', 'Priority', 'Gear','Owner', 'SireName' \
#                     ,'DamName', 'Importtype' 

#                     )):
#                         #28 columns
#                             item['Horseno'] = r.xpath("td[1]/text()").extract()[0].strip()
#                             item['Last6runs'] = r.xpath("td[2]/text()").extract()[0].strip()
#                             item['image_url'] = r.xpath("td[3]/img/@src").extract()[0].strip()
#                             item['Horsename'] = r.xpath("td[4]/a/text()").extract()[0].strip()
#                             item['Horsecode'] = r.xpath("td[5]/text()").extract()[0].strip()
#                             item['Jockeywt'] = r.xpath("td[6]/text()").extract()[0].strip()
#                             item['Jockeyname'] = r.xpath("td[7]/a/text()").extract()[0].strip()
#                             item['Jockeycode'] = re.search(r'.*jockeycode=(.*)\',', r.xpath("td[7]/a/@href").extract()[0].strip()).group(1) 
#                             # item['Jockeywtover'] = r.xpath("td[9]/text()").extract()[0].strip()
#                             item['Draw'] = r.xpath("td[9]/text()").extract()[0].strip() 
#                             item['Trainer'] = r.xpath("td[10]/a/text()").extract()[0].strip()
#                             item['Trainercode'] = re.search(r'.*trainercode=(.*)\',', r.xpath("td[10]/a/@href").extract()[0].strip()).group(1)
#                             item['Rating'] = r.xpath("td[11]/text()").extract()[0].strip()
#                             item['RatingChangeL1'] = r.xpath("td[12]/text()").extract()[0].strip()
#                             item['Horsewtdeclaration'] = r.xpath("td[13]/text()").extract()[0].strip()
#                             item['Horsewtdeclarationchange'] = r.xpath("td[14]/text()").extract()[0].strip()
#                             r2 = r.xpath("td[15]/text()").extract()[0].strip()
#                             # item['Besttime'] = time(0, int('0'+r2.split('.')[0]), int(r2.split('.')[1]), int(r.xpath("td[15]/text()").extract()[0].strip().split('.')[2]))
#                             # item['Besttime']= time(0, int('0'+r.xpath("td[15]/text()").extract()[0].split('.')[0]), int(r.xpath("td[15]/text()").extract()[0].split('.')[1]), \
#                                 # int(r.xpath("td[15]/text()").extract()[0].split('.')[2]))
#                             item['Age'] = r.xpath("td[16]/text()").extract()[0].strip()
#                             item['WFA'] = r.xpath("td[17]/text()").extract()[0].strip()
#                             item['Sex'] = r.xpath("td[18]/text()").extract()[0].strip()
#                             item['Seasonstakes'] = r.xpath("td[19]/text()").extract()[0].strip()
#                             item['Priority'] = r.xpath("td[20]/text()").extract()[0].strip()
#                             item['Gear'] = r.xpath("td[21]/text()").extract()[0].strip()
#                             item['Owner'] = r.xpath("td[22]/text()").extract()[0].strip()
#                             item['Sirename'] = r.xpath("td[23]/text()").extract()[0].strip()
#                             item['Damname'] = r.xpath("td[24]/text()").extract()[0].strip()
#                             item['Importtype'] = r.xpath("td[25]/text()").extract()[0].strip()
#                             runner_items.append(item)    
#                         # if j == 3:
#                         #     #horse name
#                         #     item[k] = r.xpath("td[j]/a/text()").extract()[0].strip()
#                         # if j ==5:
#                         #     #j name
#                         #     item[k] = r.xpath("td[j]/a/text()").extract()[0].strip()
#                         # if j ==6:
#                         #     #j code
#                         #     item[k] = re.search(r'.*jockeycode=(.*)\',', r.xpath("td[j]/a/@href").extract()[0].strip()).group(1)     
#                         # if j== 10:
#                         #     #trainer name
#                         #     item[k] = r.xpath("td[j]/a/text()").extract()[0].strip()
#                         #     # item[k] = tablesel[j].xpath("td[4]/a/text()").extract()[0].strip()
#                         #     # item[k] = re.search(r'.*horseno=(.*)\',', tablesel[j].xpath("td[4]/a/@href").extract()[0].strip()).group(1)
#                         #     #item[k] = tablesel[j].xpath("td[5]").extract()[0].strip()
#                         # if j == 11:
#                         #     item[k] = re.search(r'.*trainercode=(.*)\',', r.xpath("td[j]/a/@href").extract()[0].strip()).group(1)  
#                         # if j == 15:
#                         #     #besttime
#                         #     item[k] = time(0, int(mins), int(r2.split('.')[1]), int(r.xpath("td[15]/text()").extract()[0].strip().split('.')[2]))
#                         # else:
#                         #     item[k] = baseurl.xpath("td[j]/text()").extract()[0].strip()
#             #TODO SIMPLY THIS DIRECT ASSIGNMENT
#             #LOOP OVER ALL TRs in TABLE except first
            
#             #download race form this race img text() Download Race Form (All Races)


#             # localjumptime = response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[2]/text()").extract()[0]
#             # racedate = response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[1]/text()").extract()[0]
#             # #convert to TIME
#             # racedate = datetime.strptime(racedate, "%d/%m/%Y").date()
#             # localjumptime = datetime.strptime(localjumptime, "%H:%M").time()
#             # racecoursecode = response.xpath("//label[contains(text(), 'All Up')]/../preceding-sibling::td[2]/nobr/text()").extract()

#             #GET THIS FOR EVERY RACE

#             # meta = dict(
#             #         # Racedate = response.xpath("//td[contains(text(),'Win Place')]/../following-sibling::td[2]/text()").extract(),
#             #         # Racecoursecode = response.xpath("//td[contains(text(), 'Win Place')]/../following-sibling::td[2]/nobr/text()").extract(),

#             #         Racecoursecode = Racecoursecode,
#             #         Racenumber=  re.sub(r'\D', '',response.xpath("//strong[contains(text(),'Race')]/text()").extract()[0]),
#             #         #SPLIT ON COMMA
#             #         Racename = re.sub(r'\,$','', response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/text()").extract()[0].strip()),
#             #         Racedatetime = datetime.combine(racedate, localjumptime),
#             #         Raceclass = response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[3]/text()").extract(),
#             #         Surface =response.("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[4]/text()").extract(),
#             #         TrackType =  response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[5]/text()").extract(),
#             #         # Distance =   re.sub(r'\D', '', response.xpath("//strong[contains(text(),'Race')]/../following-sibling::td[2]/nobr[6]/text()").extract()[0]),
#             #         # DamName=RE_VAL.sub("", tf(response.xpath("//font[text()='Dam']/../following-sibling::td[1]/font/text()").extract())),
#             #         # Horseno = response.xpath("//div[contains(@id,\"detailWPTable\")]/table/tbody/tr/text()").extract()

#     #odds tavle div empty

#             #get odds data
  



#     #response.xpath("//table[contains(@id, \"betAmountCalTopcal1\") and parent::td]/parent::td/parent::tr/parent::table/parent::td/parent::tr/following-sibling::tr/td/div[@id=\"detailWPTable\"]").extract()
#             #the oddstable
#             # for i, r in enumerate(response.css('.bigborder tr')):
#             #     if i:
#             #         item = HorseItem(**meta)
#             #         for j, k in enumerate(('EventDate', 'EventType', 'EventVenue', 'EventDescription', 'Gear')):
#             #             item[k] = tf(r.xpath("./td[%s]/font/text()" % (j+1)).extract()).replace("\xc2\xa0", " ").strip()
#             #         item["EventDate"] = datetime.strptime(item["EventDate"], "%d/%m/%Y").date()
#             #         yield item
# # xpath
#             # pp.pprint(runner_items)
            
#             return runner_items
            #ON WIN/PLACE page
            #get date racecourse 
            # racedate = response.css(".subsubh            # )
# eader .title_eng_text").xpath("text()").extract()).split("\xc2\xa0")[0].strip()
            # meta = dict(HorseCode=horse_code,
            #             HorseName=horse_name,
            #             Homecountry='HKG', 
            #             Importtype=RE_VAL.sub("", tf(response.xpath("//font[contains(text(),'Import') and contains(text(),'Type')]/../following-sibling::td[1]/font/text()").extract())),
            #             Owner=tf(response.xpath("//font[text()='Owner']/../following-sibling::td[1]/font/a/text()").extract()),
            #             SireName=tf(response.xpath("//font[text()='Sire']/../following-sibling::td[1]/font/a/text()").extract()),
            #             DamName=RE_VAL.sub("", tf(response.xpath("//font[text()='Dam']/../following-sibling::td[1]/font/text()").extract())),
            #             DamSireName=RE_VAL.sub("", tf(response.xpath("//font[text()=\"Dam's Sire\"]/../following-sibling::td[1]/font/text()").extract())))
            
            # for i, r in enumerate(response.css('.bigborder tr')):
            #     if i:
            #         item = HorseItem(**meta)
            #         for j, k in enumerate(('EventDate', 'EventType', 'EventVenue', 'EventDescription', 'Gear')):
            #             item[k] = tf(r.xpath("./td[%s]/font/text()" % (j+1)).extract()).replace("\xc2\xa0", " ").strip()
            #         item["EventDate"] = datetime.strptime(item["EventDate"], "%d/%m/%Y").date()
            #         yield item
        except Exception, e:
            log.msg("Skipping meeting because of error: %s" % (str(e)))

