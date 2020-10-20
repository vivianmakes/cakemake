import yaml
import random
import os
import imaging
import copy
import glob
from fuzzywuzzy import fuzz

class Player:
    def __init__(self):
        self.name = "Default"
        self.talent = 0
        self.luck = 0
        self.unluck = 0
        self.alignment = 0
        self.fame = 0
        self.icon = 'professor.png'
        self.pronoun = 'they'
        self.cheer = 0
        self.cheered_by = []
        self.wins = 0
        self.losses = 0
        self.vibe = 0
        self.reliability = 0

        self.keywords = {}

    def build_from_yaml(self, in_yaml):

        input = yaml.load(in_yaml, Loader=yaml.BaseLoader)

        self.name = input.get('name', "Default")
        self.talent = input.get('talent', random.randint(3, 7))
        self.luck = input.get('talent', random.randint(0, 8))
        self.unluck = input.get('talent', random.randint(0, 8))
        self.alignment = input.get('alignment', random.randint(-100, 100))
        self.fame = input.get('fame', 0)
        self.icon = input.get('icon', 'professor.png')
        self.pronoun = input.get('pronoun', 'they')
        self.wins = input.get('wins', 0)
        self.losses = input.get('losses', 0)
        self.vibe = input.get('vibe', random.randrange(-1,1))
        self.reliability = input.get('reliability', random.randrange(0,2))

        self.keywords = input.get('keywords', {})

    def post_match_results(self, did_win):
        # resets after a match
        self.cheer = 0
        self.cheered_by = []
        vibe_up_chance = 50

        if did_win:
            self.wins += 1
            vibe_up_chance = 75
        else:
            self.losses += 1
            vibe_up_chance = 35

        if random.randrange(1, 100) <= vibe_up_chance:
            self.vibe = ((self.vibe + 1 + 2) % 5) - 2  # Cycles: 0 -> 1 -> 2 -> -2 -> -1 -> 0
        else:
            self.vibe = ((self.vibe - 1 + 2) % 5) - 2  # Cycles: 0 -> -1 -> -2 -> 2 -> 1 -> 0

    def add_cheer(self, user_object):
        if user_object.id not in self.cheered_by:
          self.cheer += 1
          self.cheered_by.append(user_object.id)
          return True
        else:
          return False

    def get_roll(self):
        roll = random.randint(0, self.talent+self.cheer+self.vibe)
        roll += self.reliability
        return roll

    def get_vibe_emojis(self):
        msg = ""
        if self.vibe > 0:
            for i in range(0, self.vibe):
                msg += ":fire:"
        elif self.vibe < 0:
            for i in range(0, -self.vibe):
                msg += ":snowflake:"
        else:
            msg += ":white_sun_cloud:"
        return msg


    def get_luck_description(self):
        msg = "Cryptic"
        if self.luck >= 6 and self.unluck >= 6:
            msg = "Chaotic"
        elif self.luck >= 6 and self.unluck <= 2:
            msg = "Radiant"
        elif self.unluck >= 6 and self.luck <= 4:
            msg = "Ominous"
        elif self.unluck <= 3 and self.luck <= 3:
            msg = "Borin!g"
        return msg


    def get_lucky(self):
        chance = random.randint(1,100)
        if chance < self.luck:
            return True
        else:
            return False

    def get_unlucky(self):
        chance = random.randint(1,100)
        if chance < self.unluck:
            return True
        else:
            return False

    def get_sound(self):
        if "sounds" in self.keywords:
            return random.choice(self.keywords["sounds"])
        else:
            return random.choice(['BIFF!', 'POW!', 'ZOT!', 'KAPOW!', 'WOAH!', 'SLORP!'])

    def get_cake_type(self):
        if "cakes" in self.keywords:
            return random.choice(self.keywords["cakes"])
        else:
            return random.choice(['Wedding Cake', 'Bunt Cake', 'Layer Cake', 'Birthday Cake', 'Pound Cake', 'Fruit Pie', 'Ice Cream Cake', 'Tart'])

    def get_cake_flavor(self):
        if "flavors" in self.keywords:
            return random.choice(self.keywords["flavors"])
        else:
            return random.choice(['Chocolate', 'Strawberry', 'Lemon', 'Fudge', 'Apple', 'Pumpkin', 'Vanilla', 'Orange'])

    def get_cake_adjective(self):
        if "adjectives" in self.keywords:
            return random.choice(self.keywords["adjectives"])
        else:
            return random.choice(['Juicy', 'Delicious', 'Spicy', 'Beautiful', 'Small', 'Huge', 'Creamy', 'Tangy'])

    def get_verb(self):
        if "adjectives" in self.keywords:
            return random.choice(self.keywords["adjectives"])
        else:
            return random.choice(['Whips up', 'Lovingly crafts', 'Assembles', 'Bakes', 'Fries up', 'Cooks up', 'Makes', 'Readies'])

    def get_portrait_path(self):
        return imaging.get_portrait_path(self.icon)

    def get_pronoun(self, conjugation):
        if conjugation == "their" or conjugation == "his" or conjugation == "her":
            if self.pronoun == 'he':
                return 'his'
            if self.pronoun == 'she':
                return 'her'
            if self.pronoun == 'they':
                return 'their'
        elif conjugation == "they" or conjugation == "she" or conjugation == "he":
            if self.pronoun == 'he':
                return 'he'
            if self.pronoun == 'she':
                return 'she'
            if self.pronoun == 'they':
                return 'they'
        elif conjugation == "them" or conjugation == "her" or conjugation == "him":
            if self.pronoun == 'he':
                return 'him'
            if self.pronoun == 'she':
                return 'her'
            if self.pronoun == 'they':
                return 'them'

# INIT ROSTER
players = []


def get_random_pair():
    p1 = random.choice(players)
    players_minus_p1 = players.copy()
    players_minus_p1.remove(p1)
    p2 = random.choice(players_minus_p1)

    return [p1, p2]

def search_players(search_string):
    search_list = []
    for player in players:
        search_list.append({'obj':player, 'score':fuzz.partial_ratio(player.name, search_string)})

    result = None
    high_score = 35 # base ratio it must meet.
    for elem in search_list:
        if elem['score'] > high_score:
            result = elem['obj']
            high_score = elem['score']
        elif elem['score'] == high_score:
            result = None
            high_score = elem['score']
            # Copies will null each other out in case of confusion.

    return result





# LOAD ROSTER - INITIAL
initial_roster_filenames = []
potential_roster_filenames = []
for filename in glob.glob('players/*.yaml'):
    potential_roster_filenames.append(filename)

while len(initial_roster_filenames) < 6:
    choice = random.choice(potential_roster_filenames)
    initial_roster_filenames.append(choice)
    potential_roster_filenames.remove(choice)

for filename in initial_roster_filenames:
    with open(os.path.join(os.getcwd(), filename), 'r') as f: #open file in readonly
        newplayer = Player()
        newplayer.build_from_yaml(f)
        players.append(newplayer)

