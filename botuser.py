import asyncio
import discord
from discord.ext import commands
from discord import file
import imaging
from io import BytesIO

class Botuser(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.broadcast_channel = self.get_channel(767265737739075605) # sure would be cool to set this via environment variable

    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('--------------')

    async def broadcast(self, message):
        self.broadcast_channel.send(message)


botuser = Botuser(command_prefix='!')


@botuser.command(name='test')
async def test(ctx):
    im1 = imaging.get_portrait_path('professor.png')
    im2 = imaging.get_portrait_path('knight.png')
    res = imaging.concatenate(im1, im2)

    with BytesIO() as image_binary:
        res.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='matchup.png'))




botuser.run('NzY3NzkwMjg4NDE2MDE0NDE5.X43CbQ.nvByWv0o1Alug1bAIYw4SD8c2YI')