import discord
from discord.ext import commands
import imaging
import roster
import messaging
from config import credentials, config

class Botuser(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.broadcast_channel = None

    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        print('Channel Target:')
        if config.public_test:
            self.broadcast_channel = self.get_channel(credentials.public_channel)
            print('PUBLIC')
        else:
            self.broadcast_channel = self.get_channel(credentials.private_channel)
            print('PRIVATE')
        print('--------------')
        if config.persistent:
            print('BOT IS PERSISTENT - PLAY WILL BE RECORDED.')
        else:
            print('BOT IS NOT PERSISTENT - WILL NOT SAVE.')
        if self.broadcast_channel is None:
            print("WARNING: couldn't find a broadcast channel! Are your ENVIRONMENT VARIABLES set right?")


    async def broadcast(self, message):
        await self.broadcast_channel.send(message)

    async def broadcast_embed(self, in_embed, file=None):
        await self.broadcast_channel.send(embed=in_embed, file=file)


botuser = Botuser(command_prefix='!')

@botuser.command(name = 'cheer')
async def cheer(ctx, *args):
    search_string = " ".join(args[:])
    player = roster.search_players(search_string)  # returns a player or none
    if player is None:
        await messaging.send_error_message("Couldn't figure out who you meant. Try being more specific.")
    else:
        result = player.add_cheer(ctx.author)
        if result:
            new_embed = discord.Embed(title="CHEER RESULT",
                                      description="You cheer on " + player.name + "!\n",
                                      color=0x458dd6)
        else:
            await messaging.send_error_message("You've already cheered this contestant during this show.")
        await ctx.send(embed=new_embed)


@botuser.command(name='roster')
async def list_roster(ctx):
    if len(roster.players) > 0:
        title = "**CURRENT CONTESTANTS:**\n"
        msg = ""
        sortedroster = roster.players.copy()
        sortedroster.sort(key=compare_wins, reverse=True)

        for player in sortedroster:
            msg += "\n`[" + str(player.wins) + "-" + str(player.losses) + "]` " + player.name
            msg += " - "
            msg += player.get_vibe_emojis()

        new_embed = discord.Embed(title = title,
                                  description = msg,
                                  color = 0x458dd6)
        # file = imaging.get_image_file(im_winner)
        # new_embed.set_image(url = 'attachment://image.png')

        await ctx.send(embed=new_embed)


def compare_wins(in_player):
    return in_player.wins-in_player.losses


@botuser.command(name='inspect')
async def inspect(ctx, *args):
    search_string = " ".join(args[:])
    result = roster.search_players(search_string) #returns a player or none
    if result is None:
        await messaging.send_error_message("Couldn't figure out who you meant. Try being more specific.")
    else:
        desc = ""
        desc += "\n\n**Pronouns:** " + result.get_pronoun('they') + "/" + result.get_pronoun('them')
        desc += "\n**Wins:** " + str(result.wins)
        desc += "\n**Losses:** " + str(result.losses)
        desc += "\n\n**Vibe:** " + result.get_vibe_emojis()
        desc += "\n**Talent:** " + result.get_talent_description()
        desc += "\n**Reliability:** " + result.get_reliability_description()
        desc += "\n**Horoscope:** " + result.get_luck_description()

        im = imaging.open_image_path(result.get_portrait_path())
        file = imaging.get_image_file(im)
        new_embed = discord.Embed(title = "INSPECTING " + result.name,
                                  description = desc,
                                  color = 0x458dd6)
        new_embed.set_image(url='attachment://image.png')
        await ctx.send(embed = new_embed, file=file)