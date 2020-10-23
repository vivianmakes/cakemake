import random
import messaging
import roster
from config import config
import judges
import prose

class Gameshow():
    def __init__(self, p1, p2):
        self.participant1 = p1
        self.participant2 = p2
        p1.on_added_to_show(self)
        p2.on_added_to_show(self)
        self.minutes_until_resolve = config.interval

    def get_participant_list(self):
        return [self.participant1, self.participant2]

    async def finish_show(self):
        p1 = self.participant1
        p2 = self.participant2

        result = judges.judge(p1, p2)

        await messaging.send_victory_message(result)

        p1.post_match_results(result.winner is p1)
        p2.post_match_results(result.winner is p2)
        p1.on_show_end(self)
        p2.on_show_end(self)


shows = []


async def start_show(p1, p2):
    global shows

    show = Gameshow(p1, p2)
    await messaging.send_versus_message(p1, p2)
    shows.append(show)
    return show


async def cheer(player_object, user_object):
    res = player_object.add_cheer(user_object)
    return res


async def start_random_show():
    matchup = roster.get_matchup()
    p1 = matchup[0]
    p2 = matchup[1]
    roster.bench_players([p1, p2])
    await start_show(p1, p2)


async def finish_show(show=None):
    global shows

    if show is not None:
        await show.finish_show()
        shows.remove(show)
        return show
    elif len(shows) >= 0:
        show = shows[0]
        await show.finish_show()
        shows.remove(show)
        return show


async def finish_bracket():
    if len(roster.players) == 1:
        winner = roster.players[0]
        desc = ":crown: CONGRATULATIONS! **" + winner.name + "** IS THE NEW **CAKE MAKE CHAMPION**!"
        desc += "\n\n A ***BEAM OF LIGHT** envelops "  + winner.get_pronoun('them') + " and with a blinding flash, they "
        desc += "***ASCEND***."
        desc += "\n\n " + prose.random('finish_bracket.yaml')
        desc += "\n\n *The bracket is over. A new bracket will start soon.*"
        await messaging.send_general_message("LONG LIVE THE CHAMPION", desc)


async def new_bracket():
    roster.build_new_roster()
    desc = "*A new bracket has started. Who will win the crown?*"
    desc += "\n\n**JUDGES FOR THIS BRACKET:**"
    desc += "\n*Judge Simon*, *Judge Paula*, and *Judge Vega Soulscream*."
    desc += "\n\n " + prose.random('new_bracket.yaml')
    await messaging.send_general_message("A NEW BRACKET BEGINS...", desc)
