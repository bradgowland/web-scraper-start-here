import json
import os
import time
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# change these for your setup as needed
load_dotenv()
OUTPUT_PATH = os.environ.get("OUTPUT_PATH")
KEY_FILE = os.environ.get("KEY_FILE")


"""
NOT CURRENTLY USING THIS
but it's a good template for handling login stuff
"""
def get_credentials():
    """
    accepts: (none)
    returns:
        user, pw: ordered pair of credentials from json file
    """
    print('fetching credentials...')
    print('~~~~~~~~~~~~~~~')

    with open(KEY_FILE) as json_file:
        keys = json.load(json_file)

    try:
        user = keys['user']
        pw = keys['pw']
    except KeyError:
        print("Sorry, check your key file D:")

        return 0

    return user, pw


def get_elements(url, selector):
    """
    accepts: (none)
    returns: status, int value of success / fail
    """
    print('scraping webpage...')
    print('~~~~~~~~~~~~~~~')

    # set up web driver
    options = webdriver.ChromeOptions()
    # you can toggle below if you don't want to see the webpage
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options)

    driver.get(url)
    time.sleep(3)

    """
    # sample navigate login
    user, pw = get_credentials()
    driver.find_element(By.ID, 'username').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(pw)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    """

    # get page to scrape
    elements = driver.find_elements(By.CSS_SELECTOR, selector)

    return elements


def save_data(data, prefix):
    """
    accepts:
        data: a pandas df of page data
        prefix: a string identifier for the filename
    returns:
        status: int, success or failure
    """
    print('saving outputs...')
    print('~~~~~~~~~~~~~~~')
    
    today = str((datetime.now() - timedelta(hours=4)).date())
    outfile = OUTPUT_PATH + prefix + '_' + today + '.csv'
    data.to_csv(outfile, index=False)

    return 1
