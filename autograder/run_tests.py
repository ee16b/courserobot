import json
import yaml
import sys
import glob

fileStream = open("hw-helper.yaml", "r")
info = yaml.load(fileStream)
hwNum = info['hwNum']
questions = info['questions']
selfGradeMax = info['selfGradeMax']
 
results_dict = {}               # Create results dict as per gradescope's autograder specifications
results_dict["score"] = 0       # Set total score to be 0 for now
results_dict["tests"] = []      # Create empty array of tests, to be filled in by the for loops

pathToSubmission = "../submission/*"

if __name__ == '__main__':  
  for submissionFile in glob.glob(pathToSubmission):
    with open(submissionFile) as data_file:     # Student's selfgrades files must be named selfgrades-#.txt
      data = json.load(data_file)
      for question in questions:
        id = question['id']
        if (question['graded']):
          results_dict["score"] += float(data["q" + id])
          results_dict["tests"].append({
            "score": float(data["q" + id]), 
            "max_score": selfGradeMax, 
            "name": "Question {id}".format(id = id), 
            "output": data.get("q" + id + "-comment", "")
          })
        else:
          results_dict["tests"].append({
            "score": float(data["q" + id]), 
            "max_score": selfGradeMax, 
            "name": "[NOT INCLUDED IN FINAL SCORE] Question {id}".format(id = id), 
            "output": data.get("q" + id + "-comment", "")
          })

      with open('/autograder/results/results.json', 'w') as outfile:
        json.dump(results_dict, outfile)
