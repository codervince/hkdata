# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join, Identity,  MapCompose
from datetime import datetime, timedelta
from fractions import Fraction
from decimal import Decimal
import re
from re import sub
import unicodedata

#raceday has maximum fields
class RacedayItem(scrapy.Item):
    RaceDate = scrapy.Field() #used for public index only
    LocalRaceDateTime= scrapy.Field()
    RaceDateTime = scrapy.Field()
    RacecourseCode = scrapy.Field()
    RaceName = scrapy.Field()
    Raceclass = scrapy.Field()
    Raceratingspan = scrapy.Field()
    Prizemoney = scrapy.Field()
    Surface = scrapy.Field()
    RailType = scrapy.Field()
    Distance = scrapy.Field()
    RaceNumber = scrapy.Field()
    HorseNumber = scrapy.Field()
    Wt = scrapy.Field()
    Last6runs = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    Horsename = scrapy.Field()
    Horsecode = scrapy.Field()
    Jockeyname = scrapy.Field()
    Jockeycode = scrapy.Field()
    Jockeyclaim = scrapy.Field()
    JockeyWtOver = scrapy.Field()
    Draw = scrapy.Field()
    Trainername = scrapy.Field()
    Trainercode = scrapy.Field()
    Rating = scrapy.Field()
    RatingChangeL1 = scrapy.Field()
    DeclarHorseWt = scrapy.Field()
    HorseWtDeclarChange = scrapy.Field()
    # Besttime = scrapy.Field()
    Age = scrapy.Field()
    WFA = scrapy.Field()
    Sex = scrapy.Field()
    SeasonStakes = scrapy.Field()
    Priority = scrapy.Field()
    Gear = scrapy.Field()
    Owner = scrapy.Field()
    SireName = scrapy.Field()
    DamName = scrapy.Field()
    ImportType = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


def tf(values, encoding="utf-8"):
    value = ""
    for v in values:
        if v is not None and v != "":
            value = v
            break
    return value.encode(encoding).strip()


def try_int(value):
    try:
        return int(value)
    except:
        return 0

def try_float(value):
    try:
        return float(value)
    except:
        return 0.0

def removeunicode(value):
    return value.encode('ascii', 'ignore')

def tidymoney(money):
    return Decimal(sub(r'[^\d.]', '', money))

def squeezespaces(value):
    return re.sub(r"\s\s+", "", value, flags=re.UNICODE)

def removem(value):
    if 'm' in value:
        return value.replace('m', '')

def noentryprocessor(value):
    return None if value == '' else value


class RacedayItemLoader(ItemLoader):
    default_item_class = RacedayItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)
    file_urls_out = Identity()
    tf = TakeFirst()

    def race_date_time(value):
        return datetime.strptime(value, '%B %d, %Y %H:%M')

    def race_date_time_utc(value):
        #HKG is always plus 8
        return value - timedelta(hours=8)

    LocalRaceDateTime_out = Compose(Join(' '), race_date_time)
    RaceDateTime_out = Compose(Join(' '), race_date_time,race_date_time_utc)

    @classmethod
    def get_delimited_data(cls, value):
        try:
            return [s.strip() for s in cls.tf(value).strip().split(', ')]
        except:
            return []

    @classmethod
    def Surface_out(cls, value):
        data = cls.get_delimited_data(value)
        return data[0]

    @classmethod
    def RailType_out(cls, value):
        data = cls.get_delimited_data(value)
        return data[1] if data[0] != 'All Weather Track' else None

    @classmethod
    def Distance_out(cls, value):
        data = cls.get_delimited_data(value)
        return data[-2]

    int_processor = Compose(default_output_processor, try_int)

    Draw_out = int_processor
    Place_out = Compose(default_output_processor)
    HorseNumber_out = int_processor
    RaceNumber_out = int_processor
    HorseNumber_out = int_processor
    HorseWtDeclarChange_out = int_processor
    Rating_out = int_processor
    DeclarHorseWt_out = int_processor
    RatingChangeL1_out = int_processor
    SeasonStakes_out = int_processor
    Age_out = int_processor
    Distance_out = Compose(removem, int_processor)
    Owner_out = Compose(default_output_processor, squeezespaces)
    Priority_out= Compose(default_output_processor, removeunicode)
    Prizemoney_out= Compose(default_output_processor, tidymoney)
    Jockeyclaim_out = int_processor
    Wt_out = int_processor
    JockeyWtOver_out = int_processor
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################
#######################################

def getHorseReport(ir, h):
    lir = ir.split('.')
    return [e.replace(".\\n", "...") for e in lir if h in e]



def timeprocessor(value):
    #tries for each possible format
    for format in ("%S.%f", "%M.%S.%f", "%S"):
        try:
            return datetime.strptime(value, format).time()
        except:
            pass
    return None

#dead heats
def processplace(place):
    # r_dh = r'.*[0-9].*DH$'
    if place is None:
        return None
    if "DH" in place:
        return int(place.replace("DH", ''))
    else:
        return {
    "WV": 99,
    "WV-A": 99,
    "WX": 99,
    "WX-A": 99,
    "UV": 99,
    "DISQ": 99,
    "FE": 99,
    "DNF":99,
    "PU": 99,
    "TNP":99,
    "UR": 99,
    }.get(str(place), int(place))

 #add Fractionprocessor here to convert fractions to ints for SecDBL and LBW
