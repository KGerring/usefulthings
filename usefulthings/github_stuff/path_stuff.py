#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = path_stuff
# author=AutisticScreeching
# date = 4/27/17
from __future__ import absolute_import
import sys, os, os.path,stat
import posix
from py._path.local import FSBase, LocalPath, map_as_list, copystat, copymode, Stat, PosixPath
from py._path.common import Visitor, PathBase, FNMatcher, Checkers, NeverRaised
from zipfile import is_zipfile as iszip
from stat import S_ISSOCK, S_ISLNK, S_ISFIFO, S_ISREG, S_ISBLK, S_ISCHR, S_ISDIR
from pathlib import Path
from os.path import abspath, normpath, isabs, exists, isdir, isfile, islink, dirname,basename
import grp
from datetime import datetime
from fnmatch import fnmatch
from py._path.local import LocalPath as _LocalPath
from py._path.common import PathBase as _PathBase
import re, regex
from os.path import isdir, isfile
from os import fdopen
from tempfile import gettempdir, _get_candidate_names, _candidate_tempdir_list
envs = 'TMPDIR', 'TEMP', 'TMP'
gist_include='https://gist.github.com'
collapse ='https://raw.githubusercontent.com/Mottie/GitHub-userscripts/master/github-collapse-markdown.user.js'
#els = $$(".markdown-body pre, .email-signature-reply"),
languages='https://github.com/github/linguist/blob/master/lib/linguist/languages.yml'
from send2trash import send2trash as remove
import tempfile
try:
	from startups import *
except ImportError:
	pass




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


logging_template = "[%(asctime)s] %(name)-15s %(levelname)-5s %(message)-5s %(filename)s:%(funcName)s (%(lineno)d)"
short_template = "[%(asctime)s] %(levelname)-5s %(message)-5s"
def configure_stream(level='WARNING', use_logfile=True, logfile=None, template=None):
	"""Configure root logger using a standard stream handler.

	Args:
		level (string, optional): lowest level to log to the console

	Returns:
		logging.RootLogger: root logger instance with attached handler
	"""
	# get the root logger
	import logging
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


def test_logger(log=None):
	if not log:
		log = configure_stream()
	print(log.name)
	log.debug('debug')
	log.info('info')
	log.warn('warn')
	log.error('error')
	log.critical('critical')


VERBOSE = True

if VERBOSE:
	logger = configure_stream(level='DEBUG', use_logfile=False, template=short_template)
else:
	logger = configure_stream(level='CRITICAL', use_logfile=False, template=short_template)

CORETYPES ='/System/Library/CoreServices/CoreTypes.bundle'
CORETYPES_INFO = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Info.plist'
MIME = ['/Users/kristen/dokuwiki/apache2/conf/mime.types',
		'/Users/kristen/anaconda/lib/python3.6/site-packages/scrapy/mime.types',
		'/usr/local/Cellar/erlang/19.3/lib/erlang/lib/inets-6.3.6/examples/server_root/conf/mime.types',
		'/usr/local/Cellar/erlang/19.3/lib/erlang/lib/percept-0.9/priv/server_root/conf/mime.types',
		'/usr/local/Cellar/go/1.8/libexec/misc/nacl/testdata/mime.types',
		'/usr/local/etc/apache2/2.4/mime.types',
		'/usr/local/Cellar/go/1.8.1/libexec/misc/nacl/testdata/mime.types',
		'/private/etc/apache2/mime.types',
		'/etc/apache2/mime.types']

#class visit(self, fil=None, rec=None, ignore=NeverRaised, bf=True, sort=True): pass

def get_symlink_dest(path): return posix.readlink(path)

def isfifo(file):
	return stat.S_ISFIFO(os.stat(file).st_mode)

def ispickle(file):
	with open(file, 'rb') as peeker:
		peeked = peeker.peek()
		return peeked[-1] == 46

def plist(file):
	import plistlib
	return plistlib.load(open(file, 'rb'))

FSNAME ='kMDItemFSName = "*.plist"c'

#com_apple_FileExtensionAttribute


from operator import methodcaller
from io import BytesIO, FileIO, IOBase, RawIOBase, StringIO, TextIOBase, TextIOWrapper


class Plist(object):
	from datetime import datetime
	DATETIME_FMT = '%Y-%m-%dT%H:%M:%S'
	TOTAL_SECONDS = '%s'
	sformat = methodcaller('strftime', format='%s')
	mode = 'b+'
	opener = os.open
	buffering = -1
	encoding = None
	errors = None
	closefd = True
	#root.docinfo.root_name
	
	



from py._path.local import LocalPath as _LocalPath

