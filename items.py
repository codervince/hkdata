# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#raceday has maximum fields
class RacedayItem(scrapy.Item):
    RaceDate = scrapy.Field() #used for public index only
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
    Last6runs = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    Horsename = scrapy.Field()
    Horsecode = scrapy.Field()
    ActualWt = scrapy.Field()
    Jockeyname = scrapy.Field()
    Jockeycode = scrapy.Field()
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
    YearofBirth = scrapy.Field()
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

