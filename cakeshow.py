import random
import messaging
import roster
from config import config
import judges
import prose
import periodic
from functools import partial


class Gameshow():
    def __init__(self, p1, p2, final=False):
        self.participant1 = p1
        self.participant2 = p2
        p1.on_added_to_show(self)
        p2.on_added_to_show(self)
        self.minutes_until_resolve = config.interval
        self.cheered_by = []
        self.final=final

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

    async def cheer(self, player_object, user_object):
        res = False
        if user_object.id not in self.cheered_by:
            res = player_object.add_cheer(user_object)
            if res:
                self.cheered_by.append(user_object.id)
        return res


shows = []

async def interview(player):
    await messaging.send_general_message("EXCLUSIVE INTERVIEW...", player.name + " agrees to an exclusive interview.\n" + prose.random('interview.yaml'))
    await messaging.send_inspect_message(player)


async def start_show(p1, p2, final=False):
    global shows

    show = Gameshow(p1, p2, final=final)
    await messaging.send_versus_message(p1, p2, final=final)
    shows.append(show)

    if random.randrange(1, 100) <= 38:
            interviewee = random.choice([p1, p2])
            if not interviewee.has_interviewed:
                periodic.schedule_new_event(func=lambda: interview(interviewee))
                interviewee.has_interviewed = True

    return show


async def start_random_show():
    matchup = roster.get_matchup()
    p1 = matchup[0]
    p2 = matchup[1]
    roster.bench_players([p1, p2])
    await start_show(p1, p2)


async def start_final_show():
    matchup = roster.get_matchup()
    p1 = matchup[0]
    p2 = matchup[1]
    roster.bench_players([p1, p2])
    await start_show(p1, p2, final=True)


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
        desc += "\n\n A ***BEAM OF LIGHT*** envelops "  + winner.get_pronoun('them') + " and with a blinding flash, they "
        desc += "__***ASCEND***__."
        desc += "\n\n " + prose.random('finish_bracket.yaml')
        desc += "\n\n *The bracket is over. A new bracket will start soon.*"
        roster.vacation_players(roster.players_eliminated)
        roster.ascend_players([winner])
        periodic.schedule_new_event(func=lambda: messaging.send_general_message("LONG LIVE THE CHAMPION", desc), duration=config.minutes_between_brackets)


async def new_bracket():
    roster.build_new_roster()
    desc = "*A new bracket has started. Who will win the crown?*"
    desc += "\n\n**PARTICPANTS FOR THIS BRACKET:**\n"
    for player in roster.players:
        desc += "*" + player.name + "*, "
    desc += "\n\n**JUDGES FOR THIS BRACKET:**"
    desc += "\n*Judge Simon*, *Judge Paula*, and *Judge Vega Soulscream*."
    desc += "\n\n " + prose.random('new_bracket.yaml')
    periodic.schedule_new_event(func=lambda: messaging.send_general_message("A NEW BRACKET BEGINS...", desc))
