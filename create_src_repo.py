#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  create_src_repo.py
#  Create the <semester>-www-src repo.

import sys

from github import Github

def main(args):
    # Arguments:
    github_username = args[1]
    github_password = args[2]
    repo_name = args[3]
    description = args[4]
    
    g = Github(github_username, github_password)
    org = g.get_organization("ee16b")
    new_repo = org.create_repo(name=repo_name, description=descriptiong, has_wiki=False, has_issues=False, private=True)
    bots_team = next(filter(lambda team: team.name == "bots", org.get_teams()))
    bots_team.set_repo_permission(new_repo, "admin")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