def horselengthprocessor(value):
    #covers '' and '-'

    if '---' in value:
        return None
    elif value == '-':
        #winner
        return 0.0
    elif "-" in value and len(value) > 1:
        return float(Fraction(value.split('-')[0]) + Fraction(value.split('-')[1]))
    elif value == 'N':
        return 0.3
    elif value == 'SH':
        return 0.1
    elif value == 'HD':
        return 0.2
    elif value == 'SN':
        return 0.25
    #nose?
    elif value == 'NOSE':
        return 0.05
    elif '/' in value:
         return float(Fraction(value))
    elif value.isdigit():
        return try_float(value)
    else:
        return None

def didnotrun(value):
    if "---" in value:
        return None






# def _cleanurl(value):
#     return value

# class RaceItemsLoader(ItemLoader):
#     default_item_class = ResultsItem
    # default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class ResultsItem(scrapy.Item):
    Url = scrapy.Field()
    RacecourseCode = scrapy.Field()
    RaceDate = scrapy.Field()
    RaceNumber = scrapy.Field()
    Name = scrapy.Field()
    Place = scrapy.Field()
    PlaceNum = scrapy.Field()
    HorseNumber = scrapy.Field()
    Horse = scrapy.Field()
    HorseCode = scrapy.Field()
    Jockey = scrapy.Field()
    Trainer = scrapy.Field()
    ActualWt = scrapy.Field()
    DeclarHorseWt = scrapy.Field()
    Draw = scrapy.Field()
    LBW = scrapy.Field()
    isScratched = scrapy.Field()
    RunningPosition = scrapy.Field()
    FinishTime = scrapy.Field()
    Winodds = scrapy.Field()
    LBWFirst = scrapy.Field()
    Dayofweek = scrapy.Field()
    Sec1DBL = scrapy.Field()  #not nullable e.g. 3/4 , 1/1/4 top right of '1st Sec', '2nd Sec' box
    Sec1time = scrapy.Field() #Time object e.g. '00:00:13.24'
    Sec2DBL = scrapy.Field() #not nullable
    Sec2time = scrapy.Field() #Time object e.g. '00:00:13.24'
    Sec3DBL = scrapy.Field() #not nullable
    Sec3time = scrapy.Field() #Time object e.g. '00:00:13.24'
    Sec4DBL = scrapy.Field() #can be null
    Sec4time = scrapy.Field()#can be null
    Sec5DBL = scrapy.Field() #can be null
    Sec5time = scrapy.Field() #can be null
    Sec6DBL = scrapy.Field() #can be null
    Sec6time = scrapy.Field() #can be null
    RaceIndex = scrapy.Field()
    RaceName = scrapy.Field()
    Going = scrapy.Field()
    Prizemoney = scrapy.Field()
    Raceratingspan = scrapy.Field()
    Surface = scrapy.Field()
    Railtype = scrapy.Field()
    Raceclass = scrapy.Field()
    Distance = scrapy.Field()
    HorseReport = scrapy.Field()
    IncidentReport = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    Inracename = scrapy.Field()
    WinDiv = scrapy.Field()
    Place1Div = scrapy.Field()
    Place2Div = scrapy.Field()
    Place3Div = scrapy.Field()
    QNDiv = scrapy.Field()
    QP12Div = scrapy.Field()
    QP13Div = scrapy.Field()
    QP23Div = scrapy.Field()
    TierceDiv = scrapy.Field()
    TrioDiv = scrapy.Field()
    QuartetDiv = scrapy.Field()
    FirstfourDiv = scrapy.Field()
    ThisDouble11Div = scrapy.Field()
    ThisDouble12Div = scrapy.Field()
    Treble111Div = scrapy.Field()
    Treble112Div= scrapy.Field()
    ThisDoubleTrioDiv = scrapy.Field()
    TripleTrio111Div = scrapy.Field()
    TripleTrio112Div = scrapy.Field()
    SixUpDiv = scrapy.Field()
    SixUpBonusDiv = scrapy.Field()


class ResultsItemLoader(ItemLoader):
    default_item_class = ResultsItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)
    time_processor = Compose(default_output_processor, timeprocessor)
    horselength  = Compose(default_output_processor, horselengthprocessor)
    intprocessor = Compose(default_output_processor, try_int)
    noentry = Compose(default_output_processor, noentryprocessor)

    Winodds_out = Compose(default_output_processor, try_float)
    FinishTime_out = time_processor
    Sec1time_out = time_processor
    Sec2time_out = time_processor
    Sec3time_out = time_processor
    Sec4time_out = time_processor
    Sec5time_out = time_processor
    Sec6time_out = time_processor
    LBW_out = horselength
    Draw_out =intprocessor
    # Place_out = Compose(default_output_processor)
    HorseNumber_out = noentry
    Sec1DBL_out = horselength
    Sec2DBL_out = horselength
    Sec3DBL_out = horselength
    Sec4DBL_out = horselength
    Sec5DBL_out = horselength
    Sec6DBL_out = horselength
    RaceNumber_out = intprocessor
    HorseNumber_out = intprocessor
    DeclarHorseWt_out = intprocessor

    # image_urls_out = MapCompose(_cleanurl)
    RunningPosition_out = Join(' ')
    image_urls_out = MapCompose(lambda x: x.replace('_S.', '_L.'))
