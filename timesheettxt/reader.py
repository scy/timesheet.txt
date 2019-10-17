import datetime
from dateutil.tz import gettz
import models
import re

try:
    from backports.datetime_fromisoformat import MonkeyPatch
    MonkeyPatch.patch_fromisoformat()
except ImportError:
    # It's not needed on Python >= 3.7, on everything else we risk to crash.
    pass

comment = re.compile(r"(^\s*#.*$|\s+#\s.*$)")
date = re.compile(r"^(\d+-\d{1,2}-\d{1,2}):$")
entry = re.compile(r"^(\d{4}|\d{6})([.^]|\s+(.+))$")
timezone = re.compile(r"^TZ\s+(\S+)$")

class ParserError(RuntimeError):
    pass

class FileReader:
    def __init__(self, file):
        self.file = file
        self.line_no = 0
        self.context = models.Context()
        self.current_interval = None
        self.interval_open = False

    def __iter__(self):
        return self

    def __next__(self):
        for line in self.file:
            self.line_no += 1
            try:
                # Remove comments.
                line = comment.sub("", line.strip())
                # Skip lines that are empty or just comments.
                if line == "":
                    continue
                # If the line defines the timezone, set it.
                match = timezone.match(line)
                if match:
                    self.context.tz = gettz(match[1])
                    continue
                # If the line sets a new date, keep track of it.
                match = date.match(line)
                if match:
                    self.context.date = datetime.date.fromisoformat(match[1])
                    continue
                # Is the line a time entry?
                match = entry.match(line)
                if match:
                    # Is it a stop line?
                    if match[2] == ".":
                        if not self.interval_open:
                            raise ParserError("cannot stop since there is no open interval")
                        self.current_interval.set_stop(match[1])
                        self.interval_open = False
                        # Since this interval is now complete, we should return it.
                        return self.current_interval
                    # Is it a continue line?
                    if match[2] == "^":
                        if self.interval_open:
                            raise ParserError("cannot continue since there is already an open interval")
                        if not self.current_interval:
                            raise ParserError("cannot continue since there is no previous entry")
                        self.current_interval = self.current_interval.copy()
                        self.current_interval.set_start(match[1])
                        self.current_interval.set_stop(None)
                        self.interval_open = True
                        # We don't return the interval until we know its end.
                        continue
                    # It seems to be a regular entry. If there's a previous interval open, stop it.
                    previous_interval = None
                    if self.interval_open:
                        self.current_interval.set_stop(match[1])
                        previous_interval = self.current_interval
                    # Create a new one.
                    self.current_interval = models.Interval(self.context, match[3], match[1])
                    self.interval_open = True
                    # We won't return this new interval until we know its end, but if there was a previous one, we can
                    # now return it.
                    if previous_interval:
                        return previous_interval
                    continue
                # I have no idea what this is.
                raise RuntimeError("invalid syntax: %s" % line)
            except Exception as e:
                raise ParserError("error while parsing line %d: %s" % (self.line_no, e)) from e
        # If the file is finished and we still have an open interval, return it as open.
        if self.interval_open:
            self.interval_open = False # Basically a lie, but we need to raise StopIteration next time.
            return self.current_interval
        raise StopIteration
