#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  read_tag.py
#  Read tag from general.yaml.
#  Arguments: <path to general.yaml>
import sys
import yaml


def main(args):
    with open(args[1], "r") as f:
        general = yaml.load(f)
    tag = general['tag']
    if tag == "REPLACE_ME":
        print("Must replace tag with the semester tag (e.g. sp18) in general.yaml", file=sys.stderr)
        return 1
    else:
        print(tag)
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
