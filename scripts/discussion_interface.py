#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  discussion_interface.py
#  Script that calls the course manager framework and performs various actions.
#  Arguments: <discussion tag>
import argparse
import sys

from config import Config, set_global_config
from discussion import Discussion

VALID_ACTIONS = [
    "make_discussion",
    "make_discussion_local",
    "make_answers",
    "make_answers_local"
]

def main(args):
    set_global_config(Config(True))
    disc = Discussion(args.discussion_tag)
    action = args.action
    if action == "make_discussion":
        disc.build_discussion()
        disc.push_discussion()
    elif action == "make_discussion_local":
        disc.build_discussion()
    elif action == "make_answers":
        disc.build_answers()
        disc.push_answers()
    elif action == "make_answers_local":
        disc.build_answers()
    else:
        assert False, "Should not reach here. Is an action in VALID_ACTIONS not implemented?"
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("discussion_tag", metavar="DISCUSSION_TAG", help="Discussion tag (e.g. 4A, 5B, etc.)", type=str)
    parser.add_argument("action", metavar="ACTION", help="Valid action to perform", action="store", type=str,
                        choices=VALID_ACTIONS)
    args = parser.parse_args()
    sys.exit(main(args))
