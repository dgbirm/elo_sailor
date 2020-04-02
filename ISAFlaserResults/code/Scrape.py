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
ReadySteadyTokyo2019="https://tokyo2020.org/en/special/readysteadytokyo/sailing/data/Men's_One_Person_Dinghy-Laser_as_of_22_AUG_at_1653.pdf"
europeanMasterChampionship2019="https://eurilca.eu/documents/151/overall_LaserStandardGreen.pdf"
EuropaCupBUL2019=""#could only find picture
EuropaCupGER2019="http://manage2sail.com/en-US/event/WarnemuenderWoche2019#!/results?classId=852d998d-890e-44ac-869c-0d38c18b2cb0"
PacGames2019="https://www.samoa2019.ws/assets/990b91f2eb/Results-Laser-day-4.pdf"
TravemünderWoche2019="https://www.manage2sail.com/frch/event/300fbf46-4f0f-4616-9e52-e218ad8c9f28#!/results?classId=799efda0-bebd-49c7-bfda-045ae0206f61"
seaGames2019= "https://rs.2019seagames.com/RS2019/Charts/Accumulative/6-accumulative-result-ranking-612"
copaDeBrasil2019=#pdf download


currentRegatta = seaGames2019
currentRegattastr = "seaGames2019"
outfilename='/home/daniel/Desktop/ISAFlaserResults/'+currentRegattastr+'.csv'

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

        def clean(s):
            print('cleaning \n\n', s)
            if type(s)== str:
                index = s.find('  ')
                if index != -1:
                    return s[:index]
            return s
        foo = lambda x: clean(x)

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

    # ##############FIRST############
    # resultsTable = allTables[0]

    # ###########SOMENUMBER##############
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

    ######write results to output file######
    outfile = open( outfilename, 'w')
    resultsTable.to_csv(outfile)
    outfile.close()

if os.path.exists(outfilename):
  subprocess.run(['xdg-open', outfilename], check=True)
else:
  print("Results for "+currentRegattastr+" were not downloaded properly")



