#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  update_repos.py
#  Script that pulls changes from upstream for a given repo.
#  Arguments: <hw num>
import argparse
import sys

from config import Config, set_global_config
import repo

VALID_REPOS = [
    "release",
    "content_repos"
]

def main(args):
    set_global_config(Config(True))
    repo_name = str(args.repo)
    if repo_name == "release":
        repo.pull_repo(Config.get_global().release_loc)
    elif repo_name == "content_repos":
        for repo_loc in Config.get_global().content_repos:
            repo.pull_repo(repo_loc)
    else:
        assert False, "Shouldn't reach here. Is some repo unimplemented?"
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", metavar="REPO", help="Which repo to update", action="store", type=str,
                        choices=VALID_REPOS)
    args = parser.parse_args()
    sys.exit(main(args))
