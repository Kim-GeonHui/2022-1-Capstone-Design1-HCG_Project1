from lib2to3.pgen2 import driver
import selenium
from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat
import csv
import math

rank_list = []
title_list = []
singer_list = []

count = 0

for i in range(1,13):
  
  driver = wd.Chrome('C:\chromedriver')
  driver.maximize_window()

  url = 'https://www.melon.com/chart/index.htm'
  h = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
  driver.get(url)

  driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span').click()

  driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[2]/a').click()
  time.sleep(1)

  driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[1]/span/label').click()
  time.sleep(1)

  driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[3]/span/label').click()
  time.sleep(1)

  driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li[%s]/span/label' % i).click()
  time.sleep(1)

  driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[6]/span/label').click()
  time.sleep(1)

  driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()
  time.sleep(1)

  html = driver.page_source 
  soup = BeautifulSoup(html, 'html.parser')

  rank = soup.select('tbody tr td div.wrap.right_none span.rank')
  title = soup.select('tbody tr td div.wrap div div.ellipsis.rank01 a')
  singer = soup.select('tbody tr td div.wrap_song_info div div.ellipsis.rank02 > span.checkEllipsis')

  for j in rank:
    rank_list.append(j.text)

  for j in title:  
    if (i == 10):
      if (count != 56):
        title_list.append(j.text)
      else:
        title_list.append('')
      count += 1
    else:
      title_list.append(j.text)
    
    
  for j in singer:
    singer_list.append(j.text)
    
  driver.close()
  driver.quit()

total_list = []
for j in range(1200):
  total_list.append([math.trunc(j/100 + 1), rank_list[j], title_list[j], singer_list[j]])

with open('melon.csv', 'w', encoding='CP949', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(['월', '순위', '타이틀', '가수'])
  writer.writerows(total_list)