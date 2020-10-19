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

        winner = random.choice([p1, p2])
        im_winner = imaging.open_image_path(winner.get_portrait_path())

        desc = "***" + p1.get_sound() + "*** " + p1.name + " " + p1.get_verb().lower() + " a " + p1.get_cake_adjective().lower() + " " + p1.get_cake_flavor().lower() + " " + p1.get_cake_type().lower() + "!!"
        desc += "\n***" + p2.get_sound() + "*** " + p2.name + " " + p2.get_verb().lower() + " a " + p2.get_cake_adjective().lower() + " " + p2.get_cake_flavor().lower() + " " + p2.get_cake_type().lower() + "!!"
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

        new_embed = discord.Embed(title="UP NEXT...", description="The following contestants will bake next. The show will start shortly.", color=0xffd300)
        new_embed.add_field(name="Contestant 1", value=n1, inline=True)
        new_embed.add_field(name="Contestant 2", value=n2, inline=True)
        file = imaging.get_image_file(res)
        new_embed.set_image(url = 'attachment://image.png')
        await broadcast_embed(new_embed, file=file)