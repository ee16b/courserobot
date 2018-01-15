#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  config.py
#  Configuration for the course manager.

import os

import yaml

GLOBAL_CONFIG = None
# Set the global config.
def set_global_config(config):
    global GLOBAL_CONFIG # pylint: disable=global-statement

    GLOBAL_CONFIG = config

class Config:
    @staticmethod
    def get_global():
        if GLOBAL_CONFIG is None:
            raise ValueError("Must call set_global_config with Config object!")
        return GLOBAL_CONFIG

    def __init__(self, from_env=True):
        # Where to find general.yaml (general settings)
        self.general_yaml = os.environ['GENERAL_YAML'] if from_env else ""

        # Makefile location (root of courserobot repo)
        self.makefile_loc = os.environ['MAKEFILE_LOC'] if from_env else ""

        # Colon-separated list of content repos to be pulled.
        self.content_repos = str(os.environ['CONTENT_REPOS']).split(':') if from_env else []

        # Path to notes location
        #self.notes_loc = os.environ['NOTES_LOC'] if from_env else ""

        # Path to homework location
        self.hw_loc = os.environ['HW_LOC'] if from_env else ""

        # Path to discussion location
        self.disc_loc = os.environ['DISC_LOC'] if from_env else ""

        # Path to practice problems location
        #self.practice_loc = os.environ['PRACTICE_LOC'] if from_env else ""

        # Path to release location
        self.release_loc = os.environ['RELEASE_LOC'] if from_env else ""

        # Course Manager Piazza account e-mail
        self.piazza_email = os.environ['PIAZZA_EMAIL'] if from_env else ""

        # Course Manager Piazza account password
        self.piazza_password = os.environ['PIAZZA_PASSWORD'] if from_env else ""

    def get_general_yaml(self):
        """Get the dictionary corresponding to content/general.yaml.
        """
        with open(self.general_yaml, "r") as f:
            general_yaml = yaml.load(f)
        return general_yaml

    def get_semester_tag(self) -> str:
        """Get semester tag (e.g. fa17)."""
        return self.get_general_yaml()['tag']

    @property
    def piazza_id(self) -> str:
        return self.get_general_yaml()['piazza_id']

    @property
    def scripts_dir(self) -> str:
        """Get the path to the folder containing all the scripts."""
        return str(os.path.join(self.makefile_loc, "scripts"))

    def get_taft_cmd(self, template_file):
        """Get the taft shell command to compile a certain template."""
        return ' '.join([
            'taft',
            '--helper handlebars-helper-range',
            '--helper handlebars-fs',
            '--helper handlebars-helpers',
            '--helper handlebars-helper-moment',
            "--helper '" + self.makefile_loc + "/helpers/*.js'",
            "--partial '" + self.makefile_loc + "/sub-templates/*.html'",
            "--data '" + self.makefile_loc + "/autograder/*.yaml'",
            '--dest-dir ' + self.release_loc,
            template_file
        ])
