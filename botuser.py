import asyncio
import discord
from discord.ext import commands
from discord import file
import imaging
import roster
from io import BytesIO
import cakeshow
from config import credentials

class Botuser(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.broadcast_channel = None

    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        self.broadcast_channel = self.get_channel(credentials.broadcast_channel)
        print('Channel Target:')
        print(credentials.broadcast_channel)
        print('--------------')

    async def broadcast(self, message):
        await self.broadcast_channel.send(message)

    async def broadcast_embed(self, in_embed, file=None):
        await self.broadcast_channel.send(embed=in_embed, file=file)


botuser = Botuser(command_prefix='!')


@botuser.command(name='test')
async def test(ctx):
    await cakeshow.test_show()


@botuser.command(name='cheer')
async def cheer(ctx, arg):
  if cakeshow.pending_show is not None:
    if arg == '1' or arg == '2':
      if arg == '1':
        res = await cakeshow.cheer(1, ctx.author)
      elif arg == '2'
        res = await cakeshow.cheer(2, ctx.author)
      
      if res:
        await ctx.send(':tada: *You successfully cheer on contestant no. '+ arg + '* :tada:')
      else:
        await ctx.send(':no_entry_sign: *Your cheers fall on deaf ears...* :no_entry_sign:\n(No more than one cheer per person, sorry)'
    else:
      await ctx.send(':no_entry_sign: **NO CAN DO, BOSS** :no_entry_sign:\nPlease enter a contestant number in numeral form.')
  else:
    await ctx.send(':no_entry_sign: **NO CAN DO, BOSS** :no_entry_sign:\nNo contestants are currently baking. You must wait until contestants are baking!')


botuser.run(credentials.bot_token)