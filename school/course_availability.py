"""
IMPORTANT: DO NOT USE THIS SCRIPT TO DOS THE SCHOOL SERVER. THIS IS
INTENDED TO MAKE IT EASIER TO CHECK WHICH COURSES ARE OPEN WITHOUT
HAVING TO LOG IN AND MANUALLY GO THROUGH EACH STEP TO SELECT THE
TERM AND DEPARTMENT. USE IT ONCE AND THEN REGISTER. AT MOSE USE IT
ONCE EVERY 15 MINUTES, ABOUT THE RATE AT WHICH A HUMAN USING A MOUSE
WOULD REFRESH THEIR OWN SEARCHES.

This is a single-module script to scrape OSCAR for course openings.
It works for Summer and Fall of 2016. There is no guarantee it will
work for future terms unless you change the CRNs and term dates.

Additionally, if you are using this in the future, you will want to
ensure that the OSCAR API has not changed and this url structure still
works. I will likely maintain this myself until I have graduated and
no longer.

(c) Adam Acosta 2016
"""

from __future__ import print_function

import re
import sys
import argparse

from urllib2 import urlopen
from bs4 import BeautifulSoup


class TermDependent(argparse.Action):
    """Custom Action to ensure user selects a term if specifying crn."""

    def __call__(self, parser, namespace, values, option_string=None):
        term = getattr(namespace, 'term')
        # User tried to specify a crn without specifying a term
        if term == 'all':
            parser.error("must specify term to use crn")
        else:
            setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument('--term', type=str, default='all',
                    help='the term you wish to check')
parser.add_argument('--crn', type=str, default=None,
                    action=TermDependent,
                    help='use this if you only want to check one CRN')

crns = {
    'summer':
    {'intro to info security': '56393',
     'software dev process': '55424',
     'software arch and design': '56394',
     'software analysis and test': '56395',
     'comp photography': '55805',
     'knowledge-based ai': '55806',
     'artificial intelligence for robotics': '55426',
     'intro to operating systems': '55804',
     'reinforcement learning': '56396',
     'embedded software': '56397'},
    'fall':
    {'high performance computing': '89826',
     'data and visual analytics': '91202',
     'big data for health': '91201',
     'intro to info security': '89823',
     'adv operating systems': '88770',
     'computer networks': '88771',
     'network security': '91203',
     'high performance computer arch': '88775',
     'software dev process': '88772',
     'software arch and design': '88776',
     'software analysis and test': '91197',
     'db sys concepts and design': '91198',
     'intro health informatics': '88777',
     'educ tech foundations': '90228',
     'comp photography': '89821',
     'computer vision': '90192',
     'computability and algorithms': '88778',
     'artificial intelligence': '91199',
     'knowledge-based ai': '88779',
     'machine learning': '88773',
     'mach learning for trading': '89824',
     'artificial intelligence for robotics': '88774',
     'intro to operating systems': '89822',
     'reinforcement learning': '89825',
     'embedded software': '91200',
     'cyber-physical systems': '91581'},
}

terms = {'summer': '201605', 'fall': '201608'}


def get_seats(term, crn):
    """Enter the term and crn and return the number of open seats."""

    # This is the API as of April 2016
    url = "https://oscar.gatech.edu/pls/bprod/bwckschd" + \
        ".p_disp_detail_sched?term_in={}&crn_in={}".format(term, crn)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Uncomment one of these to test
    # return url
    # return soup
    # return text

    # Available seats is the third column in the table
    seats = re.search('(?<=Seats\n[0-9]{3}\n[0-9]{3}\n)[0-9]{1,3}', text)
    if seats is not None:
        return seats.group(0)

    # In this case, the course only has double-digit enrollment
    # Do this twice because re.search() only accepts fixed-length strings
    seats = re.search('(?<=Seats\n[0-9]{3}\n[0-9]{2}\n)[0-9]{1,3}', text)
    return seats.group(0)


if __name__ == '__main__':
    args = parser.parse_args()

    # I am double-checking here that you are not DOSing the server
    ans = raw_input("Have you checked in the last 15 minutes? (y/n): ")
    if str(ans).lower() != 'n':
        print("Please wait at least 15 minutes.")
        sys.exit(0)

    # Single CRN
    if args.crn:
        print(get_seats(terms[args.term], args.crn))
        sys.exit(0)

    # Single term
    if args.term != 'all':
        for course in crns[args.term]:
            print(course, get_seats(terms[args.term], crns[args.term][course]))
        sys.exit(0)

    # Go ahead and check
    for term in terms:
        for course in crns[term]:
            print(term, course, get_seats(terms[term], crns[term][course]))
    sys.exit(0)
