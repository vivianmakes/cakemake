import asyncio
import discord
from discord.ext import commands
from discord import file
import imaging
import roster
from io import BytesIO
import cakeshow
from config import credentials, config
import copy

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
        if (config.public_test):
            self.broadcast_channel = self.get_channel(credentials.public_channel)
            print('PUBLIC')
        else:
            self.broadcast_channel = self.get_channel(credentials.private_channel)
            print('PRIVATE')
        print('--------------')
        if (config.persistent):
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


@botuser.command(name='test')
async def test(ctx):
    await cakeshow.test_show()


@botuser.command(name = 'cheer')
async def cheer(ctx, arg):
    if cakeshow.pending_show is not None:
        if arg == '1' or arg == '2':
            res = False
            if arg == '1':
                res = await cakeshow.cheer(1, ctx.author)
            elif arg == '2':
                res = await cakeshow.cheer(2, ctx.author)

            if res:
                await ctx.send(':tada: *You successfully cheer on contestant no. ' + arg + '* :tada:')
            else:
                await ctx.send(
                    ':no_entry_sign: *Your cheers fall on deaf ears...* :no_entry_sign:\n(No more than one cheer per person, sorry)')
        else:
            await ctx.send(
                ':no_entry_sign: **NO CAN DO, BOSS** :no_entry_sign:\nPlease enter a contestant number in numeral form.')
    else:
        await ctx.send(
            ':no_entry_sign: **NO CAN DO, BOSS** :no_entry_sign:\nNo contestants are currently baking. You must wait until contestants are baking!')


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
  return in_player.wins - in_player.losses*0.001


@botuser.command(name='inspect')
async def inspect(ctx, *args):
    search_string = " ".join(args[:])
    result = roster.search_players(search_string) #returns a player or none
    if result is None:
        new_embed = discord.Embed(title = "ERROR",
                                  description = "Couldn't figure out who you meant. Try being more specific?",
                                  color = 0x458dd6)
        await ctx.send(embed=new_embed)
    else:
        desc = "*You consume 1 :sparkles: magic to scry.*"
        desc += "\n\n**Pronouns:** " + result.get_pronoun('they') + "/" + result.get_pronoun('them')
        desc += "\n**Wins:** " + str(result.wins)
        desc += "\n**Losses:** " + str(result.losses)
        desc += "\n\n**Vibe:** " + result.get_vibe_emojis()
        desc += "\n**Talent:** " + str(result.talent)
        desc += "\n**Reliability:** " + str(result.reliability)
        desc += "\n**Horoscope:** " + result.get_luck_description()


        new_embed = discord.Embed(title = "INSPECTING " + result.name,
                                  description = desc,
                                  color = 0x458dd6)
        await ctx.send(embed = new_embed)