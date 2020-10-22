import asyncio
import arrow


class Event:
    def __init__(self, time=None, loop_minutes=0, func=None):
        self.event_time = time
        self.func_to_call = func
        self.loop_minutes = loop_minutes

    async def run_if_ready(self):
        if self.event_time is None:
            print('Event time with None! Be sure to schedule your events ;)')
            return False
        elif self.event_time < arrow.utcnow():
            return await self.run()
        else:
            return True

    async def run(self):
        if self.func_to_call is not None:
            await self.func_to_call()
        else:
            print("Couldn't run a queued non-function")
            return False

        if self.loop_minutes > 0:
            self.event_time.shift(minutes=self.loop_minutes)
            return True
        else:
            return False


class Periodic:
    def __init__(self):
        self.events = []

    async def update(self):
        remove_these_events = []
        for event in self.events:
            if event.event_time < arrow.utcnow():
                keep = await event.run_if_ready()
                if not keep:
                    remove_these_events.append(event)

        for event in remove_these_events:
            self.events.remove(event)

    def remove_event(self, event):
        self.events.remove(event)

    def add_event(self, event):
        self.events.append(event)


periodic = Periodic()


def schedule_new_event(time=None, loop_minutes=0, func=None):
    global periodic
    new_event = Event(time=time, loop_minutes=loop_minutes, func=func)
    periodic.add_event(new_event)

