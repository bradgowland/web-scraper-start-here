import json
import os
import pandas as pd
from datetime import datetime, timedelta
from tasks.schedule_template import schedule_template

BASE_PATH = '/mnt/disks/home/donation_tracker/'
KEY_FILE = '/mnt/disks/home/donation_tracker/drive_keys.json'

def get_dates(drive_key):
    # check key file for a drive, get dates if drive exists
    with open(KEY_FILE) as json_file:
        keys = json.load(json_file)

    try:
        drive = keys[drive_key]['drive']
        drive_start = keys[drive_key]['start_date']
        drive_end = keys[drive_key]['end_date']
    except KeyError:
        print("Sorry, check your drive name and dates D:")

        return False

    start_dt = datetime.strptime(drive_start, '%Y-%m-%d').date()
    end_dt = datetime.strptime(drive_end, '%Y-%m-%d').date()

    delta = end_dt - start_dt
    drive_dates = []
    for i in range(0, delta.days + 1):
        drive_dates.append(str(start_dt + timedelta(days=i)))

    return drive_dates


def create_files(drive, drive_dates):
    # load template
    schedule_df = pd.DataFrame(schedule_template)

    # check paths, write new schedule if empty
    path = BASE_PATH + drive
    if not os.path.exists(path):
        os.mkdir(path)
        print('created new directory:')
        print(path)
        print('*~*~*~*~*~*~*~*')

        for drive_date in drive_dates:
            path = BASE_PATH + drive + '/' + drive_date + '.csv'
            if not os.path.exists(path):
                schedule_df.to_csv(path, index=False)

                print('created new file:')
                print(path)
                print('*~*~*~*~*~*~*~*')
    else:
        print('file strucutre for drive:', drive)
        print('already exists.')
        print('*~*~*~*~*~*~*~*')

        return False

    return True


def new_drive(drive):
    drive_dates = get_dates(drive)

    if drive_dates:
        result = create_files(drive, drive_dates)

        if result:
            print('set up files for new drive')
    else:
        return False
        
    return True
