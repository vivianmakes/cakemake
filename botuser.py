import asyncio
import discord
from discord.ext import commands
from discord import file
import imaging
import roster
from io import BytesIO
import cakeshow

class Botuser(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.broadcast_channel = None # sure would be cool to set this via environment variable

    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        self.broadcast_channel = self.get_channel(767265737739075605)  # sure would be cool to set this via environment variable

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
    await cakeshow.test_show()


botuser.run('NzY3NzkwMjg4NDE2MDE0NDE5.X43CbQ.nvByWv0o1Alug1bAIYw4SD8c2YI')