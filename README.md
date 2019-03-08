# wca-statistics

This repository is meant to provide statistics for the WCA Statistics [group on Facebook](https://www.facebook.com/groups/439995439706174). It's also my repo to study data science with Python.

Later, I'll let a page available with all the data available.

## Getting started

- Download this repo and execute `./run.sh`. You'll need python3 and some packages like [numpy](http://www.numpy.org/) and [pandas](https://pandas.pydata.org/). You'll be asked to download the WCA export. Some statistics can take a time to run.
- To add a new statistics, place the .py in scr/. The filename must start with stat- (eg. stat-foo.py). This program must create a dictionary d containing d["title"], d["table"] and d["labels"]. The table is the content of the statistic and it must be a python list of lists. Labels are a list of string and title a string. You can use build_page(d) from utils.py.
