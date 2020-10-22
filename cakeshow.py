import random
import messaging
import periodic
import arrow
import roster
from config import config


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

        p1_quality = p1.get_roll()
        desc = "***" + p1.get_sound() + "*** " + p1.name + " " + p1.get_verb().lower() + " a " + p1.get_cake_adjective().lower() + " " + p1.get_cake_flavor().lower() + " " + p1.get_cake_type().lower() + "!!"
        if p1.get_unlucky():
            desc += ' ' + get_unlucky_text()
            p1_quality = 1
        if p1.get_lucky():
            desc += ' ' + get_lucky_text()
            p1_quality += 30
        desc += '\n' + get_quality_text(p1_quality)

        p2_quality = p2.get_roll()
        desc += "\n\n***" + p2.get_sound() + "*** " + p2.name + " " + p2.get_verb().lower() + " a " + p2.get_cake_adjective().lower() + " " + p2.get_cake_flavor().lower() + " " + p2.get_cake_type().lower() + "!!"
        if p2.get_unlucky():
            desc += ' ' + get_unlucky_text()
            p2_quality = 1
        if p2.get_lucky():
            desc += ' ' + get_lucky_text()
            p2_quality += 30
        desc += '\n' + get_quality_text(p2_quality)

        # RESULTS

        if (p1_quality == p2_quality):
            winner = random.choice([p1, p2])
        else:
            if (p1_quality > p2_quality):
                winner = p1
            else:
                winner = p2

        await messaging.send_victory_message(desc, winner)

        p1.post_match_results(winner is p1)
        p2.post_match_results(winner is p2)
        p1.on_show_end(self)
        p2.on_show_end(self)


def get_quality_text(quality):
    text = "It's "
    if quality >= 30:
        text += "**LEGENDARY!!** :star::star::star::star::star:"
    elif quality >= 17:
        text += "**AMAZING!!** :star::star::star::star:"
    elif quality >= 10:
        text += "**REALLY GOOD!!** :star::star::star:"
    elif quality >= 5:
        text += "**Yummy!** :star::star:"
    elif quality >= 3:
        text += "okay! :star:"
    elif quality >= 1:
        text += "alright."
    else:
        text += "***HORRIBLE!!!*** :weary:"
    return text


def get_lucky_text():
  random_lucky_text = []
  random_lucky_text.append('The cake **sparkles**!! :sparkles:')
  random_lucky_text.append('The cake **gleams**!! :sparkles:')
  random_lucky_text.append('The cake **glows**!! :sparkles:')
  random_lucky_text.append('A **choir of angels** sings!! :sparkles:')
  random_lucky_text.append('A **series of trumpets** herald the arrival of the cake!! :sparkles:')
  return random.choice(random_lucky_text)


def get_unlucky_text():
  random_unlucky_text = []
  random_unlucky_text.append('The cake **is badly burned**!!')
  random_unlucky_text.append('The cake **screeches, blood-curdlingly**!!')
  random_unlucky_text.append('The cake **levitates ominously**!!')
  random_unlucky_text.append('The cake **begins to weep blood!**')
  random_unlucky_text.append('The cake **bursts into flames**!!')
  random_unlucky_text.append('The cake **begs for death**!!')
  return random.choice(random_unlucky_text)


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
    roster.bench_player(p1)
    roster.bench_player(p2)
    await start_show(p1, p2)


async def finish_show(show):
    global shows

    await show.finish_show()
    shows.remove(show)
    return show

matches_until_elimination = 9


async def handle_show_update():
    global matches_until_elimination

    if matches_until_elimination >= 0:
        if len(shows) > 0:
            for show in shows:
                show.minutes_until_resolve += -1
                if show.minutes_until_resolve == 0:
                    await finish_show(show)
        else:
            await start_random_show()
        matches_until_elimination += -1
    else:
        roster.eliminate_player()
        matches_until_elimination = 9



# --

periodic.schedule_new_event(time=arrow.utcnow(), func=handle_show_update, loop_minutes=1)