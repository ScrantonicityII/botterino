import praw
from sty import fg

debug = False

roundfile = 'rounds/rounds.yaml'
archivefile = 'rounds/archive.yaml'

reddit = praw.Reddit('SuperFreakonomics', user_agent="picturegame hosting bot")
pg = reddit.subreddit('PictureGameRounds' if debug else 'PictureGame')

try:
    print(f'{fg.green}Successfully logged into reddit as {reddit.user.me()}')
except Exception as e:
    print(f'{fg.red}Unable to login to reddit. Please check praw.ini')
    print(f'{fg.red}{e}')

username = str(reddit.user.me())

donotreply = {
    'achievements-bot',
    username.lower(),
    'r-picturegame',
    'imreallycuriousbird',
}

donotupdate = True

incorrect = 'x'
