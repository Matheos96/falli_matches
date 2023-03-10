import requests
import datetime
import setup
import pandas as pd
from os.path import exists
from pandas import json_normalize

# Compiles a list of "game rows" given a dataframe containing games
def generate_match_rows(df: pd.DataFrame) -> list[str]:
    return [f'{row["date"]} | {row["time"]} | {row["venue_name"]} | {row["category_name"]}: {row["team_A_name"]} vs. {row["team_B_name"]}\n' for _, row in df.iterrows()]

# Prints a list of strings. Each string on its own row
def print_rows(rows: list[str]) -> None:
    for r in rows:
        print(r)

# Writes a list of rows to the top of the log file
def write_rows_to_log(rows: list[str]) -> None:
    old_content = None
    if exists(setup.log_file):
        with open(setup.log_file, 'r') as file:
            old_content = file.read()
    with open(setup.log_file, 'w') as file:
        file.write(f'---------------------------- FROM SESSION: {datetime.datetime.now()} ----------------------------\n')
        file.writelines(rows)
        file.write('\n')
        if old_content:
            file.write(old_content)

def main() -> None:
    # Fetch Json data
    with requests.Session() as s:
        r = s.request('GET', setup.url, data='', headers=setup.headers, params=setup.querystring)
        json_result = r.json()

    # If we got data to work with
    if json_result and 'matches' in json_result:
        df = json_normalize(json_result['matches'])  # Put the matches Json array into a pandas dataframe
        if df.empty:
            print('No matches found! \nExiting... (Old cache unmodified. You may want to manually delete the prev.pkl file)')
            return
            
        df = df[['date', 'time', 'category_name', 'venue_name', 'team_A_name', 'team_B_name']]  # Only pick interesting columns

        session_log = []

        # If a previous data cache exists, compare and report the result
        if exists(setup.previous_data_file):
            prev_df = pd.read_pickle(setup.previous_data_file)  # Read previous result from file to dataframe 
            merged = df.merge(prev_df, how='outer', indicator=True)  # Merge previous (cached data) dataframe and current dataframe

            # Find new entries
            news = merged.loc[lambda x : x['_merge']=='left_only']
            new_match_rows = generate_match_rows(news)
            if len(new_match_rows) > 0:
                session_log.append('New matches since last run:\n')
                session_log.extend(new_match_rows)

            # Find removed entries
            removed = merged.loc[lambda x : x['_merge']=='right_only']
            removed_match_rows = generate_match_rows(removed)
            if len(removed_match_rows) > 0:
                session_log.append('\nRemoved matches since last run:\n')
                session_log.extend(removed_match_rows)
            
            # If no changes were found, make the user aware
            if len(removed_match_rows) == 0 and len(new_match_rows) == 0:
                session_log.append('No changes since last time!')
        
        # If no previous data cache was found, create one and print all the fetched data
        else:
            session_log.append('No previous data cache found. Creating a new cache for next run... All currently scheduled matches are:')
            all_match_rows = generate_match_rows(df)
            if len(all_match_rows) > 0:
                session_log.extend(generate_match_rows(df))

        # Print and log results
        print_rows(session_log)
        write_rows_to_log(session_log)

        # Save latest data to file (Overwrite previous)
        df.to_pickle(setup.previous_data_file)
    else:
        print('Something went wrong. The matches could not be fetched.')

if __name__ == '__main__':
    main()   