class PathEntry(_LocalPath):
	
	def abspath(self):
		return abspath(self)
	
	def as_abs(self):
		self.strpath = self.abspath(self)
		#self.basename
	
	@property
	def relpath(self):
		return self.relto(self)
		
	@staticmethod
	def _as_datetime(timestamp):
		try:
			return datetime.fromtimestamp(timestamp)
		except AttributeError:
			return datetime.datetime.fromtimestamp(timestamp)
			
	def get_time(self, attr = 'mtime', as_datetime=True):
		stat = self.stat()
		timestamp = getattr(stat, attr, None)
		if not timestamp: return None
		if as_datetime:
			return self._as_datetime(timestamp)
		return timestamp
	
	def mtime(self, as_datetime=True):
		return self.get_time(attr='mtime', as_datetime=as_datetime)
	
	def atime(self, as_datetime=True):
		return self.get_time(attr='atime', as_datetime=as_datetime)
	
	def ctime(self, as_datetime=True):
		return self.get_time(attr='ctime', as_datetime=as_datetime)
	
	def check(self, **kw):
		if not kw:
			return exists(self.strpath)
		if len(kw) == 1:
			if "dir" in kw:
				return not kw["dir"] ^ isdir(self.strpath)
			if "file" in kw:
				return not kw["file"] ^ isfile(self.strpath)
			if 'zip' in kw:
				return not kw['zip'] ^ iszip(self.strpath)
			
			if 'fifo' in kw:
				return not kw['fifo'] ^ stat.S_ISFIFO(self.stat().mode)
			if 'pickle' in kw:
				return not kw['pickle'] ^ ispickle(self.strpath)
		return super(PathEntry, self).check(**kw)
	
	def create(self, *args, **kwargs):
		p = self.join(*args)
		if not p.check(file=1):
			p.open('w').close()
		return p
	
	def remove(self, rec=0):
		if rec==0:
			if self.check(file=1, link=0):
				remove(str(self))
			elif self.check(link=1):
				os.unlink(str(self))
		elif rec == 1:
			for item in self.visit():
				if item.check(dir=0):
					remove(str(item))
				else:
					try:
						remove(str(item))
						
						
					except OSError:
						pass
					
					
			
	
	def match(self, pattern, *args):
		return bool(RegexMatcher(pattern)(self))

	def regexvisit(self, fil=None, rec=None, ignore=NeverRaised, bf=None, sort=None):
		for x in RegexVisitor(fil=fil, rec=rec, ignore=ignore, bf=bf, sort=sort).gen(self):
			yield x
			
	def relregexvisit(self, fil=None, rec=None, ignore=NeverRaised, bf=None, sort=None):
		for x in RegexVisitor(fil=fil, rec=rec, ignore=ignore, bf=bf, sort=sort).gen(self):
			yield x.relto(self)
			
	def __repr__(self):
		return '{}({!r})'.format(self.__class__.__name__, str(self))


class Opener(PathEntry):
	from configparser import RawConfigParser
	configparser = RawConfigParser
	plistlib = __import__('plistlib')
	
	def _open(self, *args, **kwargs): pass
	
	def open_plist(self):
		import plistlib
		return plistlib.load(self.open(mode='rb'))
	
	def open_ini(self):
		from configparser import RawConfigParser


parts ='dirname basename purebasename ext'.split()

class FNMatcher:
	def __init__(self, pattern):
		self.pattern = pattern
	
	def __call__(self, path):
		pattern = self.pattern
		if (pattern.find(path.sep) == -1 and
				iswin32 and
					pattern.find(posixpath.sep) != -1):
			# Running on Windows, the pattern has no Windows path separators,
			# and the pattern has one or more Posix path separators. Replace
			# the Posix path separators with the Windows path separator.
			pattern = pattern.replace(posixpath.sep, path.sep)
		if pattern.find(path.sep) == -1:
			name = path.basename
		else:
			name = str(path)  # path.strpath # XXX svn?
			if not os.path.isabs(pattern):
				pattern = '*' + path.sep + pattern
		return fnmatch.fnmatch(name, pattern)
	
class RegexMatcher(object):
	def __init__(self, pattern):
		self.pattern = pattern
		#logger.info('using pattern {!r}'.format(self.pattern))
		
	def __call__(self, path):
		#logger.info('checking path {!r}'.format(str(path)))
		pattern = self.pattern
		if not isinstance(path, (str, bytes)):
			if pattern.find(path.sep) == -1:
				name = path.basename
				#logger.info('name is {!r}'.format(str(name)))
			else:
				#name = str(path)
				name = path.basename
				#logger.info('name is {!r}'.format(str(name)))
		else:
			name = str(path)
			#logger.info('name is {!r}'.format(str(path)))
			#if not os.path.isabs(pattern):
				#pattern = '.*'+ path.sep + pattern
		name = path.basename
		found = re.search(pattern, name)
		#if found:
			#logger.info('found {!r} in {!r}'.format(found.group(0), name))
		return found
		
