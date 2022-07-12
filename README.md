# Falli Matches - A Tulospalvelu web scraper
_Requires Python >= 3.6_

## Setup
1. Install the requirements
```console
$ python -m pip install -r requirements.txt
```
2. Use Postman or Insomnia (or whatever) to GET ```https://spl.torneopal.net/taso/rest/getMatches```. Copy the cookie in from the response ("TASO_palloliitto=....")
3. Create the file ```cookie.py``` in the script's working directory and define the variable ```cookie```. Give the variable the cookie value you copied in the previous step.

Example ***cookie.py***
```
cookie = 'TASO_palloliitto=...morejibberish...'
```

## Usage
```console
$ python falli_matches.py
```
The script will print the results to the console as well as write a log to the file ```Falli_matches_log.txt``` which is prepended to after each run.
