
import pandas as pd
import numpy as np
import random 
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_chrome_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def get_firefox_driver():
    options = webdriver.FirefoxOptions()
    # options.headless = True
    driver = webdriver.Firefox(options = options, service=Service(GeckoDriverManager().install()))
    return driver


def listify_geo_markets(df):
    l = []
    for val in df['geographical markets']:
        if val is not np.nan:
            l.append(val.split(', '))
        else :
            l.append(np.nan)
    return l


def get_location_list(df: pd.DataFrame)-> list : 
    countries = []
    for list in df['geographical markets']:
        if list is not np.nan:
            for country in list:
                if country not in countries:
                    countries.append(country.lower())
    
    return countries



def get_world_pop(driver) -> int :
    """Get world population by scraping www.worldometers.info"""

    url = "https://www.worldometers.info/world-population/"
    driver.get(url)
    time.sleep(random.uniform(1,2))

    population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
    return int(population)



def get_countries_population(driver) -> dict:
    """Get countries population by scraping www.worldometers.info"""
    
    
    
    url = "https://www.worldometers.info/world-population/population-by-country/"
    driver.get(url)
    time.sleep(random.uniform(1,2))
    d = {}
    table = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    for row in table:
        elements = row.find_elements(By.TAG_NAME, "td")
        d.update({elements[1].text.lower(): int(''.join(elements[2].text.split(',')))})
    
    time.sleep(random.uniform(1,2))
    return d
    


def get_not_in_list_data(driver, l: list):
    ret_list = []
    
    url = "https://www.worldometers.info/world-population/"  #  "western-europe-population/"
    postfix=['','ern']

    for country in l:

        if country == 'americas':
            driver.get(f'{url}latin-america-and-the-caribbean-population')
            time.sleep(random.uniform(0.5,1.5))
            americas_population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            time.sleep(random.uniform(5,8))
            driver.get(f'{url}northern-america-population')
            time.sleep(random.uniform(0.5,1.5))
            americas_population += int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            ret_list.append(americas_population)

        elif country == 'southeast asia':
            driver.get(f'{url}south-eastern-asia-population')
            population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            ret_list.append(population)

        elif country.count(' ') == 0:
            try:
                new_url = f"{url}{country}-population"
                driver.get(new_url)
                time.sleep(random.uniform(0.5,1.5))
                population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
                ret_list.append(population)
                    
            except Exception as e:
                print("Error on "+ new_url)
                print(str(e))
        else:
            sp_index = country.rindex(' ')
            for p in postfix:
                try:
                    newcountry = f"{country[:sp_index]}{p}{country[sp_index:]}"
                    new_url = url+ "-".join(newcountry.split(' '))+'-population'
                    driver.get(new_url)
                    time.sleep(random.uniform(0.5,1.5))
                    population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
                # if population is not None:
                    ret_list.append(population)
                    break
                    
                except:
                    # print("Error on "+ new_url)
                    continue
        
        time.sleep(random.uniform(5,8))
             
    return ret_list



def vectorize_geo(dataframe: pd.DataFrame, browser='') -> pd.DataFrame: 
    df = dataframe.copy()

    if browser.lower() == 'c' or browser.lower() == 'chrome':
        driver = get_chrome_driver()
    else:
        driver = get_firefox_driver()

    df['geographical markets'] = listify_geo_markets(df)
    countries = get_location_list(df)
    country_pop = get_countries_population(driver)


    # Adjust necessary keys according to the dataframe 

    dict_update = {'palestine':'State of Palestine','macedonia':'North Macedonia','myanmar (burma)':'myanmar',
    "cote d'ivoire":"côte d'ivoire", 'czech republic':'Czech Republic (Czechia)', 'swaziland': 'eswatini'}

    for key,val in dict_update.items():
        country_pop.update({key.lower():country_pop[val.lower()]})

    country_pop.update({'global' : get_world_pop(driver)})
    country_pop.update({'north asia' : country_pop['russia']})


    # find all missing elements from the 'geographical markets column in the dataframe 
    not_in_list = []

    for country in countries:
        if country not in country_pop.keys():
            not_in_list.append(country)
    
    not_in_list_res = get_not_in_list_data(driver, not_in_list)


    for key, val in zip(not_in_list, not_in_list_res):
        country_pop.update({key: val})
    


    # Convert all strings to int and compute percentage

    world_population = country_pop['global']
    country_pop_percent = {}
    for key,val in country_pop.items():

        if type(val) == int:
            country_pop_percent.update({key : val / world_population})
        else:
            print(type(val))
            country_pop_percent.update({key : 0})

    # Add a 'geo_market_per' to the df
    per_list = []
    geo_list = df['geographical markets'].tolist()
    for list in geo_list:
        sum = 0
        if len(list)>0 :
            for country in list :
                if country in country_pop_percent.keys() :
                    sum += country_pop_percent[country]
            per_list.append(sum if sum < 1 else 1)
        else:
            per_list.append(np.nan)

    driver.quit()
    df['geo_market_per'] = per_list
    print(f"shape of df['geo_market_per']: {df['geo_market_per'].shape}")
    return df


