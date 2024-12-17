"""
This scripts extracts authors from dblp.xml and creates a map that is easier to process in other files.

Download dblp.xml from https://dblp.org/xml/ and extract it using gunzip
"""

import argparse
import html
import json
import xml.sax
import xml.sax.saxutils
from collections import defaultdict
from pathlib import Path


class AuthorFilter(xml.sax.saxutils.XMLFilterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack = [None]
        self.attrs = []
        self.pid_map = {}
        self.text_active = None
        self.current_pid = None

    def startElement(self, name, attrs):
        if name == "www":
            atribs = dict(attrs.items())
            if atribs['key'].startswith('homepages'):
                self.stack.append(name)
                pid = atribs['key'][len('homepages/'):]
                self.current_pid = defaultdict(list)
                self.current_pid['pid'] = pid
        elif self.current_pid is not None:
            self.text_active = []
            self.attrs.append(dict(attrs.items()))

    def endElement(self, name):
        if name == "www" and self.stack[-1] == "www":
            self.stack.pop()
            if self.current_pid:
                self.pid_map[self.current_pid['pid']] = self.current_pid
                self.current_pid = None
        elif self.current_pid:
            key = name
            atribs = self.attrs.pop()
            if atribs and 'type' in atribs and atribs.get('label', '') != 'former':
                key = atribs['type']
            value = html.unescape("".join(self.text_active))
            if name not in ("title",):
                self.current_pid[key].append(value)
            if key == "url" and value.startswith("https://orcid.org/"):
                self.current_pid["orcid"].append(value[len("https://orcid.org/"):])
            self.text_active = None

    def characters(self, content):
        if self.text_active is not None:
            self.text_active.append(content)

    def skippedEntity(self, name):
        if self.text_active is not None:
            self.text_active.append(f"&{name};")

def main():
    parser = argparse.ArgumentParser(
        prog='create_dblp_map',
        description='Extract authors from DBLP')
    parser.add_argument(
        '-i', '--input', default="input/dblp.xml",
        help="Input xml file")
    parser.add_argument(
        '-o', '--output', default="output/dblp_map.json",
        help="Output json file")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    parser = xml.sax.make_parser()
    reader = AuthorFilter(parser)
    reader.parse(args.input)

    with open(args.output, "w") as f:
        json.dump(reader.pid_map, f)

    
if __name__ == "__main__":
    main()
    