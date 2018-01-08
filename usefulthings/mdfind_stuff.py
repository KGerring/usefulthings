#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = mdfind_stuff
# author=KGerring
# author_email=''
# date = 11/9/17
""" filename = mdfind_stuff"""
from __future__ import absolute_import, unicode_literals # isort:skip
from startups import *
import sys, os
import regex
import yaml

SIMPLE_DATE_RE = regex.compile(r'(?<date>(?<month>\d*)\/(?<day>\d*)\/(?<year>\d*))\-*(?P>date)?')  # use captures

AON_RE = regex.compile('(AND|OR|NOT)')
LIST_METADATA_TAGS = 'mdimport -A | cut -f 2  -d "\'"| sort'


MDFIND_SCHEMA_DICT, MDFIND_SCHEMA_LIST = list(
	yaml.safe_load_all(open('/Users/kristen/PycharmProjects/proj/startups/startups/data/mdfind_schema.yaml')))






if __name__ == '__main__': print(__file__)