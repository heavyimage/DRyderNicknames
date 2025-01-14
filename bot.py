""" A simple bot for tooting nicknames for Dave Ryder """

from random import choice
import logging
import time
from mastodon import Mastodon

HASHTAG_INTERVAL = 10

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
    """ Access and authorize mastodon using secret token file """
    api = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://mastodon.social/'
    )
    return api

class MST3K_nickname(object):
    """ A class for generating a nicknames procedurally """

    # Extracted from here: http://mst3k.wikia.com/wiki/Dave_Ryder
    # and here: https://keeprollingrifftrax.com/2019/12/26/dave-ryder/
    first_chunks = ['bacon', 'beef', 'big', 'blast', 'blitz', 'block',
                    'boaty', 'bob', 'bold', 'bolt', 'brick', 'buck', 'buff',
                    'bulk', 'burl', 'burpy', 'butch', 'clint', 'crash',
                    'crud', 'crunch', 'dicky', 'dirk', 'earl', 'eat', 'fist',
                    'flex', 'flint', 'fridge', 'gristle', 'gunner', 'hack',
                    'herpe', 'hulk', 'hump', 'hunk', 'hunter', 'knob', 'lex',
                    'lift', 'luke', 'lump', 'lunch', 'lunk', 'max', 'much', 'pork',
                    'punch', 'punt', 'reef', 'rip', 'roll', 'rough', 'rusty',
                    'slab', 'slap', 'slate', 'smash', 'smoke', 'splint', 'stiff',
                    'storm', 'stump', 'subliterate', 'tank', 'thick', 'thump',
                    'touch', 'trunk', 'turkey', 'whip']

    second_chunks = ['ass', 'battle', 'beef', 'bench', 'big', 'blast', 'blow', 'boat', 'bone',
                    'brisk', 'bulge', 'bulk', 'butt', 'chest', 'chunk', 'cross', 'dead',
                    'doug', 'drink', 'dry', 'face', 'fist', 'fizzle', 'hand', 'hard',
                    'iron', 'kettle', 'knock', 'lamp', 'large', 'limp', 'man', 'meat',
                    'pack', 'pec', 'plank', 'puma', 'punch', 'railing', 'rock', 'roid',
                    'rust', 'schwar', 'sex', 'shake', 'shank', 'shoulder', 'side', 'slab',
                    'slag', 'slam', 'smack', 'snack', 'speed', 'squat', 'steak', 'thack',
                    'thick', 'thorn', 'thrust', 'vander']

    third_chunks = ['all', 'back', 'beef', 'bells', 'body', 'bone', 'brisket',
                    'broth', 'cheek', 'cheese', 'chest', 'chunk', 'cookie',
                    'crunch', 'face', 'fast', 'fist', 'fit', 'flank', 'groin',
                    'hair', 'head', 'hold', 'hole', 'huge', 'iron', 'jaw', 'kill',
                    'knob', 'wurst', 'lift', 'lots', 'man', 'meal', 'meat',
                    'men', 'more', 'muscle', 'neck', 'nugget', 'pants', 'pec',
                    'press', 'punch', 'rage', 'rock', 'rod', 'run', 'shaft',
                    'spread', 'squat', 'stag', 'stallion', 'steak', 'stone',
                    'sweat', 'thrust', 'wall', 'want', 'watt', 'wich', 'wurst',
                    'zenegger']

    bob = "Bob Johnson!  Oh wait..."
    beef = "Beef Brisket!"

    def __init__(self):
        """ Set self.name to a randomly generated (w/ weights!) nickname """

        # there's always a 1/40 chance of Bob Johnson!
        self.name = weighted_choice(
                [(self.make_name(), 39), (self.bob, 1), (self.beef, 1)])

    def get_name(self):
        """ Return the instance's name """
        return self.name

    def make_name(self):
        """ Build a name using simple logic """
        first, last = "", ""

        def get_first(self):
            """ Generate a first name """
            return "%s%s" % (
                    weighted_choice([("", 39), ("We put our faith in ", 1)]),
                    choice(self.first_chunks).title()
                )

        def get_last(self):
            """ Generate a last name """
            return "%s%s%s" % (
                # As per the original list there's a 1/39 (not conting Bob)
                # chance for a 'Mc' prefix to the lastname
                #
                # Can also, with low propability be "von <lastname>"
                weighted_choice([("", 35), ("Mc", 3), ("von ", 1)]),
                choice(self.second_chunks).title(),
                choice(self.third_chunks))

        # Avoid the first name reappearing in the last name...
        while first.lower() in last.lower():
            first = get_first(self)
            last = get_last(self)

        # Always exclaimatory
        return "%s %s!" % (first, last)


def get_all_followers(api):
    """ Get the accounts we are following and keep only the account names """
    accounts = []
    user_id = api.account_verify_credentials().id
    following = api.account_followers(user_id)
    while following != None :
        accounts += list(map(lambda x: x.acct, following))
        following = api.fetch_next(following)
    return accounts

def main():
    """ entry point """

    counter = 0
    followers = set()

    logger.info("Serving: https://mastodon.social/@daveryderbot")

    # get api object
    api = get_api()

    # Main loop
    while True:

        # make
        name = MST3K_nickname().get_name()

        # toot
        msg = name
        if counter % HASHTAG_INTERVAL == 0:
            msg += weighted_choice([(" #mst3k", 1), (" #rifftrax", 1)])
        api.status_post(msg)
        counter +=1

        # log
        logger.info("Posted msg #%s: %s" % (counter, msg))

        # Check for new followers:
        for handle in get_all_followers(api):
            if handle not in followers:
                logger.info("New Follower: %s" % handle)
                followers.add(handle)

        # sleep for 3 hours
        time.sleep(60 * 60 * 3)

if __name__ == "__main__":
    main()
