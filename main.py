import asyncio

from periodic import Periodic
import botuser
from config import credentials

async def update_loop():
    await asyncio.sleep(6)
    await botuser.botuser.wait_until_ready()
    while not botuser.botuser.is_closed():
        await asyncio.sleep(30)
        await Periodic.update()

botuser.botuser.loop.create_task(update_loop())
botuser.botuser.run(credentials.bot_token)