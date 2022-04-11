from html.parser import HTMLParser


class SimpleHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.strings = []

    def handle_data(self, data):
        self.strings.append(data)


def html_to_strings(html):
    parser = SimpleHtmlParser()
    parser.feed(html)
    return parser.strings


def html_to_dict(html):
    d = dict()
    for string in html_to_strings(html):
        pair = string.split(":")
        if len(pair) > 1:
            d[pair[0].strip()] = pair[1].strip()
    return d
