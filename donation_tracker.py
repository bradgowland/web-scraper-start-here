import click
import logging
import sys
import traceback
from datetime import datetime
from dwight.dwight import post_to_slack
from tasks.export import export
from tasks.extract import extract
from tasks.new_drive import new_drive


# create new log file once monthly
log_date = str(datetime.now().date().replace(day=1))
logfile = '/mnt/disks/home/logs/donation_tracker_' + log_date + '.log'
logging.basicConfig(filename=logfile, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@click.command()
@click.option('--task', help='[new | update]')
@click.option('--drive', help='[season]_[year], ex fall_2021')
def run_task(**kwargs):
    task = kwargs['task']
    drive = kwargs['drive']

    try:
        if task == 'new':
            if drive != None:
                result = new_drive(drive)
            else:
                result = False
                print('oops! new task requires a drive name:')
                print('python donation_tracker.py --task new --drive name_YYYY')

            # this is a manual command line task, so logging errors is just clutter
            if result == True:
                log_text = 'created new drive: ' + str(drive)
                logging.warning(log_text)
        elif task == 'update':
            # run extraction
            if drive != None:
                extract_result = extract(drive)
            else:
                extract_result = False
                print('oops! update task requires a drive name:')
                print('python donation_tracker.py --task update --drive name_YYYY')

            if extract_result == True:
                log_text = 'extracted data for drive: ' + str(drive)
                logging.warning(log_text)

                # run export if extraction succeeds
                export_result = export(drive)
                if export_result == True:
                    # overall result is only true if both tasks in update succeed
                    result = True
                    log_text = 'exported data for drive: ' + str(drive)
                    logging.warning(log_text)
                else:
                    result = False
                    log_text = 'failed to export data for drive: ' + str(drive)
                    logging.warning(log_text)
            else:
                result = False
                log_text = 'failed to extract data for drive: ' + str(drive)
                logging.warning(log_text)
        elif task == 'extract':
            # run extraction
            if drive != None:
                result = extract(drive)
            else:
                result = False
                print('oops! extract task requires a drive name:')
                print('python donation_tracker.py --task update --drive name_YYYY')

            if result == True:
                log_text = 'extracted data for drive: ' + str(drive)
                logging.warning(log_text)
            else:
                log_text = 'failed to extract data for drive: ' + str(drive)
                logging.warning(log_text)
        elif task == 'export':
            # run extraction
            if drive != None:
                result = export(drive)
            else:
                result = False
                print('oops! export task requires a drive name:')
                print('python donation_tracker.py --task update --drive name_YYYY')

            if result == True:
                log_text = 'exported data for drive: ' + str(drive)
                logging.warning(log_text)
            else:
                log_text = 'failed to export data for drive: ' + str(drive)
                logging.warning(log_text)
        else:
            print('Didn''t recognize that :( Try python donation_tracker.py --help.')

        if result:
            print('Task - ' + task + ': complete :D')
        else:
            print('Task - ' + task + ': failed D:')
    except:
        log_text = 'error in ' + task  + ' task for drive: ' + str(drive)
        logging.warning(log_text)
        error = traceback.format_exc()
        post_to_slack(error)


if __name__ == '__main__':
    run_task()
