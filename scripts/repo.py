#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  repo.py
#  Repository related actions.

import subprocess

from config import Config


def update_inst_server() -> None:
    """Update the website on inst."""
    tag = Config.get_global().get_semester_tag()

    print("Updating inst server")
    cmd = """ssh ee16b@cory.eecs.berkeley.edu "cd ~/public_html/{tag}/src && git pull --rebase" """.format(tag=tag)
    print(subprocess.check_output(cmd, shell=True))


def commit_all_update_push(repo_root: str, comment: str) -> None:
    """Commit all changes, pull rebase, and push."""
    commit_all(repo_root, comment)
    pull_repo(repo_root, rebase=True)
    push_repo(repo_root)


def commit_all(repo_root: str, comment: str) -> None:
    """Commit all changes to the repo."""
    print(subprocess.check_output("git add -A", cwd=repo_root, shell=True))
    print(subprocess.check_output("git commit --allow-empty -m \"{comment}\"".format(comment=comment),
                                  cwd=repo_root, shell=True))


def push_repo(repo_root: str, remote: str = "origin", branch: str = "master") -> None:
    """Push the given repo to origin."""
    print(subprocess.check_output("git push {remote} {branch}".format(remote=remote, branch=branch), cwd=repo_root,
                                  shell=True))


def pull_repo(repo_root: str, rebase: bool = True) -> None:
    """Pull changes for the given repo from upstream."""
    print(subprocess.check_output("git pull{rebase_or_not}".format(rebase_or_not=" --rebase" if rebase else ""),
                                  cwd=repo_root,
                                  shell=True))
