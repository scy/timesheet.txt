import re

class IssueIDExtractor:
    regex = re.compile(r"^(#?d+|[A-Z]{2,}-\d+)(:\s+|$)")

    def extract(self, text):
        match = IssueIDExtractor.regex.match(text)
        if not match:
            return ({"issue": None}, text)
        return ({
            "issue": match[1],
        }, IssueIDExtractor.regex.sub("", text))
