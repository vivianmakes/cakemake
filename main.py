import asyncio

from periodic import Periodic
from botuser import Botuser

async def update_loop():
    await asyncio.sleep(6)
    await Botuser.wait_until_ready()
    while not Botuser.is_closed():
        await asyncio.sleep(30)
        await Periodic.update()

await update_loop()