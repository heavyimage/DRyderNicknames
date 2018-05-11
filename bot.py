""" A simple bot for tweeting nicknames for Dave Ryder """

from random import choice
import logging
import time

import tweepy

from secret import *

# Setup logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:\t%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger = logging.getLogger()

# utils
def weighted_choice(choices):
    """ Define super useful weighted choice function.
    https://stackoverflow.com/a/3679780 """
    return choice(sum(([value]*weight for value, weight in choices), []))


def get_api():
    """ Access and authorize our Twitter credentials from secrets.py
    and produce api object """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    return api


class MST3K_nickname(object):
    """ A class for generating a nicknames procedurally """

    # Extracted from here: http://mst3k.wikia.com/wiki/Dave_Ryder
    first_chunks = ['big', 'blast', 'bold', 'bolt', 'brick', 'buck', 'buff',
            'butch', 'crud', 'crunch', 'dirk', 'eat', 'fist', 'flint', 'fridge',
            'gristle', 'hack', 'hunk', 'lump', 'punch', 'punt', 'reef', 'rip',
            'roll', 'slab', 'slate', 'smash', 'smoke', 'splint', 'stump',
            'thick', 'touch', 'trunk', 'whip']

    second_chunks = ['beef', 'big', 'blast', 'blow', 'bone', 'bulk', 'butt',
            'chest', 'chunk', 'dead', 'drink', 'fist', 'fizzle', 'hard', 'iron',
            'lamp', 'large', 'man', 'plank', 'punch', 'rock', 'rust', 'side',
            'slab', 'slag', 'slam', 'speed', 'squat', 'steak', 'thick',
            'thorn', 'vander']

    third_chunks = ['back', 'beef', 'body', 'bone', 'broth', 'cheek', 'cheese',
            'chest', 'chunk', 'crunch', 'face', 'fast', 'fist', 'flank',
            'groin', 'hair', 'head', 'huge', 'iron', 'jaw', 'knob', 'lift',
            'lots', 'man', 'meal', 'meat', 'men', 'muscle', 'neck', 'pec',
            'rock', 'rod', 'stag', 'steak', 'thrust']

    bob = "Bob Johnson!  Oh wait..."

    def __init__(self):
        """ Set self.name to a randomly generated (w/ weights!) nickname """

        # there's always a 1/40 chance of Bob Johnson!
        self.name = weighted_choice(
                [(self.get_name(), 39), (self.bob, 1)])

    def get_name(self):
        """ Build a name using simple logic """
        first, last = "", ""

        def get_first(self):
            """ Generate a first name """
            return choice(self.first_chunks).title()

        def get_last(self):
            """ Generate a last name """
            return "%s%s%s" % (
                # As per the original list there's a 1/39 (not conting Bob)
                # chance for a 'Mc' prefix to the lastname
                weighted_choice([("", 36), ("Mc", 3)]),
                choice(self.second_chunks).title(),
                choice(self.third_chunks))

        # Avoid the first name reappearing in the last name...
        while first.lower() in last.lower():
            first = get_first(self)
            last = get_last(self)

        # Always exclaimatory
        return "%s %s!" % (first, last)

def main():
    """ entry point """

    counter = 0

    # Main loop
    while True:

        # make
        name = MST3K_nickname().name

        # tweet
        msg = name
        get_api().update_status(msg)
        counter +=1

        # log
        logger.info("Posted name #%s: %s" % (counter, name))

        # sleep for 12 hours
        time.sleep(43200)

if __name__ == "__main__":
    main()
