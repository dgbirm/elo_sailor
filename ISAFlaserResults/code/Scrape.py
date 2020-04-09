import pandas as pd
import numpy as np
from sys import exit

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from tabulate import tabulate

from text_unidecode import unidecode
import requests
import subprocess
import os

#list of qualifying regattas can be found at: https://www.sailing.org/rankings/fleet/events_included.php

#alias the raw html
santander2017 = "https://site-isaf.soticcloud.net/tools/isaf/resultsprintable/?params=YToxNDp7czo0OiJ2aWV3IjtzOjEwOiJmbGVldGV2ZW50IjtzOjEwOiJpbmNsdWRlcmVmIjtzOjE4OiJyZWdhdHRhZXZlbnRzNDE0NDciO3M6OToicHJpbnRhYmxlIjtpOjE7czoxNDoiY21zaW5jbHVkZWZpbGUiO3M6NjQ6Ii92YXIvd3d3L3Zob3N0cy9pc2FmL3Jlc3VsdF9jZW50cmUvc3lzdGVtL1Jlc3VsdENlbnRyZVBsdWdpbi5waHAiO3M6MTI6ImNtc2NsYXNzbmFtZSI7czoxODoiUmVzdWx0Q2VudHJlUGx1Z2luIjtzOjY6InJndGFpZCI7czo1OiIyMDI0OCI7czo2OiJldm50aWQiO3M6NToiMzkxNjciO3M6NjoibW9kdWxlIjtzOjQ6ImlzYWYiO3M6OToiY2FjaGV0aW1lIjtpOjMwMDtzOjQ6InR5cGUiO3M6MTM6InJlZ2F0dGFldmVudHMiO3M6NjoibGF5b3V0IjtzOjI6ImJhIjtzOjQ6InBhdGgiO3M6NDA6Ii9ob21lL2lzYWYvcHVibGljX2h0bWwvd29ybGRjdXAvcmVnYXR0YXMiO3M6ODoicm9vdHBhdGgiO3M6MTc6Ii9pc2FmL3B1YmxpY19odG1sIjtzOjc6InN1YnBhdGgiO3M6MTg6Ii93b3JsZGN1cC9yZWdhdHRhcyI7fQ%3D%3D&includeref=regattaevents41447"
deltaLloyd2017 = "http://manage2sail.com/enUS/event/b257bea1-dc41-4c2d-a767-a682da4d5002#!/results?classId=SAM004000"
keilerWoche2017 = "https://www.manage2sail.com/en-US/event/KielWeek#!/results?classId=52f483b6-a924-4c38-a612-e7d7f308d8c2"
NAs2017 = "http://rvan.ca/LaserNA/LaserNA2017.htm"
europeanMasterChampionship2017 = "*" #cant find results
PCCs2017 = "http://www.regattanetwork.com/event/14808#_newsroom+results" #copied directly
CORK2017 = "http://www.cork.org/past-results/results2017/ocr/laser_results.htm"
canadianChamps2017 = "http://www.cork.org/past-results/results2017/lasercdns/lasercdns_results.htm"
USnationals2017 = "http://www.regattanetwork.com/event/14186#_newsroom" #copied directly
midwintersWest2017 = "http://results.calyachtclub.com/RaceResults/2017/laser_mww.html"
worldCupSeriesR12017 = "https://site-isaf.soticcloud.net/worldcup/gamagori_2018.php?view=regatta&includeref=regattaevents42759&view=fleetevent&rgtaid=20510&regattaid=20510&evntid=39298&includeref=regattaevents42759#results__20510"
#need qualifying series fleet split and cant find it
worldChamps2017 = "https://sailing.laserinternational.org/regattauploads/2017/SM/2017_Std_Men_Worlds_Final_Results.htm"
CORKFR2019 = "http://www.cork.org/past-results/results2019/fall/lasers_results.htm"
EuropaCupHUN2019 = "https://byc.hu/wp-content/uploads/2019/03/LASER-EC-2-NAP-EREDM%C3%89NY.pdf"
GPLuisAlbertoCerrato2019 = "https://a883e2e5-74f8-45ae-aa7c-7972e5eedcef.filesusr.com/ugd/c4dd53_55d793e422474abe9bae049069a48b0f.pdf"
WCSR12019="https://site-isaf.soticcloud.net/worldcup/enoshima_2019.php?view=eventoa&rgtaid=21336&regattaid=21336&evntid=40832&includeref=regattaevents88952#results__21336"
worldChamps2019="https://2019worlds.laserjapan.org/standard/results/"
worldChamps2019byFinalFleet="https://sailing.laserinternational.org/regattauploads/2019/SM/2019_Std_Men_Worlds_Final_Results.htm"
keilerWoche2019="http://manage2sail.com/en-US/event/kiwo19#!/results?classId=StdM"
NAs2019="https://regattatoolbox.s3.amazonaws.com/gL0vFgqbbE_Results_156373941385"
PanAms2019="http://panamsailing.org/wp-content/uploads/2019/08/2019-PAN-AM-GAMES-SAILING-FINAL-RESULTS-BY-EVENT.pdf"
CORKOCR2019="http://www.cork.org/past-results/results2019/ocr/laser_results.htm"
ReadySteadyTokyo2019="https://site-isaf.soticcloud.net/readysteadytokyo.php?view=regatta&includeref=regattaevents88935&view=fleetevent&rgtaid=21745&regattaid=21745&evntid=41495&includeref=regattaevents88935#results__21745"
europeanMasterChampionship2019="https://eurilca.eu/documents/151/overall_LaserStandardGreen.pdf"
EuropaCupBUL2019=""#could only find picture
EuropaCupGER2019="http://manage2sail.com/en-US/event/WarnemuenderWoche2019#!/results?classId=852d998d-890e-44ac-869c-0d38c18b2cb0"
PacGames2019="https://www.samoa2019.ws/assets/990b91f2eb/Results-Laser-day-4.pdf"
TravemünderWoche2019="https://www.manage2sail.com/frch/event/300fbf46-4f0f-4616-9e52-e218ad8c9f28#!/results?classId=799efda0-bebd-49c7-bfda-045ae0206f61"
seaGames2019= "https://rs.2019seagames.com/RS2019/Charts/Accumulative/6-accumulative-result-ranking-612"
copaDeBrasil2019=""#pdf download
WorldChamps2020Entries = "http://sailingresults.net/sa/results/entrylist.aspx?ID=80326.1"
WorldChamps2020R1="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.1"
WorldChamps2020R2="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.2"
WorldChamps2020R3="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.3"
WorldChamps2020R4="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.4"
WorldChamps2020R5="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.5"
WorldChamps2020R6="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.1.6"
WorldChamps2020R7gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.7"
WorldChamps2020R7silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.7"
WorldChamps2020R7bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.7"
WorldChamps2020R8gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.8"
WorldChamps2020R8silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.8"
WorldChamps2020R8bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.8"
WorldChamps2020R9gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.9"
WorldChamps2020R9silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.9"
WorldChamps2020R9bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.9"
WorldChamps2020R10gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.10"
WorldChamps2020R10silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.10"
WorldChamps2020R10bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.10"
WorldChamps2020R11gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.11"
WorldChamps2020R11silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.11"
WorldChamps2020R11bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.11"
WorldChamps2020R12gold="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.4.12"
WorldChamps2020R12silver="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.3.12"
WorldChamps2020R12bronze="http://sailingresults.net/sa/results/race.aspx?ID=80326.1.2.12"
HempelWCMiami2020='https://site-isaf.soticcloud.net/worldcup/miami_2020.php?view=regatta&includeref=regattaevents88953&view=fleetevent&rgtaid=21002&regattaid=21002&evntid=40310&includeref=regattaevents88953#results__21002'
HempelWCEnoshima2019='https://site-isaf.soticcloud.net/worldcup/enoshima_2019.php?view=regatta&includeref=regattaevents88952&view=fleetevent&rgtaid=21336&regattaid=21336&evntid=40832&includeref=regattaevents88952#results__21336'
HempelWCMarseille2019='https://site-isaf.soticcloud.net/worldcup/regattas/marseille_2019.php?view=regatta&includeref=regattaevents88611&view=fleetevent&rgtaid=21305&regattaid=21305&evntid=40776&includeref=regattaevents88611#results__21305'
HempelWCGenoa2019raceIds={'107499':'QR1_blue', '107491':'QR1_yellow',\
    '107500': 'QR2_blue','107492':'QR2_yellow','107493':'QR3_yellow',\
    '107494':'QR4_yellow','107495':'QR5_yellow','107496':'QR6_yellow',\
    '107501': 'QR3_blue','107502': 'QR4_blue','107503': 'QR5_blue',\
    '107504': 'QR6_blue','107497':'FR7_gold','107498':'FR_medal',\
    '107505':'FR7_silver','107506':'FR8_silver'}
