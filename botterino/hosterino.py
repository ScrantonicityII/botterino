from geopy.distance import distance
from geopy.point import Point
from config import donotreply, incorrect, reddit, username, pg
from itertools import permutations
import re
from sty import fg
from Utils.utils import decimal, getComments, getDistance, randomColor


def withinTolerance(guess, answer, tolerance):
    return distance(guess, answer).m <= tolerance

def checkCoordinates(guess, answer, tolerance):
    answer = Point(answer)
    error = getDistance(guess.body, answer)
    if error is None:
        print(f"{randomColor()}Could not find a coordinate in guess '{guess.body}' by {guess.author}")
        return 'ignore'
    error = round(error, 2)
    print(f'{randomColor()}{guess.author}\'s guess {guess.body} was {error} meters off')
    return error <= tolerance

def checkAnswers(r, submission):
    tolerance, manual, after, text, answer = float(r.get('tolerance', 0)), r.get(
        'manual'), r.get('after'), r.get('text'), r.get('answer')
    if not tolerance:
        return
    for c in getComments(submission):
        result = True
        r = checkCoordinates(c, answer, tolerance)
        if r == 'ignore':
            continue
        result = result and r

        if not result:
            c.reply(incorrect)
        if result:
            if manual:
                print(f"{randomColor()}Guess '{c.body}' looks correct, but you will have to check it out.")
            else:
                plusCorrect = c.reply('+correct')
                print(f'{randomColor()}Corrected {c.author} in {plusCorrect.created_utc - c.created_utc}s')
                break
    if after:
        submission.reply(after)
        print(f'{randomColor()}Posted your message after the round: {after}')

