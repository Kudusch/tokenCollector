import tweepy
import json
from operator import itemgetter
import datetime
import time
import curses

def gen_api_list(CONSUMER_KEY, CONSUMER_SECRET, TOKEN_FILE="tokens.json"):
    with open(TOKEN_FILE) as token_file:
        tokens = json.load(token_file)
        api_list = []
        for token in tokens:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(token["token"], token["secret"])
            api = tweepy.API(auth)
            rate_limit_status = api.rate_limit_status()
            api_list.append({
                "limit": rate_limit_status["resources"]["search"]["/search/tweets"]["remaining"],
                "reset_at": datetime.datetime.fromtimestamp(rate_limit_status["resources"]["search"]["/search/tweets"]["reset"]).strftime("%y-%m-%d %H:%M:%S"),
                "reset_in": int(rate_limit_status["resources"]["search"]["/search/tweets"]["reset"] - datetime.datetime.now().timestamp()),
                "user": api.me().screen_name})
    return(api_list)

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

api_list = gen_api_list(TOKEN_FILE="tokens.json", CONSUMER_KEY = "", CONSUMER_SECRET = "")
output_string = ""
for api in (sorted(api_list, key=itemgetter("limit", "reset_at"), reverse=True)):
    output_string = output_string + ("{limit} calls left for {user}. Reset in {reset_in} seconds at {reset_at}".format(limit=api["limit"], reset_at=api["reset_at"], reset_in=api["reset_in"], user=api["user"])) + "\n"
for i in range(60):
    if i == 59:
        stdscr.addstr(0, 0, output_string + "\nRefreshing  …")
    else:
        stdscr.addstr(0, 0, output_string + "\nRefresh in " + str(60-i).zfill(2))
    stdscr.refresh()
    time.sleep(1)