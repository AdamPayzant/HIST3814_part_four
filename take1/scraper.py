#/usr/bin/python3.9

"""
scraper.py
The webscraper for pulling the records of Canadians in the American Civil War from Ancestory

Developed by Adam Payzant
"""

import requests
from selenium import webdriver
from time import sleep
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
import os


URLBASE = 'https://www.ancestry.com/search/categories/war_civil/?pg={0}&count=50&residence=_Canada_3243'
URLBORN = 'https://www.ancestry.com/search/categories/war_civil/?pg={0}&birth=_Canada&count=50'
RESFILEPATH = 'data/residence.csv'
BORNFILEPATH = 'data/birth.csv'

def authenticate(username, password):
    print("logging in...")
    driver = webdriver.Chrome()

    driver.get("https://www.ancestry.com/secure/login")
    driver.switch_to.frame(driver.find_element_by_id("signInFrame"))
    sleep(5)
    un = driver.find_element_by_id('username')
    pw = driver.find_element_by_id('password')
    un.send_keys(username)
    pw.send_keys(password)
    login_attempt = driver.find_element_by_xpath('//*[@type="submit"]')
    login_attempt.submit()
    sleep(5)
    welcome = driver.find_element_by_xpath('//h1[@class="pageTitle"]').text
    if 'Welcome,' in welcome:
        print('successfully logged in')
        sleep(5)
        return driver
    else:
        print('something went wrong')
        driver.quit()
        return False

def scrapeResidence(driver, i):
    data = {
        "name": [],
        "residence": [],
    }
    print("Grabbing page " + str(i))
    driver.get(URLBASE.format(i))
    sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    table = soup.find_all('tbody')
    
    for entry in table:
        vals = entry.find_all('tr')
        name = ""
        residence = ""
        for val in vals:
            if val.find('th') != None:
                if val.find('th').text == "Name":
                    name = val.find('div').text
                elif val.find('th').text == "Residence":
                    residence = val.find('div').text

        if name != "" and residence != "":
            data["name"].append(name)
            data["residence"].append(residence)
    return pd.DataFrame(data)

def scrapeBorn(driver, i):
    data = {
        "name": [],
        "birth": [],
    }
    print("Grabbing page " + str(i))
    driver.get(URLBORN.format(i))
    sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    table = soup.find_all('tbody')
    
    for entry in table:
        vals = entry.find_all('tr')
        name = ""
        birth = ""
        for val in vals:
            if val.find('th') != None:
                if val.find('th').text == "Name":
                    name = val.find('div').text
                elif val.find('th').text == "Birth":
                    birth = val.find('div').text

        if name != "" and birth != "":
            data["name"].append(name)
            data["birth"].append(birth)
    return pd.DataFrame(data)

def main():
    if os.path.exists(RESFILEPATH):
        os.remove(RESFILEPATH)
    if os.path.exists(BORNFILEPATH):
        os.remove(BORNFILEPATH)

    username = ""
    password = ""

    # Just reads your log-in information from the perms file
    # You will need to make a perms files with your own log-in information
    with open("perms", 'r') as f:
        lines = f.readlines()
        password = lines[0]
        username = lines[1]
    browser = authenticate(username, password)
    if browser:
        df = scrapeResidence(browser, 1)
        for i in range(2, 101):
        #for i in range(2, 3):
            d = scrapeResidence(browser, i)
            df = df.append(d)
            sleep(3)

        df.to_csv(RESFILEPATH)

        df = scrapeBorn(browser, 1)
        for i in range(2, 101):
            d = scrapeBorn(browser, i)
            df = df.append(d)
            sleep(3)

        df.to_csv(BORNFILEPATH)
    print("Done")

if __name__ == "__main__":
    main()