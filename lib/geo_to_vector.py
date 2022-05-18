
import pandas as pd
import numpy as np
import random 
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def listify_geo_markets(df):
    l = []
    for i,val in enumerate(df['geographical markets']):
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



def get_world_pop(driver: webdriver.WebDriver) -> int :
    """Get world population by scraping www.worldometers.info"""
    
    

    url = "https://www.worldometers.info/world-population/"
    driver.get(url)
    population = driver.find_element(By.CLASS_NAME, "maincounter-number").text
    
    pop = population.split(',')
    num = ''.join(pop)
    return int(num)



def get_countries_population(driver: webdriver.WebDriver) -> dict:
    """Get countries population by scraping www.worldometers.info"""
    
    
    
    url = "https://www.worldometers.info/world-population/population-by-country/"
    driver.get(url)
    d = {}
    table = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    for row in table:
        elements = row.find_elements(By.TAG_NAME, "td")
        d.update({elements[1].text.lower(): elements[2].text.lower()})
    
    
    return d
    


def get_not_in_list_data(driver: webdriver.WebDriver, l: list):
    d = {}
    
    url = "https://www.worldometers.info/world-population/"  #  "western-europe-population/"
    postfix=['','ern']
    americas_population = 0

    for country in l:

        if country == 'americas':
            driver.get(f'{url}latin-america-and-the-caribbean-population')
            time.sleep(random.uniform(0.5,1.5))
            americas_population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            time.sleep(random.uniform(5,8))
            driver.get(f'{url}northern-america-population')
            time.sleep(random.uniform(0.5,1.5))
            americas_population += int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            d.update({country: americas_population})

        elif country == 'southeast asia':
            driver.get(f'{url}south-eastern-asia-population')
            population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
            d.update({country: population})

        elif country.count(' ') == 0:
            try:
                new_url = f"{url}{country}-population"
                driver.get(new_url)
                time.sleep(random.uniform(0.5,1.5))
                population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
                if population is not None:
                    d.update({country: population})
                    continue
                    
            except Exception as e:
                pass
                # print("Error on "+ new_url)
                # print(str(e))
        else:
            sp_index = country.rindex(' ')
            for p in postfix:
                try:
                    newcountry = f"{country[:sp_index]}{p}{country[sp_index:]}"
                    new_url = url+ "-".join(newcountry.split(' '))+'-population'
                    driver.get(new_url)
                    time.sleep(random.uniform(0.5,1.5))
                    population = int(''.join(driver.find_element(By.CLASS_NAME, "maincounter-number").text.split(',')))
                    if population is not None:
                        d.update({country: population})
                        break
                    
                except:
                    # print("Error on "+ new_url)
                    continue
        
        time.sleep(random.uniform(5,8))
            


    
    return d



def vectorize_geo(dataframe: pd.DataFrame) -> pd.DataFrame: 
    df = dataframe.copy()
    driver = get_driver()

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
    
    country_pop.update(get_not_in_list_data(driver, not_in_list))
    


    # Convert all strings to int and compute percentage

    world_population = country_pop['global']
    country_pop_percent = {}
    for key,val in country_pop.items():

        if type(val) == str:
            popu = val.split(',')
            country_pop_percent.update({key : int(''.join(popu)) / world_population})
        elif type(val) == int:
            country_pop_percent.update({key : val / world_population})

    # Add a 'geo_market_per' to the df

    for i, list in enumerate(df['geographical markets']):
        sum = 0
        if list is not np.nan :
            for country in list :
                if country in country_pop_percent.keys() :
                    sum += country_pop_percent[country]
            df.loc[i,'geo_market_per'] = sum if sum < 1 else 1

    driver.quit()
    return df


