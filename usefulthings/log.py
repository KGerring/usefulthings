#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = log
# author=AutisticScreeching
# date = 4/4/17
import sys, os
import logging
import posixpath

LEVELS = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}
logging_template = "[%(asctime)s] %(name)-15s %(levelname)-5s %(message)-5s %(filename)s:%(funcName)s (%(lineno)d)"


def logfile_exists(file=None, filename='logfile.log'):
	dirname = posixpath.dirname(__file__)
	logfile = posixpath.join(dirname, filename)
	if posixpath.exists(logfile):
		return logfile
	else:
		log_file = open(logfile, 'w')
		log_file.write('')
		log_file.close()
		return logfile

def configure_stream(level='WARNING', use_logfile=True, logfile=None, template=logging_template):
	"""Configure root logger using a standard stream handler.

	Args:
		level (string, optional): lowest level to log to the console

	Returns:
		logging.RootLogger: root logger instance with attached handler
	"""
	# get the root logger
	root_logger = logging.getLogger(__file__)
	# set the logger level to the same as will be used by the handler
	root_logger.setLevel(level)
	
	# customize formatter, align each column
	if not template:
		template = "[%(asctime)s] %(name)-25s %(levelname)-8s %(message)s"
	else:
		template = template
	formatter = logging.Formatter(template, datefmt='%x %l:%M %p')
	
	# add a basic STDERR handler to the logger
	console = logging.StreamHandler()
	console.setLevel(level)
	console.setFormatter(formatter)
	
	if use_logfile:
		if not logfile:
			logfile = logfile_exists()
		else:
			logfile = logfile
		filelog = logging.FileHandler(filename=logfile)
		filelog.setLevel(level)
		filelog.setFormatter(formatter)
		root_logger.addHandler(filelog)
	root_logger.addHandler(console)
	root_logger.handlers = root_logger.handlers[:2]
	return root_logger


if __name__ == '__main__': print(__file__)