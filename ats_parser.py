from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import requests
from datetime import date, datetime


def df_from_ats():
    url = 'https://www.atsenergo.ru/results/market/fact_region'
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
    driver.get(url)
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'xml-data-row')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    dwnld_link = driver.find_element_by_xpath("//a[contains(text(),'Московская область')]").get_attribute('href')
    req = requests.get(dwnld_link, verify=False)
    return pd.read_excel(req.content, names=['date', 'hour', 'val'], skiprows=6)


def big_nodes_prices():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
    start_date = date(2022, 9, 1)
    end_date = date(2022, 10, 31)
    dates = pd.date_range(start_date, end_date, freq='d').strftime('%Y%m%d').tolist()
    columns_name = ['date', 'hour', 'id_node', 'name_node', 'u_nom', 'u_fact', 'name_subj', 'price']
    df = pd.DataFrame(columns=columns_name)

    for day in dates:
        url = f'https://www.atsenergo.ru/nreport?rname=big_nodes_prices_pub&region=eur&rdate={day}'
        driver.get(url)
        delay = 10  # seconds
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'reports_breadcrumb')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        dwnld_link = driver.find_element_by_xpath(
            f"//a[contains(text(),'{day}_eur_big_nodes_prices_pub.xls')]").get_attribute('href')
        req = requests.get(dwnld_link, verify=False)

        dict_df = pd.read_excel(req.content, sheet_name=None, names=columns_name[2:], usecols='A:F', skiprows=2)

        for k, v in dict_df.items():
            v['hour'] = k
            v['date'] = datetime.strptime(day, '%Y%m%d').date()
            df = pd.concat([df, v], ignore_index=True)
    return df


def sell_units():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
    start_date = date(2022, 9, 1)
    end_date = date(2022, 10, 31)
    dates = pd.date_range(start_date, end_date, freq='d').strftime('%Y%m%d').tolist()
    columns_name = ['date', 'hour', 'id_gen', 'name_gen', 'id_node', 'name_node', 'tech_min', 'technol_min',
                    'down_limit', 'plan_vol', 'up_limit', 'tech_max', 'technol_max']
    df = pd.DataFrame(columns=columns_name)

    for day in dates:
        url = f'https://www.atsenergo.ru/nreport?rname=carana_sell_units&region=eur&rdate={day}'
        driver.get(url)
        delay = 10  # seconds
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'reports_files')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        dwnld_link = driver.find_element_by_xpath(
            f"//a[contains(text(),'{day}_MOSENERG_eur_sell_units.xls')]").get_attribute('href')
        req = requests.get(dwnld_link, verify=False)

        df_excel = pd.read_excel(req.content, header=None, skiprows=7, skipfooter=1)

        for h, i in zip(range(0, 24), range(4, 178, 7)):
            v = pd.concat([df_excel.iloc[:, 0:4], df_excel.iloc[:, i:i + 7]], axis=1)
            v.columns = columns_name[2:]
            v['hour'] = h
            v['date'] = datetime.strptime(day, '%Y%m%d').date()

            df = pd.concat([df, v], ignore_index=True)
    return df



