from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.keys import Keys
import random

import time

from lib.snf_credentials import *


def get_driver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options = options, service=Service(GeckoDriverManager().install()))
    driver.set_window_size(500, 400)
    return driver

# Main
url = "https://finder.startupnationcentral.org/"
driver = get_driver()
driver.get(url)

def scroll_down(driver):
    html = driver.find_element_by_tag_name("html")
    html.send_keys(Keys.END)

def click_on_login_primary(driver):
    
    login_btn = driver.find_element_by_xpath("//div[@data-popup-name='login-modal']")
    webdriver.ActionChains(driver).click(login_btn).perform()
    
def click_on_login_secondary(driver):
    login_btn = driver.find_element_by_xpath("//div[@class='text js-log-in-modal pointer']")
    webdriver.ActionChains(driver).click(login_btn).perform()

def click_on_accept_terms(driver):
    terms_btn = driver.find_element_by_xpath("//input[@id='login-agree']")
    webdriver.ActionChains(driver).click(terms_btn).perform()

def click_on_login_with_email(driver):
    login_btn = driver.find_element_by_xpath("//div[@class='login-method-btn mt-24 js-login-with-email-open-modal']")
    webdriver.ActionChains(driver).click(login_btn).perform()

def insert_credentials(driver, username, password):
    action = webdriver.ActionChains(driver)
    user_field = driver.find_element_by_xpath("/html/body/div[9]/div/div/div[2]/div[2]/div/form/div[1]/div[2]/input")
    action.move_to_element(user_field).click().send_keys(username).perform()
    time.sleep(random.uniform(2,5))
    password_field = driver.find_element_by_xpath("/html/body/div[9]/div/div/div[2]/div[2]/div/form/div[1]/div[3]/input")
    action.move_to_element(password_field).click().send_keys(password).perform()

def click_on_submit(driver):
    submit_btn = driver.find_element_by_xpath("//div[@class='action-button yellow bg-yellow js-send-login']")
    webdriver.ActionChains(driver).click(submit_btn).perform()


def Login(driver):
    click_on_login_primary(driver)
    time.sleep(random.uniform(2,5))
    click_on_login_secondary(driver)
    time.sleep(random.uniform(2,5))
    click_on_accept_terms(driver)
    time.sleep(random.uniform(2,5))
    click_on_login_with_email(driver)
    time.sleep(random.uniform(2,5))
    insert_credentials(driver, USERNAME, PASSWORD)
    time.sleep(random.uniform(2,5))
    click_on_submit(driver)

