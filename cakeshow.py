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


pending_show = None

def get_lucky_text():
  random_lucky_text.append('The cake **sparkles**!! :sparkles:')
  random_lucky_text.append('The cake **gleams**!! :sparkles:')
  random_lucky_text.append('The cake **glows**!! :sparkles:')
  random_lucky_text.append('A **choir of angels** sings!! :sparkles:')
  return random.choice(random_lucky_text)

def get_unlucky_text():
  random_unlucky_text = []
  random_unlucky_text.append('The cake **is badly burned**!!')
  random_unlucky_text.append('The cake **screeches, bloodcurdlingly**!!')
  random_unlucky_text.append('The cake **levitates ominously**!!')
  random_unlucky_text.append('The cake **begins to weep blood!**')
  random_unlucky_text.append('The cake **bursts into flames**!!')
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

        desc = "***" + p1.get_sound() + "*** " + p1.name + " " + p1.get_verb().lower() + " a " + p1.get_cake_adjective().lower() + " " + p1.get_cake_flavor().lower() + " " + p1.get_cake_type().lower() + "!!"

        p1_quality = p1.get_roll()

        if (p1.get_unlucky()):
          desc += ' ' + get_unlucky_text()
          p1_quality = 1

        if (p1.get_lucky()):
          desc += ' ' + get_lucky_text()
          p1_quality += 30

        desc += "\n***" + p2.get_sound() + "*** " + p2.name + " " + p2.get_verb().lower() + " a " + p2.get_cake_adjective().lower() + " " + p2.get_cake_flavor().lower() + " " + p2.get_cake_type().lower() + "!!"

        p2_quality = p2.get_roll()

        if (p2.get_unlucky()):
          desc += ' ' + get_unlucky_text()
          p2_quality = 1

        if (p2.get_lucky()):
          desc += ' ' + get_lucky_text()
          p2_quality += 30

        if (p1_quality == p2_quality):
          winner = random.choice([p1, p2])
        else:
          if (p1_quality > p2_quality):
            winner = p1
          else:
            winner = p2
        
        im_winner = imaging.open_image_path(winner.get_portrait_path())

        desc += "\n\n*" + winner.name + "* has swayed the judges with " + winner.get_pronoun('their') + " skill! ***VICTORY! :sparkles:***"

        new_embed = discord.Embed(title="THE WINNER IS...",
                                  description=desc,
                                  color=0x7aa54c)
        file = imaging.get_image_file(im_winner)
        new_embed.set_image(url='attachment://image.png')
        await broadcast_embed(new_embed, file=file)

        p1.cheer = 0
        p2.cheer = 0
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
        im2 = p2.get_portrait_path()

        n1 = p1.name
        n2 = p2.name

        res = imaging.concatenate(im1, im2)

        new_embed = discord.Embed(title="UP NEXT...", description="The following contestants will bake next. The winner will be announced in 30 minutes.\nUse `!cheer [contestant]` to cheer for the contestant you think will win.", color=0xffd300)
        new_embed.add_field(name="Contestant 1", value=n1, inline=True)
        new_embed.add_field(name="Contestant 2", value=n2, inline=True)
        file = imaging.get_image_file(res)
        new_embed.set_image(url = 'attachment://image.png')
        await broadcast_embed(new_embed, file=file)