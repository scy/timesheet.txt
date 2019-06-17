import copy
import datetime
import description

class Context:
    def __init__(self):
        self.date = None
        self.tz = None

class ContextError(RuntimeError):
    pass

class Interval:
    extractors = [
        description.IssueIDExtractor(),
        description.BillableExtractor(),
    ]

    def __init__(self, context, spec, time):
        self.context = context
        self.start = self.parse_time(time)
        self.stop = None
        self.duration = None
        self.spec = spec
        self.description = spec
        self.meta = {}
        self.extract(spec)

    def __str__(self):
        dateformat = "{:%Y-%m-%d %H:%M:%S}"
        meta = []
        if self.meta["issue"]:
            meta.append(self.meta["issue"])
        if self.meta["billable"] is not None:
            meta.append("$" if self.meta["billable"] else "!$")
        if self.stop:
            stop = dateformat.format(self.stop.astimezone(None))
            minutes = round(self.duration.total_seconds() / 60)
            duration = "%2d:%02d" % (minutes // 60, minutes % 60)
        else:
            stop = " [ still running ] "
            duration = "--:--"
        return "%s -- %s (%s)  %s%s" % (
            dateformat.format(self.start.astimezone(None)),
            stop,
            duration,
            "[%s] " % " ".join(meta) if meta else "",
            self.description,
        )

    def copy(self):
        return copy.copy(self)

    def extract(self, description):
        for extractor in Interval.extractors:
            ret = extractor.extract(description)
            if len(ret) == 2: # Tuple of key/value metadata dict and new text.
                self.meta.update(ret[0])
                description = ret[1]
            else:
                raise NotImplementedError("extractors returning something with length %d not implemented" % len(ret))
        self.description = description

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
            self.duration = None
            return
        stop = self.parse_time(time)
        if stop < self.start:
            raise ValueError("the interval may not end before it started")
        self.stop = stop
        self.duration = self.stop - self.start

    def set_start(self, time):
        self.start = self.parse_time(time)
