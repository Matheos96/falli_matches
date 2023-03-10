from cookie import cookie  # Import cookie from cookie.py. This file needs to be manually created by the user (see README.md) 

start_date = '2023-05-01'
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