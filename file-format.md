# timesheet.txt File Format Specification

**Please note that this specification is preliminary and a work in progress.**
It will be finalized in [the 1.0 release](https://github.com/scy/timesheet.txt/milestone/4).
Therefore, the wording might be terse in some parts.

**But!**
If you think anything is confusing, unclear or even wrong, please open an [issue](https://github.com/scy/timesheet.txt/issues) so that we can clarify it before release.

## Purpose

_timesheet.txt_ defines a plain text file format for time sheets, i.e. a log of what a single person did during specific intervals in time.

Please refer to the [readme](README.md) for more information about its design goals and philosophy, as they will not be repeated here.

## Terms

To make sure that we're talking about the same things, this specification will define some special terms that have a certain meaning when it comes to our file format.
These terms will be written in ***bold italic*** font to make them clearly distinguishable.

Unfortunately, it's a bit easy to mix up these terms in a colloquial setting.
Also, the format is still in the process of being specified, therefore it can happen that the wrong term is used in a GitHub issue or even project documentation.
You're welcome to point these out for us to fix.

## The Input File

The _timesheet.txt_ tools act upon a stream of data called the ***input file***.
This does not have to be a real file, since the tools are designed to be able to read from a stream (e.g. Unix's *standard input*), too.
Since we don't care how you create this stream of data, and it's transparent to the tools, it will nevertheless be called the input file.

The characters in the input file are expected to be encoded according to the UTF-8 standard.

The input file is read from start to end, one line at a time.
A ***line*** ends with a ***line terminator***, a newline character (`\n` or `LF` or `U+000A`).
Since whitespace is removed from the end of each line (see below), Windows-style line endings (`\r\n` or `CRLF` or `U+000D` followed by `U+000A`) are implicitly supported as well.
Mac OS 9 style line endings (`CR` only) are not, though.

It is a good habit to end the file with a line terminator, but this is not required.

## Lines

Whitespace at the beginning and end of a line will be ignored.
*(TODO: define whitespace)*

There is no way for a "logical line" to span across a line terminator.
In other words, ending a line with `\`, as supported by some programming languages and formats, is deliberately not a part of _timesheet.txt_.
Parsers should be simple and a description text should not be a novel.

## Comments

A ***comment*** is introduced by the `#` character.
Everything after it until the end of the line will be dropped/ignored when parsing.
Comments allow adding remarks to the input file for human consumption.

In order to allow parsing of hashtags and issue IDs that start with `#`, the character must only be recognized as starting a comment if it is followed by at least one whitespace character or nothing at all (i.e. end of line).
Additionally, `#` will only be recognized as the comment character if it is preceded by whitespace or the beginning of the line.
As a (greedy) regular expression, this can be written as `(^|\s+)#(\s+.*|)$`.

Whitespace preceding the `#` character is considered part of the comment.
