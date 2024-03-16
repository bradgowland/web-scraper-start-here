import json
import pandas as pd
from apiclient.discovery import build
from glob import glob
from oauth2client.service_account import ServiceAccountCredentials

API_NAME = 'sheets'
API_VERSION = 'v4'
BASE_PATH = '/mnt/disks/home/donation_tracker/'
KEY_FILE = '/mnt/disks/home/resources/data_api_client_secrets.json'
RANGE_NAME = "data!A2:F"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1uP3oVj6WAJ61DmCkkjIv_9SmFCEm59-okOVusFL1FMs'


def aggregate(drive):
    file_paths = glob(BASE_PATH + drive + '/*')
    first_pass = True
    for path in file_paths:
        try:
            donation_df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            continue

        # add date from filepath to dataframe
        donation_df
        donation_df['date'] = path[-14:-4]

        # append dataframe to full dataset
        if first_pass == True:
            all_data = donation_df
            first_pass = False
        else:
            all_data = pd.concat([all_data, donation_df])

    # sort by date, then hour
    all_data = all_data.sort_values(by = ['date', 'hour'], ascending = [True, True])

    # move date to first column
    cols = ['date', 'hour', 'total_ct', 'total_amt', 'new_ct', 'new_amt']
    all_data = all_data[cols]

    return all_data


def sheets_init():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            KEY_FILE, scopes=SCOPES)
    service = build(API_NAME, API_VERSION, credentials=credentials, cache_discovery=False)
    sheets_api = service.spreadsheets()

    return sheets_api


def sheets_write(**kwargs):
    data = kwargs['data']
    range = kwargs['range']
    sheet_id = kwargs['sheet_id']
    sheets_api = kwargs['sheets_api']
    body = {
        'values': data
    }

    result = sheets_api.values().update(
        spreadsheetId=sheet_id, range=range,
        body=body, valueInputOption='USER_ENTERED').execute()

    result_msg = str(result.get('updatedCells')) + ' cells updated'
    return result_msg


def post_to_sheets(schedule_df):
    print('Wrtiting donation data to sheets...')

    schedule_json = schedule_df.to_json(orient='values')
    schedule_json = json.loads(schedule_json)

    sheets_api = sheets_init()
    result = sheets_write(data=schedule_json, range=RANGE_NAME, sheet_id=SHEET_ID, sheets_api=sheets_api)

    return True


def export(drive):
    aggregated_data = aggregate(drive)
    result = post_to_sheets(aggregated_data)

    return True


if __name__ == '__main__':
    drive = 'fall_2021'
    export(drive)
