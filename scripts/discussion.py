#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  discussion.py
#  Discussion related actions.

import os
import shutil
import string
import subprocess

import sys
import yaml

import post_hw_piazza

from config import Config
import repo


class Discussion:
    def __init__(self, discussion_tag: str) -> None:
        self.discussion_tag = str(discussion_tag)  # type: str

    def build_dis_pdf(self) -> None:
        """Build the discussion pdf and place it into the output at the release folder."""
        print("Building discussion PDF")
        self.build_pdf("dis{discussion_tag}.pdf".format(discussion_tag=self.discussion_tag))

    def build_ans_pdf(self) -> None:
        """Build the answers pdf and place it into the output at the release folder."""
        print("Building answers PDF")
        self.build_pdf("ans{discussion_tag}.pdf".format(discussion_tag=self.discussion_tag))

    def build_sol_pdf(self) -> None:
        """Build the staff pdf and place it into the output at the release folder."""
        print("Building staff PDF")
        self.build_pdf("sol{discussion_tag}.pdf".format(discussion_tag=self.discussion_tag))

    def build_pdf(self, pdf: str) -> None:
        """Build the specified pdf (e.g. prob6.pdf) and copy it to the output at the release folder."""

        discussion_src_path = os.path.join(Config.get_global().disc_loc, self.discussion_tag)  # e.g. dis/0B
        pdf_full_path = os.path.join(discussion_src_path, pdf)

        # Remove previous build product and build.
        print(subprocess.check_output(["rm", "-f", pdf_full_path], cwd=discussion_src_path,
                                      shell=False))
        print("Running 'make' in {path}".format(path=discussion_src_path))
        print(subprocess.check_output("make", cwd=discussion_src_path, shell=True))
        if not os.path.isfile(pdf_full_path):
            print("Requested pdf {pdf} did not build", file=sys.stderr)
            sys.exit(1)
        # Copy to release folder.
        shutil.copy(pdf_full_path, self.discussion_release_dir)

    def build_discussion(self) -> None:
        """Build the discussion."""
        repo.pull_repo(Config.get_global().release_loc)
        self.build_dis_pdf()
        # TODO: also bundle iPython/data files if present

    def push_release_repo(self, comment: str = ""):
        """Commit all changes to the release repo and push for inst."""
        if comment == "":
            comment = "Update repo for dis{discussion_tag}".format(discussion_tag=self.discussion_tag)
        repo.commit_all_update_push(Config.get_global().release_loc, comment)

    def push_discussion(self):
        """Push out this homework to the website and Piazza."""
        self.push_release_repo()
        repo.update_inst_server()

    def build_answers(self) -> None:
        """Build answers and put them into the release location."""
        repo.pull_repo(Config.get_global().release_loc)
        self.build_ans_pdf()
        # TODO: also bundle iPython/data files if present

    def push_answers(self) -> None:
        """Push answers to website."""
        self.push_release_repo()
        repo.update_inst_server()

    @property
    def discussion_release_dir(self):
        """Return the path to this discussion's release folder.
        Example: dis/0B/"""

        dis_dir = os.path.join(Config.get_global().release_loc, "dis",
                               self.discussion_tag)
        template_dir = os.path.join(Config.get_global().release_loc, "dis", "_template")

        # Make sure it exists first.
        if not os.path.isdir(dis_dir):
            print(subprocess.check_output(["rm", "-rf", dis_dir], shell=False))
            print(subprocess.check_output(["cp", "-r", template_dir, dis_dir], shell=False))

        return dis_dir