class RegexVisitor(object):
	def __init__(self, fil=None, rec=None,
				 ignore=NeverRaised, bf=None, sort=None, logger=None):
		if isinstance(fil,str):
			fil = RegexMatcher(fil)
		if isinstance(rec, str):
			self.rec = RegexMatcher(rec)
		
		elif not hasattr(rec, '__call__') and rec:
			self.rec = lambda path: True
		else:
			self.rec = rec
		self.fil = fil
		self.ignore = ignore
		self.breadthfirst = bf
		self.optsort = sort and sorted or (lambda x: x)
		
	def gen(self, path):
		try:
			entries = path.listdir()
		except self.ignore:
			return
		rec = self.rec
		dirs = self.optsort([p for p in entries
							 if p.check(dir=1) and (rec is None or rec(p))])
		
		if not self.breadthfirst:
			for subdir in dirs:
				#logger.info('recursing into directory {!r}'.format(subdir))
				for p in self.gen(subdir):
					yield p
		
		for p in self.optsort(entries):
			if self.fil is None or self.fil(p):
				yield p
		if self.breadthfirst:
			for subdir in dirs:
				#logger.info(subdir)
				for p in self.gen(subdir):
					yield p
		

class Visitor:
	def __init__(self, fil, rec, ignore, bf, sort):
		if isinstance(fil, py.builtin._basestring):
			fil = FNMatcher(fil)
		if isinstance(rec, py.builtin._basestring):
			self.rec = FNMatcher(rec)
		elif not hasattr(rec, '__call__') and rec:
			self.rec = lambda path: True
		else:
			self.rec = rec
		self.fil = fil
		self.ignore = ignore
		self.breadthfirst = bf
		self.optsort = sort and sorted or (lambda x: x)
	
	def gen(self, path):
		try:
			entries = path.listdir()
		except self.ignore:
			return
		rec = self.rec
		dirs = self.optsort([p for p in entries
							 if p.check(dir=1) and (rec is None or rec(p))])
		if not self.breadthfirst:
			for subdir in dirs:
				for p in self.gen(subdir):
					yield p
		for p in self.optsort(entries):
			if self.fil is None or self.fil(p):
				yield p
		if self.breadthfirst:
			for subdir in dirs:
				for p in self.gen(subdir):
					yield p

#/usr/local/bin/sift
#--line-number
#--filename
#--no-recursive, -R
#--regexp, -e
#--output-unixpath
#--output=FILE, -o
#--group
#--git
#--stats
#--column
#--context-after=NUM
#--context-before=NUM
#--conf=FILE

SIFT_CONFIG ='/Users/kristen/.sift.conf'
#sift [OPTIONS] [-e PATTERN | -f FILE]



KMD = dict(DATE_USED='kMDItemUsedDates',
		   D_DOWNLOADED='kMDItemUserDownloadedDate',
		   TAGS='kMDItemUserTags',
		   TEXT='kMDItemTextContent',
		   URL='kMDItemURL',
		   CHANGED='kMDItemFSContentChangeDate',
		   CREATED='kMDItemContentCreationDate',
		   MODIFIED='kMDItemContentModificationDate',
		   TYPE='kMDItemContentType',
		   ADDED='kMDItemDateAdded',
		   NAME='kMDItemDisplayName',
		   FOLDER='kMDItemDocumentContainer',
		   PLATFORM='kMDItemExecutablePlatform',
		   FS_MOD='kMDItemFSContentChangeDate',
		   FS_C='kMDItemFSCreationDate',
		   INVISIBLE='kMDItemFSInvisible',
		   EXT_HIDDEN='kMDItemFSIsExtensionHidden',
		   FILENAME='kMDItemFSName',
		   NODECOUNT='kMDItemFSNodeCount',
		   FS_GID='kMDItemFSOwnerGroupID',
		   FS_UID='kMDItemFSOwnerUserID',
		   FS_SIZE='kMDItemFSSize',
		   SIZE_LOGICAL='kMDItemLogicalSize',
		   SIZE_PHYSICAL='kMDItemLogicalSize',
		   FINDER_OPEN='kMDItemFinderOpenDate',
		   ITEM_ID='kMDItemIdentifier',
		   KIND='kMDItemKind',
		   LAST_USED='kMDItemLastUsedDate',
		   FULL_PATH='kMDItemPath',
		   SUPPORT_FILE='kMDItemSupportFileType')


if __name__ == '__main__':
	logger = configure_stream(level='DEBUG', use_logfile=False, template=short_template)
	pf = PathEntry('/Users/kristen/PycharmProjects/proj/mdls')
	#check=pf.regexvisit('($[a-z]+|\.rst$|\.py$|\.plist$|\.in$|[a-z,1]+.txt$)', rec='[a-z]+')
	cfg =PathEntry('/Users/kristen/PycharmProjects/proj/mdls/setup.cfg')
	mdls = PathEntry('/Users/kristen/PycharmProjects/proj/mdls/mdls', relpath=True)