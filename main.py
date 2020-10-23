import asyncio

from periodic import periodic
import botuser
from config import credentials
import cakeshow

async def update_loop():
    await asyncio.sleep(10)
    await botuser.botuser.wait_until_ready()
    while not botuser.botuser.is_closed():
        await periodic.update()  # would like to move this into periodic for better encapsulation
        await asyncio.sleep(5)

botuser.botuser.loop.create_task(update_loop())
botuser.botuser.run(credentials.bot_token)