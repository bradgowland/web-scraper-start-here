import pandas as pd
from .extract import get_elements, save_data

SELECTOR = '.entry-title a'
URL = 'https://aquariumdrunkard.com/'


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


def extract(task):
    elements = get_elements(URL, SELECTOR)
    df = parse_elements(elements)
    result = save_data(df, task)

    return result
