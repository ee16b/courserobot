#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  hw_get_num_questions.py
#  Script that calls the course manager framework and gets the number of questions for a given homework.
#  Arguments: <hw num>

import sys

from config import Config, set_global_config
from homework import Homework

def main(args):
    set_global_config(Config(True))
    hw = Homework(int(args[1]))
    print(hw.get_num_questions())
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
