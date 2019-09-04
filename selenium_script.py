"""
selenium script to scrape google map POI with rotating IP proxy
@author: Yunbo Chen
@date: 09/02/2019
"""
import os,time
from helper import CoordBound
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.proxy import Proxy, ProxyType

# BIG_BOUND = [(38.896211, -77.032005), (38.902540, -77.018926)] # downtown test
BIG_BOUND = [(38.875, -77.072), (38.918, -77.002)]
PROXY = '5.79.73.131:13010'
# 细分
coords = CoordBound(BIG_BOUND[0][0], BIG_BOUND[0][1], BIG_BOUND[1][0], BIG_BOUND[1][1])
grids = coords.dividify()
print("total number of grids: {}".format(len(grids)))
# print(grids)

# chrome webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

# start
driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
driver.get('localhost:5000')
time.sleep(2)
index = 0
# driver.get('http://whatismyipaddress.com')
# while (index < 10):
#     driver.get('http://whatismyipaddress.com')
#     # driver.execute_script("window.open('http://whatismyipaddress.com');")
#     time.sleep(2)
#     driver.quit()
#     driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    # driver.switch_to_window(driver.window_handles[0])

# for grid in grids[162:]:
while index < len(grids):
    grid = grids[index]
    print("scarping index: {}\ngrid : {}".format(index, grid))
    if index > 0 and index % 6 == 0:
        # restart driver to change IP
        driver.quit()
        driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        driver.get('localhost:5000')
        time.sleep(2)
    # call it
    try: 
        driver.execute_script('continueSearch({},{},{},{});'.format(
            grid.sw_lat, grid.sw_lng, grid.ne_lat, grid.ne_lng
        ))
        wait = WebDriverWait(driver, 180)
        out = wait.until(ec.text_to_be_present_in_element((By.ID, 'soutput'), '{},{},{},{}: done'.format(
            grid.sw_lat, grid.sw_lng, grid.ne_lat, grid.ne_lng
        )))
        print("done grid index {}".format(index))
        index += 1
    except TimeoutException:
        continue
    except JavascriptException:
        # page not loaded properly
        continue
    
