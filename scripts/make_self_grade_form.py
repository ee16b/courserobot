#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  make_self_grade_form
#  Script that calls the course manager framework and generates a self-grade
#  form.
#  Arguments: <hw num>

import sys

from config import Config, set_global_config
from homework import Homework

def main(args):
    set_global_config(Config(True))
    hw = Homework(int(args[1]))
    hw.generate_self_grade_form()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
