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

area = ['아파트']

add_name = []
for idx in area:
    driver.get('https://map.kakao.com/')
    driver.find_element_by_css_selector('#search.Search > form > fieldset > div > input').send_keys(idx)
    driver.find_element_by_css_selector('#search.Search > form > fieldset > div > button').send_keys(Keys.ENTER)

    html = driver.page_source
    soup = bs(html, 'html.parser')
    www = soup.select_one("ul.info.search.place.list > li > div > strong > a.name").text
    print(www)

    while True:
        html = driver.page_source
        soup = bs(html,'html.parser')
        www = soup.select_one("ul > li > div > strong > a").text
        print(www)
        name = soup.select('.lsnx_det a')
        name =' '.join(str(x) for x in name)
        print(name)
        soup = bs(name,'lxml')
        a = soup.find('a').parent.text
        add_name.append(a)

        try : driver.find_element_by_css_selector('.paginate strong+a').click()
        except : break
        time.sleep(1)
a = " ".join(str(x) for x in add_name)
a = a.replace('거리뷰','')
a = a.replace('항공뷰','')
a = a.replace('카드','')
a = a.replace('지번','')
a = a.replace('올리브','\t올리브')
a = a.split('\t')
name = pd.DataFrame(a,columns = ['Name'])

# name = name.replace (r'^\s+$',np.nan,regex=True)
name['Name'].replace('',np.NaN,inplace = True)
name = name.dropna(how='all')


driver.close()