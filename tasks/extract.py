import json
import pandas as pd
import time
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# change these for your setup as needed
OUTPUT_PATH = '/Users/bradgowland/dev/web-scraper-start-here/outputs/'
KEY_FILE = '/path/to/credentials.json'
URL = 'https://aquariumdrunkard.com/'


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


def get_elements():
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

    driver.get(URL)
    time.sleep(3)

    """
    # sample navigate login
    user, pw = get_credentials()
    driver.find_element(By.ID, 'username').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(pw)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    """

    # get page to scrape
    selector = '.entry-title a'
    elements = driver.find_elements(By.CSS_SELECTOR, selector)

    return elements


def parse_elements(elements):
    """
    accepts:
        elements: a list of selenium elements
    returns:
        df: a structured dataframe of element contents
    """
    print('parsing elements...')
    print('~~~~~~~~~~~~~~~')

    # extract text
    raw_entries = []
    for element in elements:
        raw_entries.append(element.text)

    # parse text into lists
    first_pass = True
    data_list = []
    for entry in raw_entries:
        data_list.append(entry.split(" :: "))

    # lists to dataframe
    df = pd.DataFrame(data_list)
    df.columns = ['artist', 'album']

    return df


def save_data(data):
    """
    accepts:
        data: a pandas df of page data
    returns:
        status: int, success or failure
    """
    print('saving outputs...')
    print('~~~~~~~~~~~~~~~')
    
    today = str((datetime.now() - timedelta(hours=4)).date())
    outfile = OUTPUT_PATH + today + '.csv'
    data.to_csv(outfile, index=False)

    return 1


def extract():
    elements = get_elements()
    df = parse_elements(elements)
    result = save_data(df)

    return result
