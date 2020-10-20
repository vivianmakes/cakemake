import asyncio
import arrow
from botuser import Botuser
import cakeshow

class Periodic:
    def __init__(self):
        self.next_event = arrow.utcnow().shift(minutes=+1)
        self.schedule_next_event()

    def schedule_next_event(self):
      self.next_event = arrow.utcnow().shift(minutes=+15)
      """
      if arrow.utcnow().hour < 17:
          self.next_event = arrow.utcnow().replace(hour=22, minute=09)
      else:
          self.next_event = arrow.utcnow().replace(hour=22, minute=00).shift(days=+1)
      """

    async def update(self):
        if self.next_event <= arrow.utcnow():
            self.schedule_next_event()

            try:
                await cakeshow.test_show()
            except Exception as e:
                print('>> ENCOUNTERED AN EXCEPTION IN RUN_SCHEDULED')
                print(e)
                raise e

periodic = Periodic()