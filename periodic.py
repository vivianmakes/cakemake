import asyncio
import cakeshow
import roster
import arrow
import messaging
from config import config


class Event:
    def __init__(self, duration=0, func=None):
        self.func_to_call = func
        self.duration = duration  # in minutes

    async def run(self):
        if self.func_to_call is not None:
            await self.func_to_call()
            return arrow.utcnow().shift(minutes=self.duration)
        else:
            print("Couldn't run a queued non-function")
            return arrow.utcnow()

async def send_elimination_warning():
    desc = "The judges meet in their soundproof chambers to discuss the rankings... :warning:"
    await messaging.send_general_message("THE JUDGES DELIBERATE...", desc)


async def send_bracket_warning():
    desc = "A new bracket begins."
    await messaging.send_general_message("A NEW BRACKET BEGINS!", desc)


class Periodic:
    def __init__(self):
        self.events = []
        self.hold_event_queue_until = arrow.utcnow()
        self.hold_show_until = arrow.utcnow()
        self.shows_since_last_elimination = 0

    def remove_event(self, event):
        self.events.remove(event)

    def add_event(self, event):
        self.events.append(event)

    async def update(self):

        if self.hold_event_queue_until < arrow.utcnow() or len(self.events) > 0:
            if self.hold_event_queue_until and len(self.events) > 0:
                self.hold_event_queue_until = await self.events[0].run()
                self.remove_event(self.events[0])
        else:
            if self.hold_show_until < arrow.utcnow():
                if len(cakeshow.shows) == 0:
                    if self.shows_since_last_elimination < get_matches_before_elimination():
                        await cakeshow.start_random_show()
                        self.hold_show_until = arrow.utcnow().shift(minutes=config.interval)
                    else:
                        self.shows_since_last_elimination = 0
                        await roster.eliminate_player()
                        self.hold_show_until = arrow.utcnow().shift(minutes=5)
                else:
                    await cakeshow.finish_show()
                    self.shows_since_last_elimination += 1
                    if self.shows_since_last_elimination == get_matches_before_elimination():
                        schedule_new_event(func=send_elimination_warning, duration=5)


def get_matches_before_elimination():
    return min(len(roster.players) * 1.5, 6)


def schedule_new_event(duration=0, func=None):
    global periodic
    new_event = Event(duration=duration, func=func)
    periodic.add_event(new_event)


periodic = Periodic()
schedule_new_event(func=send_bracket_warning, duration=1)


