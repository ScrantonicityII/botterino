from config import pg, username, donotupdate
from sty import fg
from Utils.utils import waitForApproval, approved, postDelay, randomColor
from Utils import update
from Loader.loader import getRound
from botterino.posterino import submitRound
from botterino.hosterino import checkAnswers
import time
import configparser

def checkType(r):
    if 'tolerance' in r and 'answer' in r:
        return "automatic"
    if 'tolerances' in r and 'answers' in r:
        return "automatic"
    if 'manual' in r:
        return 'x wrong guesses, manual correct'
    return 'manual'

parser = configparser.ConfigParser()
parser.read('praw.ini')
if not donotupdate:
    print(f'{fg.cyan}Checking for updates...')
    if update.hasUpdate():
        doUpdate = input(f'{randomColor()}There is an update available! Would you like to update? Enter Y/N ').lower() == 'y'
        if doUpdate:
            update.doUpdate()
            print(f'{fg.li_green}Successfully updated. Please restart botterino')
            exit(0)
    else:
        print(f'{fg.yellow}You are up to date!')

while True:
    print(f'{fg.yellow}Waiting for {username} to win a round... 🐌')
    waitForApproval()
    r = getRound()
    while not r:
        print(f'{fg.red}No rounds in round file! checking again in 10s')
        time.sleep(10)
        r = getRound()
    submission = submitRound(r)
    print(f'{randomColor()}Your round was posted to https://reddit.com{submission.permalink}')
    print(f'{fg.magenta}Round \'{r["title"]}\' posted in {postDelay()}s')
    print(f'{fg.cyan}Checking Answers: {checkType(r)}...')
    checkAnswers(r, submission)
    while approved():
        continue