HempelWCGenoa2019Overall= 'https://site-isaf.soticcloud.net/worldcup/regattas/genoa_2019.php?view=regatta&includeref=regattaevents88612&view=fleetevent&rgtaid=21306&regattaid=21306&evntid=40788&includeref=regattaevents88612#results__21306'
HempelWCMiami2019Overall='https://site-isaf.soticcloud.net/worldcup/regattas/Miami_2019.php?rgtaid=21001&evntid=40299&view=fleetevent&includeref=regattaevents87424#results__21001'
HempelWCMiami2019raceIds={'107076':'QR1_yellow','107077':'QR2_yellow','107078':'QR3_blue','107079':'QR4_blue','107080':'FR5_gold','107081':'FR6_gold','107082':'FR7_gold','107083':'FR8_gold','107084':'FR9_gold','107085':'FR10_gold','107086':'FR11_gold','107087':'FR_medal','107088':'QR3_yellow','107089':'QR4_yellow','107090':'QR1_blue','107091':'QR2_blue','107092':'FR5_silver','107093':'FR6_silver','107094':'FR7_silver','107095':'FR8_silver','107096':'FR9_silver','107097':'FR10_silver'}



def main():
    currentRegatta = HempelWCMiami2019Overall
    currentRegattastr = "HempelWCMiami2019Overall"
    outfilename='/home/daniel/Desktop/elo_sailor/ISAFlaserResults/'+currentRegattastr+'.csv'

    scrapeResults(currentRegatta,currentRegattastr,outfilename)

    if os.path.exists(outfilename):
        subprocess.run(['xdg-open', outfilename], check=True)
    else:
        print("Results for "+currentRegattastr+" were not downloaded properly")

