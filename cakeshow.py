import roster
import random
import botuser
import asyncio
import imaging
import discord


class Gameshow():
    def __init__(self):
        self.participant1 = None
        self.participant2 = None
        self.cheered_by = []

    def get_participant_list(self):
        return [self.participant1, self.participant2]


pending_show = None

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

async def broadcast(message):
    await botuser.botuser.broadcast(message)

async def broadcast_embed(in_embed, file=None):
    await botuser.botuser.broadcast_embed(in_embed, file=file)


async def test_show():
    if pending_show is not None:
        await run_show()
    else:
        await prep_show()


async def run_show():
    global pending_show
    if pending_show is not None:
        p1 = pending_show.participant1
        p2 = pending_show.participant2
        p1_quality = 0
        p2_quality = 0

        # PT 1

        p1_quality = p1.get_roll()

        desc = "***" + p1.get_sound() + "*** " + p1.name + " " + p1.get_verb().lower() + " a " + p1.get_cake_adjective().lower() + " " + p1.get_cake_flavor().lower() + " " + p1.get_cake_type().lower() + "!!"
        
        if (p1.get_unlucky()):
          desc += ' ' + get_unlucky_text()
          p1_quality = 1

        if (p1.get_lucky()):
          desc += ' ' + get_lucky_text()
          p1_quality += 30

        desc += '\n' + get_quality_text(p1_quality)

        # PT 2

        p2_quality = p2.get_roll()

        desc += "\n\n***" + p2.get_sound() + "*** " + p2.name + " " + p2.get_verb().lower() + " a " + p2.get_cake_adjective().lower() + " " + p2.get_cake_flavor().lower() + " " + p2.get_cake_type().lower() + "!!"

        if (p2.get_unlucky()):
          desc += ' ' + get_unlucky_text()
          p2_quality = 1

        if (p2.get_lucky()):
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
        
        im_winner = winner.get_portrait_path()
        res = imaging.concatenate_multiple("images/win_l.png", im_winner, "images/win_r.png")

        desc += "\n\n*" + winner.name + "* has swayed the judges with " + winner.get_pronoun('their') + " skill! ***VICTORY! :sparkles:***"

        new_embed = discord.Embed(title="THE WINNER IS...",
                                  description=desc,
                                  color=0x7aa54c)
        file = imaging.get_image_file(res)
        new_embed.set_image(url='attachment://image.png')
        await broadcast_embed(new_embed, file=file)

        p1.post_match_results(winner is p1)
        p2.post_match_results(winner is p2)
        pending_show = None
    else:
        print("Couldn't start a show. No show was pending!")


async def prep_show():
    global pending_show
    if pending_show is None:
        participants = roster.get_random_pair()

        p1 = participants[0]
        p2 = participants[1]

        pending_show = Gameshow()
        pending_show.participant1 = p1
        pending_show.participant2 = p2

        im1 = p1.get_portrait_path()
        im_vs = "images/vs.png"
        im2 = p2.get_portrait_path()

        n1 = p1.name
        n2 = p2.name

        d1 = '[' + str(p1.wins) + '-' + str(p1.losses) + ']' + ' - ' + p1.get_vibe_emojis()
        d2 = '[' + str(p2.wins) + '-' + str(p2.losses) + ']' + ' - ' + p2.get_vibe_emojis()

        res = imaging.concatenate_multiple(im1, im_vs, im2)

        new_embed = discord.Embed(title="UP NEXT...", description="The following contestants will bake next. The winner will be announced soon.\nUse the `!cheer [part of name]` command to cheer for the contestant you think will win. (Or want to win!)", color=0xffd300)
        new_embed.add_field(name=n1, value=d1, inline=True)
        new_embed.add_field(name=n2, value=d2, inline=True)
        file = imaging.get_image_file(res)
        new_embed.set_image(url = 'attachment://image.png')
        await broadcast_embed(new_embed, file=file)


async def cheer(player_object, user_object):
    global pending_show
    res = False
    res = player_object.add_cheer(user_object)

    return res