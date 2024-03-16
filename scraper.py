import click
import logging
import logging.handlers as handlers
from pathlib import Path
from datetime import datetime
from tasks.extract import extract


# get a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# format logs and set to rotate weekly, keep for six weeks
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
LOG_FILE = str(Path.home()) + '/logs/scraper.log'
logHandler = handlers.TimedRotatingFileHandler(LOG_FILE, when='W0', interval=6, backupCount=5)

# apply log config
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

@click.command()
@click.option('--task', help='[run]')
def run_task(**kwargs):
    task = kwargs['task']

    if task == 'run':
        result = extract()
        log_msg = task + ' complete with status ' + str(result)
        logger.info(log_msg)
    else:
        print('valid --task names are [run]')


if __name__ == '__main__':
    run_task()
