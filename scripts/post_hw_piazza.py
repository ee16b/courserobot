#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# For posting on Piazza

import json
import os

import time
from collections import Callable
from typing import Tuple

from config import Config

from piazza_api import Piazza
import piazza_api.exceptions

IMG_URL_TEMPLATE = "http://inst.eecs.berkeley.edu/~ee16b/{tag}/hw_pics/{HWNO}/prob{QNO}.png"

SOLUTIONS_POST_TITLE = "Homework {hw_num} solutions and grading form"
SOLUTIONS_POST_TEMPLATE = """
<ul><li><a href="http://inst.eecs.berkeley.edu/~ee16b/{tag}/hw/hw{hw_num}/sol{hw_num}.pdf">solutions</a></li></ul>
You can also start submitting self-grades for HW{hw_num}. You should submit a file on Gradescope generated from the <a href="http://inst.eecs.berkeley.edu/~ee16b/{tag}/grade/hw{hw_num}.html">self-grading form</a>.

#pin
"""


# TODO: implement unpin

def post_hw_piazza(hw_num: int, question_number: int) -> None:
    """Create a post for the given homework number and question number."""
    hw_str = str(hw_num)
    qno_str = str(question_number)

    title = "Homework {HWNO} question {QNO}".format(HWNO=hw_num, QNO=question_number)
    content = ("<img src=\"" + IMG_URL_TEMPLATE + """" alt=""><br>#pin""").format(
        tag=Config.get_global().get_semester_tag(), HWNO=hw_num,
        QNO=question_number)

    post_db, post_db_loc = read_post_db(hw_num)

    # Don't try to create a post if it already exists.
    # TODO: update post instead
    if qno_str not in post_db['hws'][hw_str]:
        cid = create_piazza_post(title, content, folder="hw" + hw_str)
        # Store cid of post for unpin, etc
        post_db['hws'][hw_str][qno_str] = cid

    print(post_db)

    write_post_db(post_db, post_db_loc)


def post_solutions_piazza(hw_num: int) -> None:
    """Create the solutions/self-grade post for the given homework."""
    hw_str = str(hw_num)

    title = SOLUTIONS_POST_TITLE.format(hw_num=hw_num)
    content = SOLUTIONS_POST_TEMPLATE.format(
        hw_num=hw_num,
        tag=Config.get_global().get_semester_tag()
    )

    post_db, post_db_loc = read_post_db(hw_num)

    # Don't try to create a post if it already exists.
    # TODO: update post instead
    if hw_str not in post_db['hw_sols']:
        cid = create_piazza_post(title, content, folder="hw" + hw_str)
        # Store cid of post for unpin, etc
        post_db['hw_sols'][hw_str] = cid

    print(post_db)

    write_post_db(post_db, post_db_loc)


def create_piazza_post(title: str, content: str, folder: str) -> int:
    """Create a piazza post from the given parameters and return the post's CID."""
    EMAIL = Config.get_global().piazza_email
    PWD = Config.get_global().piazza_password
    ID = Config.get_global().piazza_id

    p = Piazza()
    p.user_login(EMAIL, PWD)
    post = p.network(ID)

    while True:
        try:
            result = post.create_post(
                title=title,
                content=content,
                nid=ID,
                folder=folder
            )
        except piazza_api.exceptions.RequestError as e:
            str_e = str(e)
            if "posting too quickly" in str_e:
                # Piazza has posting time limits, grumble grumble
                # "Sorry! It looks like you are posting too quickly--wait a second and try again."

                # Try again
                time.sleep(0.4)
                continue
            else:
                # Don't handle this
                raise e

        # All done now!
        break

    return int(result['nr'])


def write_post_db(post_db: dict, post_db_loc: str) -> None:
    """Write post db back to disk."""
    with open(post_db_loc, 'w') as f:
        json.dump(post_db, f)


def read_post_db(hw_num: int) -> Tuple[dict, str]:
    """Read post db from disk.
    :return: Returns the post_db and its location."""
    hw_str = str(hw_num)

    post_db_loc = os.path.join(Config.get_global().release_loc, '_piazza-db.json')
    try:
        post_db = json.loads(open(post_db_loc, 'r').read())
    except IOError:
        # If not exists or error, assume empty db
        post_db = {}
    if 'hws' not in post_db:
        post_db['hws'] = {}  # Homeworks
    if 'hw_sols' not in post_db:
        post_db['hw_sols'] = {}  # Homework solution posts
    if hw_str not in post_db['hws']:
        post_db['hws'][hw_str] = {}
    return post_db, post_db_loc
