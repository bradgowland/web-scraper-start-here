import json
import numpy as np
import pandas as pd
import requests
import shutil
import time
from glob import glob
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


BASE_PATH = '/mnt/disks/home/donation_tracker/'
DRIVER_PATH = '/usr/local/bin/chromedriver'
KEY_FILE = '/mnt/disks/home/donation_tracker/drive_keys.json'
URL = 'https://michiganradio.secureallegiance.com/wuom/DonationTracker/Tracker.aspx?CAMPCODE&#61;WINTER22'


def get_credentials(drive_key):
    with open(KEY_FILE) as json_file:
        keys = json.load(json_file)

    try:
        drive = keys[drive_key]['drive']
        pw = keys[drive_key]['pw']
    except KeyError:
        print("Sorry, check your drive name D:")

        return False

    return [drive, pw]


def get_data(drive, pw):
    # set up web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    driver.get(URL)
    time.sleep(3)

    # navigate login
    driver.find_element(By.ID, 'ddCampaign').send_keys(drive)
    driver.find_element(By.ID, 'txtPassword').send_keys(pw)
    driver.find_element(By.ID, 'txtPassword').send_keys(Keys.RETURN)

    # switch to hourly page
    selector = '.igtab_BHTabSel+ .igtab_BHTab .igtab_BHCenter'
    driver.find_element(By.CSS_SELECTOR, selector).click()
    time.sleep(3)

    # the page can take a while to fetch values - limited retry loop until something loads
    for i in range(0,5):
        # get table data
        selector = '.igg_Item td'
        table_elements = driver.find_elements(By.CSS_SELECTOR, selector)
        table_data = []
        for element in table_elements:
            table_data.append(element.text)

        # clean and shape
        filtered_data = np.array(list(filter(lambda x: x != '', table_data)))
        shaped_data = filtered_data.reshape(26,5)[:24]
        columns = [
            'hour',
            'total_ct',
            'total_amt',
            'new_ct',
            'new_amt'
        ]
        clean_df = pd.DataFrame(shaped_data, columns=columns)

        # check for results, looks for any total donors
        if clean_df.iloc[-1]['total_ct'] == '0':
            print('no results yet... waiting for another try')
            time.sleep(6)
            continue
        else:
            break

    return clean_df


def save_data(drive_key, data):
    today = str((datetime.now() - timedelta(hours=4)).date())
    outfile = BASE_PATH + drive_key + '/' + today + '.csv'
    data.to_csv(outfile, index=False)

    return True


def extract(drive_key):
    # fetch credentials by drive name
    credentials = get_credentials(drive_key)
    if credentials == False:
        return False

    # scrape data
    drive = credentials[0]
    pw = credentials[1]
    data = get_data(drive, pw)

    # save out
    result = save_data(drive_key, data)

    return result
