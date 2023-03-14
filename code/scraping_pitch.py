# import libraries
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import sleep
import os

# data dir
path = 'C:/Users/nsbea/OneDrive/4_coding/wbc/data'
file_name = '0310_korea.csv'

df_path = os.path.join(path, file_name)

# set games url
url = 'https://baseballsavant.mlb.com/gamefeed?date=3/10/2023&gamePk=719532&chartType=pitch&legendType=pitchName&playerType=pitcher&inning=&count=&pitchHand=&batSide=&descFilter=&ptFilter=&resultFilter=&hf=pitchVelocity&sportId=51#719532'
i = 'pitchVelocityTable_' + url[-6:]


# open webdriver
driver = webdriver.Chrome('C:/Users/nsbea/OneDrive/4_coding/webscraping/chromedriver_win32/chromedriver')

# url
driver.get(url)

# get html
html = driver.page_source

# close 
driver.close()

# get html from the webpage
soup = BeautifulSoup(html, 'html.parser')

# get title
title = soup.find('title')
print(title)

#get div
div = soup.find(id = i)

# get table
table = div.find_all('table')[0]
rows =table.findAll('tr')

# save the data
os.chdir(path)

import csv
with open(df_path, "w",encoding="utf-8") as file:
    writer = csv.writer(file)
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)