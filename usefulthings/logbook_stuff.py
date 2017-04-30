#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = logbook_stuff
# author=AutisticScreeching
# date = 3/15/17
import sys, os
import logbook

from logbook.queues import MultiProcessingHandler
from multiprocessing import Queue



testlog = '/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/test.log'
extralog = '/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/extra.log'

SearchLog = logbook.FileHandler('/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/extra.log',
                                format_string='[{record.time:%Y-%m-%dT%H:%M:%S}] {record.message}',
                                filter=lambda r, h: r.extra['search'])
TestLog = logbook.FileHandler('/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/test.log',
                              format_string='[{record.time:%Y-%m-%dT%H:%M:%S}] {record.message}',
                              bubble=True)


SEARCH_LOG = '/Users/kristen/.pip/search.log'
INSTALL_LOG = '/Users/kristen/.pip/install.log'
UNINSTALL_LOG = '/Users/kristen/.pip/uninstall.log'
PIP_LOG = '/Users/kristen/.pip/pip.log'

install_logger = logbook.FileHandler(INSTALL_LOG, format_string='[{record.time:%Y-%m-%dT%H:%M:%S}] {record.message}',
                                     filter=lambda r, h: r.extra['install'])
search_logger = logbook.FileHandler(SEARCH_LOG, format_string='[{record.time:%Y-%m-%dT%H:%M:%S}] {record.message}',
                                    filter=lambda r, h: r.extra['search'])

pip_logger = logbook.FileHandler(PIP_LOG, format_string='[{record.time:%Y-%m-%dT%H:%M:%S}] {record.message}',
                                 bubble=True)

with SearchLog, TestLog:
	logbook.info('this is interesting', extra={'search': True})
	logbook.info('this is not interesting')

import sys, os

def search_test():
	with SearchLog, TestLog:
		logbook.info('this is interesting', extra={'search': True})
		logbook.info('this is not interesting')


if __name__ == '__main__': print(__file__)