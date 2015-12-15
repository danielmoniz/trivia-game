trivia-game is intended to dynamically generate questions and answers for a
trivia game. It uses the Wikipedia API to pull up-to-date information. The user
must provide lists of entities (eg. cities, people, wars, etc.) in separate
files, as well as questions for each entity. The program attempts to pull the
answer for each question and outputs the relevant information.

Notes
==========

* This project is in early alpha at best.
* The program may fail to retrieve answers for some entities. This is because
  of a lack of consistency on the part of Wikipedia and must be accounted for.

Setup
============

Run

    pip install -r requirements.txt

to set up the Python environment.

Run
=========

Simply run

    python api.py

to generate the questions and answers. Note that the Wikipedia API is used to
poll data for each entity (eg. "Abraham Lincoln"), and so it will take some
time to run.
