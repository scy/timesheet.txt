# timesheet.txt

This project defines a plain text timesheet file format and provides a Python 3 parser.

## Example

```
# I'm in Germany right now.
TZ Europe/Berlin

2019-06-03:
0905  think about concept #tstxt
0931  write readme #tstxt
1215.  # a simple dot means "stop the previous entry without starting a new one"
1305^  # a caret means "continue the previous entry"
1402.

2019-06-04:
0710  take the train to the airport
0724  flight check-in
0732. # checked in, hanging around in the terminal waiting for boarding
0808  boarding
0820. # sitting in the plane, doing nothing
0903  ASD-2342: fix regex buffer overflow
1008  in-flight breakfast
1025  e-mail to customer #asd !$   # the "asd" project tag and "not billable"
TZ Europe/London # we've crossed the timezone border
0933  ASD-1701: improve design
# …
```

## Design Goals

* The user should be able to create new timesheet entries really quickly.
  When the time tracking system gets in your way, you stop using it, or your entries start to get inaccurate.
* No special software other than a text editor should be required to modify the timesheet.
  This allows you to capture entries using any device that can edit plain text files, or even with a sheet of paper.
* Timesheet entries should not need an explicit end time if another activity was started immediately afterwards.
  Instead, the end time of the first entry should automatically be the start time of the second one.
  Else, changing the times of adjacent entries is a pain and error-prone.
* The format should be easily parsable by a machine, but easy to learn for the end user.
* Comments, completely ignored by the parser (i.e. for the file author only) should be supported, both standalone and associated with an entry.
* For each entry, there should be an easy way to provide
  * a description text
  * a ticket or issue ID (for filtering, reports or export to other software)
  * tags (for filtering and reports)
  * a "billable" flag that can be set explicitly to yes or no, to allow for different defaults based on project or issue.
* Writing entries in different timezones should be possible and easy to do.
* Creating entries across midnight or spanning multiple days should be possible and easy.
* The code that's reading it should handle the case where the most recent entry is still active/open while parsing.
* If the parser does not understand something, it should throw an error instead of ignoring the input.

There are also some anti-goals, i.e. things that the system should _not_ have:

* Description texts should be a single line only.
  This is a timesheet, not a diary.
* Providing multiple issue IDs for a single entry should not be supported because it's hard to automatically export time spent to issue trackers then.

## Done

* define basic file format
* parser understands
  * comments
  * `TZ` lines
  * date lines
  * time entries, but without parsing the description string into its components (tags, issue ID, …)
  * stop lines
  * continue lines
* timezone handling

## Missing

These are things that I as the author still want to do.
If you need anything else, feel free to create a GitHub issue for it, but be prepared to implement it yourself. 😉

* [create GitHub issues for all of these items]
* parse description string into components
* allow to continue more than just the last entry (e.g. the next-to-last one)
* CLI tool instead of just a Python module
* filtering
* reports
* export to Jira
* extensive documentation of the file format
* best practices?
