# HKDATA

*T1  
    * run server scrapyd
*T2 
    * deploy project: scrapyd-deploy scrapyd -p hkdata --version GIT
    * python auto.py (gets codes dates from CSV file)
    * curl http://localhost:6800/schedule.json -d project=hkdata -d spider=raceday -d setting=DOWNLOAD_DELAY=2 -d date="20150101" -d coursecode="ST"
    * and results
 

* Variant1:
    * to update racedaya and results data to 2 temp tables and run separate script to merge
    * update raceday RDAY and results RES data to one table
    * run from CSV file all historical meetings

* Variant2:
    * 'merge' data from both spiders (same domain using response.URL to get new URL for raceday/results)
    * single insert into PS 

* current status:
    * RDAY updates first meeting only
    * RES does not update to database

