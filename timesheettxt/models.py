import copy
import datetime

class Context:
    def __init__(self):
        self.date = None
        self.tz = None

class ContextError(RuntimeError):
    pass

class Interval:
    def __init__(self, context, spec, time):
        self.context = context
        self.start = self.parse_time(time)
        self.stop = None
        self.spec = spec

    def __str__(self):
        dateformat = "{:%Y-%m-%d %H:%M:%S}"
        if self.stop:
            stop = dateformat.format(self.stop.astimezone(None))
        else:
            stop = " [ still running ] "
        return "%s -- %s  %s" % (dateformat.format(self.start.astimezone(None)), stop, self.spec)

    def copy(self):
        return copy.copy(self)

    def parse_time(self, time):
        if self.context.date is None:
            raise ContextError("date is unknown")
        if self.context.tz is None:
            raise ContextError("timezone is unknown")
        if len(time) == 4:
            seconds = 0
        elif len(time) == 6:
            seconds = int(time[4:6])
        else:
            raise ValueError("time has to be in HHMM or HHMMSS (24-hour) format")
        return datetime.datetime(
            self.context.date.year, self.context.date.month, self.context.date.day,
            int(time[0:2]), int(time[2:4]), seconds,
            tzinfo=self.context.tz
        )

    def set_stop(self, time):
        if time is None:
            self.stop = None
            return
        stop = self.parse_time(time)
        if stop < self.start:
            raise ValueError("the interval may not end before it started")
        self.stop = stop

    def set_start(self, time):
        self.start = self.parse_time(time)
