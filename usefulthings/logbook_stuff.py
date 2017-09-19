#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = logbook_stuff
# author=AutisticScreeching
# date = 3/15/17
import sys, os
import logbook

from logbook.queues import MultiProcessingHandler
from multiprocessing import Queue
from logbook.base import LogRecord, dispatch_record, _create_log_record, _convert_frame_filename, _ExceptionCatcher, \
	StackedObject
from logbook.handlers import FileHandler, TestHandler, StringFormatter, SYSLOG_PORT, Handler
import regex, re


INFO = frozenset({'exception_message',
                  'exception_name',
                  'filename',
                  'formatted_exception',
                  'func_name',
                  'greenlet',
                  'lineno',
                  'message',
                  'module',
                  'process_name',
                  'thread',
                  'thread_name'})


FS = '[{record.time:%Y-%m-%dT%H:%M:%S}] {record.func_name}({record.lineno})|{record.message}'
F = r'\[(?P<time>.+?)\]\s*?(?P<func_name>.+?)\((?P<lineno>.+?)\)\|(?P<message>.+?)\n'

frame_correction = 0
extra = None
exc_info = True
#channel = self

#level, args[0], args[1:], kwargs,exc_info, extra, frame_correction)
#record = LogRecord(self.name, level, msg, args, kwargs, exc_info, extra, None, channel, frame_correction)


#stack_manager
ISO = re.compile('(\\d{4})(?:-?(\\d{2})(?:-?(\\d{2}))?)?(?:T(\\d{2}):(\\d{2})(?::(\\d{2}(?:\\.\\d+)?))?(Z|[+-]\\d{2}:\\d{2})?)?$')


class RecordHandler(TestHandler):
	encoding = 'utf-8'
	_filename = "filename"
	
	
	def get_record(self, n=-1):
		if self.records:
			return self.records[n]
		else:
			return None
	





#dt =_datetime_factory()
#frame = sys._getframe(1)


def emit(self, record):
	# keep records open because we will want to examine them after the
	# call to the emit function.  If we don't do that, the traceback
	# attribute and other things will already be removed.
	record.keep_open = True
	if self._force_heavy_init:
		record.heavy_init()
	self.records.append(record)

#_formatted_record_cache

#exc_info =(exc_type, exc_value, tb)







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