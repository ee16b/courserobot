#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  homework.py
#  Homework related actions.

import os
import shutil
import string
import subprocess

import sys
import yaml

import post_hw_piazza

from config import Config
import repo

class Homework:
    def __init__(self, hw_num: int) -> None:
        self.hw_num = int(hw_num)  # type: int

    def get_hw_info_yaml(self):
        """Get a dictionary of the info.yaml file corresponding to the given homework.
        """
        return yaml.load(open(Config.get_global().hw_loc + "/" + str(self.hw_num) + "/info.yaml", "r"))

    def get_hw_info(self):
        """Get the dictionary corresponding to the hw-helper.yaml file.
        """
        info = self.get_hw_info_yaml()
        general_yaml = Config.get_global().get_general_yaml()

        questions = []
        output_dict = {}
        output_dict['hwNum'] = self.hw_num
        output_dict['questions'] = questions

        questionParts = info['questionParts']
        optionalParts = []
        if 'optionalParts' in info:
            optionalParts = info['optionalParts']

        numQuestions = len(questionParts)
        output_dict['numQuestions'] = numQuestions

        letters = list(string.ascii_lowercase)
        numGradedQuestions = 0
        for questionIdx in range(len(questionParts)):
            numParts = letters.index(questionParts[questionIdx]) + 1
            for partIdx in range(numParts):
                part = letters[partIdx]
                questionID = str(questionIdx + 1) + part
                matchNotGraded = False
                for optionalPart in optionalParts:
                    if not matchNotGraded:
                        matchNotGraded = questionID.startswith(str(optionalPart))
                if not matchNotGraded:
                    numGradedQuestions += 1

                questions.append({'id': questionID, 'graded': (not matchNotGraded)})

        output_dict['numGraded'] = numGradedQuestions

        selfGradeScale = general_yaml['selfGradeScale']
        selfGradeMax = max(list(selfGradeScale.keys()))

        output_dict['selfGradeMax'] = selfGradeMax
        return output_dict

    def get_num_questions(self):
        """Get the number of questions in this homework.
        """
        return self.get_hw_info()['numQuestions']

    def get_grading_points(self):
        """Get the total number of points that this homework is worth.
        e.g. if it has 3 problems and the max worth is 10, then this homework is
        worth 30 points.
        """
        hw_info = self.get_hw_info()
        return hw_info['numGraded'] * hw_info['selfGradeMax']

    def build_prob_pdf(self) -> None:
        """Build the homework pdf and place it into the output at the release folder."""
        print("Building problem set PDF")
        self.build_pdf("prob{hw_num}.pdf".format(hw_num=self.hw_num))

    def build_sol_pdf(self) -> None:
        """Build the solutions pdf and place it into the output at the release folder."""
        print("Building solutions PDF")
        self.build_pdf("sol{hw_num}.pdf".format(hw_num=self.hw_num))

    def build_pdf(self, pdf: str) -> None:
        """Build the specified pdf (e.g. prob6.pdf) and copy it to the output at the release folder."""

        homework_src_path = os.path.join(Config.get_global().hw_loc, str(self.hw_num))  # e.g. hws/4 in ee16b-content
        pdf_full_path = os.path.join(homework_src_path, pdf)

        # Remove previous build product and build.
        print(subprocess.check_output(["rm", "-f", pdf_full_path], cwd=homework_src_path,
                                      shell=False))
        print("Running 'make' in {path}".format(path=homework_src_path))
        print(subprocess.check_output("make", cwd=homework_src_path, shell=True))
        if not os.path.isfile(pdf_full_path):
            print("Requested pdf {pdf} did not build", file=sys.stderr)
            sys.exit(1)
        # Copy to release folder.
        shutil.copy(pdf_full_path, self.homework_release_dir)

    def build_piazza_images(self) -> None:
        """Build the hw_pics for Piazza."""
        print("Building Piazza images")
        make_piazza_imgs = os.path.join(Config.get_global().scripts_dir, "make_piazza_imgs.sh")

        cmd = [
            make_piazza_imgs,
            str(self.hw_num),
            Config.get_global().hw_loc,
            Config.get_global().scripts_dir,
            os.path.join(Config.get_global().release_loc, "hw_pics", str(self.hw_num))
        ]
        print("Running command " + ' '.join(cmd))

        print(subprocess.check_output(cmd, shell=False))

    def build_homework(self) -> None:
        """Build the homework problem set (PDF and piazza images)."""
        repo.pull_repo(Config.get_global().release_loc)
        self.build_prob_pdf()
        # TODO: also bundle iPythons if present
        self.build_piazza_images()
        # TODO: modify/generate homework.php

    def push_release_repo(self, comment: str = ""):
        """Commit all changes to the release repo and push for inst."""
        if comment == "":
            comment = "Update repo for hw{hw_num}".format(hw_num=self.hw_num)
        repo.commit_all_update_push(Config.get_global().release_loc, comment)

    def post_to_piazza(self):
        for question_number in range(1, self.get_num_questions() + 1):
            post_hw_piazza.post_hw_piazza(hw_num=self.hw_num, question_number=question_number)
        self.push_release_repo(comment="Update piazza_db")

    def post_solutions_to_piazza(self):
        post_hw_piazza.post_solutions_piazza(hw_num=self.hw_num)
        self.push_release_repo(comment="Update piazza_db")

    def push_homework(self):
        """Push out this homework to the website and Piazza."""
        self.push_release_repo()
        repo.update_inst_server()
        self.post_to_piazza()

    def build_solutions(self) -> None:
        """Build solutions and put them into the release location."""
        repo.pull_repo(Config.get_global().release_loc)
        self.build_sol_pdf()
        # TODO: also bundle iPythons if present
        self.generate_self_grade_form()

    def push_solutions(self) -> None:
        """Push solutions to website and Piazza."""
        self.push_release_repo()
        repo.update_inst_server()
        self.post_solutions_to_piazza()

    def generate_self_grade_form(self):
        """Build the self-grade form and put it an an appropriate location."""
        self_grade_form_output_location = os.path.join(Config.get_global().release_loc, "grade",
                                                       "hw{hw_num}.html".format(hw_num=self.hw_num))

        # Write autograder/hw-helper.yaml
        yamlFile = open(Config.get_global().makefile_loc + "/autograder/hw-helper.yaml", "w")
        yaml.dump(self.get_hw_info(), yamlFile)

        # Run taft to generate the self-grade form.
        print(subprocess.check_output(Config.get_global().get_taft_cmd("self-grade.html"), cwd=Config.get_global().makefile_loc, shell=True))
        shutil.move(Config.get_global().release_loc + "/self-grade.html", self_grade_form_output_location)
        assert os.path.isfile(self_grade_form_output_location), "Self-grade form should generate"
        print("Self-grade form at " + self_grade_form_output_location)

        # Autograder zip file generation.
        print(subprocess.check_output(
            "zip -rj %s/autograder%s-%sp.zip %s/autograder" % (
                self.autograder_release_dir,
                str(self.hw_num),
                str(self.get_grading_points()),
                Config.get_global().makefile_loc)
            , shell=True))

    @property
    def autograder_release_dir(self):
        """Return the path to the autograder folder in the release dir."""
        return os.path.join(Config.get_global().release_loc, "hw_autograder")

    @property
    def homework_release_dir(self):
        """Return the path to this homework's release folder.
        Example: hw/hw1/"""

        # Make sure it exists first.
        hw_dir = os.path.join(Config.get_global().release_loc, "hw", "hw{num}".format(num=self.hw_num))
        os.makedirs(hw_dir, exist_ok=True)

        return hw_dir
