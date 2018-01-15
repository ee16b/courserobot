Course Robot (New Course Manager for Gradescope)
================================================

# Setup

1. Start a new AWS instance with Ubuntu 17.10. Make sure to enable SSH (port 22) and mosh (port 60000-61000 UDP). We recommend at least 10GB of disk space. ![Ports to enable](images/ports.png)
2. Copy the the course robot private key (`id_rsa`) and credentials file (`credentials.sh`) to the instance: (example) `scp id_rsa credentials.sh ubuntu@<instance IP>:~/`
3. SSH into the instance.
4. Clone this repo and enter it: `cd ~; git clone https://github.com/ee16b/courserobot.git && cd courserobot`
5. Copy the user credentials file and modify it: `cp user_credentials.sh.template ~/user_credentials.sh; vim ~/user_credentials.sh`. This is required in order to set up the infrastructure on Github.
6. Copy the general settings file and modify it: `cp general.yaml.template ~/general.yaml; vim ~/general.yaml`. Be sure to update at least the tag and `piazza_id`.
7. Run `sudo ./setup.sh` ONCE to initialize everything.

# Pre-Course Setup

## Piazza

Invite the course manager account (likely `course.manager.ee16 AT gmail.com`, replace `AT` with `@`) to join the class on Piazza as a TA (under "Enroll Professors/TAs").

## GSI Pictures

1. Obtain pictures from each TA on Slack.
2. Crop to square ratio.
3. Resize to about 1000x1000px, with quality of about 80 to save space.
4. ...

# User Guide

## Calendar

## Homework

### Homework YAML

In each homework directory where the latex files are stored (example: `[ee16b-content repo]/sp18/hws/1/info.yaml`), include an **info.yaml** file with:

```
questionParts: [a, a, b, b, c, a]
optionalParts: ["3a", 4]
```

This indicates that the homework consists of 1a, 2a, 3a-b, 4a-b, 5a-c, 6a. If there are no sub-parts to a problem, we will just call it #a on the self grader. Optional parts can be specified as # only (i.e. 2 should not be graded) or as a string "2a", which indicates that 2a should not be graded. If, for example, you don't want 3a and 4b to be graded, you should specify `optionalParts: ["3a", "4b"].

### Releasing Homework

### Releasing Self-Grades

## Discussions

### Releasing Discussions

### Releasing Answers

## Labs

## Lecture Notes

# Info

## Semester tags

Examples:
- Fall 2017 -> fa17
- Spring 2018 -> sp18
- Fall 2018 -> fa18
- Spring 2019 -> sp19
- Summer 2019 -> su19
- Fall 2019 -> fa19

(google doc) https://github.com/ee16b/gradebook2

TODO: lab

TODO: update/generate homework.php
