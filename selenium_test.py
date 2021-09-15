from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome('chromedriver.exe', options = options)
driver.implicitly_wait(3)

area = ['카페']

add_name = []

idx = '카페'
driver.get('https://map.kakao.com/')
driver.find_element_by_css_selector('#search.Search > form > fieldset > div > input').send_keys(idx)
driver.find_element_by_css_selector('#search.Search > form > fieldset > div > button').send_keys(Keys.ENTER)

# 로딩 시간
time.sleep(1)
html = driver.page_source
soup = bs(html,'html.parser')
www = soup.select("#info\.search\.place\.list > li:nth-child(1) > div.head_item.clickArea > strong > a.link_name")
print(www)

#
# for idx in area:
#     driver.get('https://map.kakao.com/')
#     driver.find_element_by_css_selector('#search.Search > form > fieldset > div > input').send_keys(idx)
#     driver.find_element_by_css_selector('#search.Search > form > fieldset > div > button').send_keys(Keys.ENTER)
#
#     # 여기까지 완성함
#     #while True:
#     for a in range(1):
#         html = driver.page_source
#         soup = bs(html,'html.parser')
#         www = soup.select("#info\.search\.place\.list > li:nth-child(1) > div.head_item.clickArea > strong > a.link_name")
#         print(www)
#         break
#         name = soup.select('.lsnx_det a')
#         name =' '.join(str(x) for x in name)
#         print(name)
#         soup = bs(name,'lxml')
#         a = soup.find('a').parent.text
#         add_name.append(a)
#
#         try : driver.find_element_by_css_selector('.paginate strong+a').click()
#         except : break
#         time.sleep(1)
# a = " ".join(str(x) for x in add_name)
# a = a.replace('거리뷰','')
# a = a.replace('항공뷰','')
# a = a.replace('카드','')
# a = a.replace('지번','')
# a = a.replace('올리브','\t올리브')
# a = a.split('\t')
# name = pd.DataFrame(a,columns = ['Name'])
#
# # name = name.replace (r'^\s+$',np.nan,regex=True)
# name['Name'].replace('',np.NaN,inplace = True)
# name = name.dropna(how='all')
#
#
driver.close()