from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import requests


def df_from_ats():
    url = 'https://www.atsenergo.ru/results/market/fact_region'
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
    driver.get(url)
    delay = 10 # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'xml-data-row')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    dwnld_link = driver.find_element_by_xpath("//a[contains(text(),'Московская область')]").get_attribute('href')
    req = requests.get(dwnld_link, verify=False)
    return pd.read_excel(req.content, names=['date', 'hour', 'val'], skiprows=6)