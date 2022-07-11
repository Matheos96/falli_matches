from os.path import exists
from pandas import json_normalize
from cookie import cookie  # Import cookie from cookie.py. This file needs to be manually created by the user (see README.md) 
import requests
import datetime
import pandas as pd

# SETUP
start_date = '2022-07-08'
url = 'https://spl.torneopal.net/taso/rest/getMatches'
querystring = {'start_date':start_date,'venue_location_id':'2397','tpid':'1667178516'}
headers = {
    "cookie": cookie,
    "authority": "spl.torneopal.net",
    "accept": "json/df8e84j9xtdz269euy3h",
    "accept-language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
    "if-modified-since": "Thu, 01 Jan 1970 00:00:00 GMT",
    "if-none-match": "^\^44ed893f7b8d2f86df14e300ab21b2a5^^",
    "origin": "https://tulospalvelu.palloliitto.fi",
    "referer": "https://tulospalvelu.palloliitto.fi/",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
previous_data_file = 'prev.pkl'
log_file = 'Falli_matches_log.txt'

# Compiles a list of "game rows" given a dataframe containing games
def get_game_rows(df: pd.DataFrame):
    return [f'{row["date"]} | {row["time"]} | {row["venue_name"]} | {row["category_name"]}: {row["team_A_name"]} vs. {row["team_B_name"]}\n' for _, row in df.iterrows()]

# Prints a list of strings. Each string on its own row
def print_rows(rows):
    for r in rows:
        print(r)

# Writes a list of rows to the log file
def write_rows_to_log(rows):
    with open(log_file, 'a+') as file:
        file.write(f'---------------------------- FROM SESSION: {datetime.datetime.now()} ----------------------------\n')
        file.writelines(rows)
        file.write('\n')

if __name__ == '__main__':
    # Fetch Json data
    with requests.Session() as s:
        r = s.request('GET', url, data='', headers=headers, params=querystring)
        json_result = r.json()

    # If we got data to work with
    if json_result and 'matches' in json_result:
        # Put the matches Json array into a pandas dataframe
        df = json_normalize(json_result['matches'])
        df = df[['date', 'time', 'category_name', 'venue_name', 'team_A_name', 'team_B_name']]  # Only pick interesting columns

        to_log = []  # List to keep all rows to be written to log

        # Read previous result from file to dataframe (if file exists)
        if exists(previous_data_file):
            prev_df = pd.read_pickle(previous_data_file)

            # Merge previous and current
            merged = df.merge(prev_df, how='outer', indicator=True)

            # Find new entries
            news = merged.loc[lambda x : x['_merge']=='left_only']
            new_game_rows = get_game_rows(news)
            if len(new_game_rows) > 0:
                to_log.append('New games since last run:\n')
                to_log.extend(new_game_rows)

            # Find removed entries
            removed = merged.loc[lambda x : x['_merge']=='right_only']
            removed_game_rows = get_game_rows(removed)
            if len(removed_game_rows) > 0:
                to_log.append('\nRemoved games since last run:\n')
                to_log.extend(removed_game_rows)
            
            if len(removed_game_rows) == 0 and len(new_game_rows) == 0:
                to_log.append('No changes since last time!')
        else:
            to_log.append('No previous data cache found. Creating a new cache for next run... All currently scheduled games are:')
            all_game_rows = get_game_rows(df)
            if len(all_game_rows) > 0:
                to_log.extend(get_game_rows(df))

        # Print and log results
        print_rows(to_log)
        write_rows_to_log(to_log)

        # Save latest data to file (Overwrite previous)
        df.to_pickle(previous_data_file)
    else:
        print('Something went wrong. The games could not be fetched.')   