def main2():
    baseStrOut='HempelWCMiami2019'
    for i in range(107076,107098):
        url='https://site-isaf.soticcloud.net/worldcup/regattas/Miami_2019.php?view=fleetrace&rgtaid=21001&evntid=40299&raceid={}&includeref=regattaevents87424#results__21001'.format(str(i))
        currentRegatta = url
        currentRegattastr = baseStrOut + HempelWCMiami2019raceIds.get(str(i))
        outfilename='/home/daniel/Desktop/elo_sailor/ISAFlaserResults/'+currentRegattastr+'.csv'
        scrapeResults(currentRegatta,currentRegattastr,outfilename)

def cleanWhitespace(s):
    print('cleaning \n\n', s)
    if type(s)== str:
        index = s.find('  ')
        if index != -1:
            return s[:index]
    return s

def clean(df):
    df.dropna(axis = 1,inplace=True)
    df.drop_duplicates(inplace=True)
    return df
    

def scrapeResults(currentRegatta,currentRegattastr,outfilename):
    #if results as pdf
    if currentRegatta[-3:]=="pdf":
        #download the pdf to local file
        r = requests.get(currentRegatta)
        with open("/home/daniel/Desktop/ISAFlaserResults/"\
            +currentRegattastr+".pdf", 'wb') as f:
            f.write(r.content)
            f.close()

        #use zamzar script to convert to pdf to csv
        #construct bash command
        os.chdir('/home/daniel/Desktop/ISAFlaserResults')
        bashCommand = "bash ./code/zamzar.sh "+currentRegattastr+".pdf"+" csv"
        #run bash command
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error == None: #if bash executes correctly
            pass
        else:
            print("The following error was encountered while running\
                zamzar bash command: \n" + str(error))
            raise RuntimeError

        #delete pdf
        os.remove("/home/daniel/Desktop/ISAFlaserResults/"\
            +currentRegattastr+".pdf")

    else: #not a pdf    
        try:
            #Create table of results with pandas
            allTables = pd.read_html(currentRegatta)
        except Exception as e:
            print("It seems the results are hidden behind a script... lets see if we can grab them anyways")

            browser = webdriver.Firefox()
            browser.get(currentRegatta)
            sleep(2)
            innerHTML = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            browser.close()

            allTables = pd.read_html(innerHTML)
            # soup = BeautifulSoup(innerHTML, "html5lib")
            # allTables=[]
            # tables= soup.find_all('table')
            # for table in tables:
            #     df = pd.read_html(str(table))
            
            ############## CLEANUP ##############
            foo = lambda x: cleanWhitespace(x)

            for df in allTables:
                df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
                df.dropna(axis=1, how='all', thresh=None, subset=None, inplace=True)
                columns = df.columns

                for label in columns:
                    try:
                        df[label] = df[label].apply(foo)
                    except:
                        pass
                    


        # Find index of df we want assuming desired df is the largest one
        ########LARGEST############
        size = 0
        resultsTable = pd.DataFrame() #unecessary?
        try:
            for df in allTables:
                s = df.size
                if s > size:
                    size = s
                    resultsTable = df
        except Exception as e:
            for lst in allTables:
                for df in lst:
                    s = df.size
                    if s > size:
                        size = s
                        resultsTable = df

        ##############FIRST############
        # resultsTable = allTables[0]

        # # ###########SOMENUMBER##############
        # resultsTable = allTables[0]

        
        ########## Unidecode ###############
        foo2 = lambda x: unidecode(x)
        cols = resultsTable.columns

        for label in cols:
            try:
                resultsTable[label] = resultsTable[label].apply(foo2)
            except:
                pass

        print( tabulate(resultsTable, headers='keys', tablefmt='psql'))


        ########## More cleaning ###############
        clean(resultsTable)


        ######write results to output file######
        outfile = open( outfilename, 'w') #lol this is unnecessary 
        resultsTable.to_csv(outfile, index=False)
        outfile.close()


        ########## Multiple race results by fleet same page ###############

        # for x in range(3):
        #     resultsTable = allTables[x]
        #     cols = resultsTable.columns

        #     for label in cols:
        #         try:
        #             resultsTable[label] = resultsTable[label].apply(foo2)
        #         except:
        #             pass

        #     print( tabulate(resultsTable, headers='keys', tablefmt='psql'))


        #     ########## More cleaning ###############
        #     clean(resultsTable)


        #     ######write results to output file######
        #     resultsTable.to_csv('/home/daniel/Desktop/elo_sailor/ISAFlaserResults/'+currentRegattastr+str(x)+'.csv', index=False)

#########main#######

if __name__ == '__main__':
    main()



