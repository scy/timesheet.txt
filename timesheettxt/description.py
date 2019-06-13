import re

class BillableExtractor:
    regex = re.compile(r"(?:^|\s+)(!?\$)(?:\s+|$)")

    def extract(self, text):
        match = BillableExtractor.regex.search(text)
        if not match:
            return ({"billable": None}, text)
        else:
            return ({
                "billable": match[1] == "$",
            }, BillableExtractor.regex.sub(" ", text))

class IssueIDExtractor:
    regex = re.compile(r"^(#?\d+|[A-Z]{2,}-\d+)(:\s+|$)")

    def extract(self, text):
        match = IssueIDExtractor.regex.search(text)
        if not match:
            return ({"issue": None}, text)
        return ({
            "issue": match[1],
        }, IssueIDExtractor.regex.sub("", text))
