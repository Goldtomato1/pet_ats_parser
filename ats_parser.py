from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import requests


url = 'https://www.atsenergo.ru/results/market/fact_region'
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
driver.get(url)
time.sleep(5)
dwnld_link = driver.find_element_by_xpath("//a[contains(text(),'Московская область')]").get_attribute('href')
req = requests.get(dwnld_link, verify=False)
df = pd.read_excel(req.content, names=['date', 'hour', 'val'], skiprows=6)
