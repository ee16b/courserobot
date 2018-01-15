#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  homework_interface
#  Script that calls the course manager framework and performs various actions.
#  Arguments: <hw num>
import argparse
import sys

from config import Config, set_global_config
from homework import Homework

VALID_ACTIONS = [
    "make_homework",
    "make_homework_local",
    "push_homework",
    "post_piazza",
    "make_solutions",
    "make_solutions_local",
    "make_self_grades"
]

def main(args):
    set_global_config(Config(True))
    hw = Homework(args.hw_num)
    action = args.action
    if action == "make_homework":
        hw.build_homework()
        hw.push_homework()
    elif action == "make_homework_local":
        hw.build_homework()
    elif action == "push_homework":
        hw.push_homework()
    elif action == "post_piazza":
        hw.post_to_piazza()
    elif action == "make_solutions":
        hw.build_solutions()
        hw.push_solutions()
    elif action == "make_solutions_local":
        hw.build_solutions()
    elif action == "make_self_grades":
        hw.generate_self_grade_form()
    else:
        assert False, "Should not reach here. Is an action in VALID_ACTIONS not implemented?"
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("hw_num", metavar="HW_NUM", help="Homework number (e.g. 10)", type=int)
    parser.add_argument("action", metavar="ACTION", help="Valid action to perform with the homework", action="store", type=str,
                        choices=VALID_ACTIONS)
    args = parser.parse_args()
    sys.exit(main(args))
