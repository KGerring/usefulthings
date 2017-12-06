#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = mdls
# author=AutisticScreeching
# date = 3/21/17
import sys, os
import subprocess
import launchd
import regex, re
from subprocess import Popen, STDOUT, PIPE
import shlex

sort_options ="""
-n numerically; igmore blanks/tabs
-r reverse order
-f sort upper/lower together
-k n sort by key at position x
"""
COLORS = [['Red', '6'],
          ['Orange', '7'],
          ['Yellow', '5'],
          ['Green', '2'],
          ['Blue', '4'],
          ['Purple', '3'],
          ['Gray', '1']]


def listxattr(f, symlink=False):
	return tuple(xattr(f).list(options=symlink and XATTR_NOFOLLOW or 0))


def get_top_info():
	return "top -l 1 | head -8"

def find_tag(tag=''): return "mdfind 'tag:{}'".format(tag)

def test_examples(self):
	activejobs = [job for job in launchd.jobs() if job.pid is not None]
	inactivejobs = [job for job in launchd.jobs() if job.pid is None]
	errorjobs = [job for job in launchd.jobs() if job.laststatus != 0 and job.laststatus is not None]
	ondemandjobs = [job for job in launchd.jobs() if job.properties['OnDemand'] is True]

def process_open(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                 shell=True, cwd = '~', env=None, encoding='utf-8',
                 universal_newlines=True, close_fds=None,
                 preexec_fn = os.chdir('/')):  #'INI', #'GOOGLE_APPLICATION_CREDENTIALS'
	"""mdls -name kMDItemContentTypeTree -name kMDItemKind -name kMDItemLastUsedDate -raw ~/.config/.app.ini |xargs -0"""
	pass


def sh(s):
	"""Execute a terminal command in the shell"""
	subprocess.call([s], shell=True)

def cmd(s): return os.popen(s)._stream.read().splitlines()

def output(s):
	"""Execute a terminal command, and get the result back to you as a python object"""
	from subprocess import getoutput
	o = getoutput([s])
	return o

def get_handles(process, stdin, stdout, stderr):
	p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = proc._get_handles(stdin, stdout, stderr)


mail = subprocess.Popen(['mdfind', 'kMDItemKind="Mail message"cd'], stdout=-1, stderr=-1, universal_newlines=True)
wc = subprocess.Popen(["wc", '-l'], stdin=mail.stdout, stdout=-1, stderr=-1, universal_newlines=True)

EXECUTE_CHILD =('self',
                 'args',
                 'executable',
                 'preexec_fn',
                 'close_fds',
                 'pass_fds',
                 'cwd',
                 'env',
                 'startupinfo',
                 'creationflags',
                 'shell',
                 'p2cread',
                 'p2cwrite',
                 'c2pread',
                 'c2pwrite',
                 'errread',
                 'errwrite',
                 'restore_signals',
                 'start_new_session')

class NameTag(object):
	def __init__(self, name=''):
		self._basename = name
		if name == 'OwnerUserID':
			self.itemname = '_kMDItem'+ self._basename
		else:
			self.itemname = 'kMDItem' + self._basename
			
	def __repr__(self):
		return 'kMDItem{!r}'.format(self._basename)
		
mail_message = """mdfind 'kMDItemKind="Mail Message"cd'"""

find_pixel_each = """mdfind -0 "kMDItemFocalLength == '*'" | xargs -0 mdls | grep -E '(PixelHeight|DisplayName|PixelWidth)'"""

params = ['mdls']
attrs = ['kMDItemPath', 'kMDItemUserTags', 'kMDItemFSContentChangeDate', 'kMDItemContentModificationDate']
params.extend(['-plist', '-'])
params.append(obj)
cmm = subprocess.list2cmdline(params)
from plistlib import loads


LS = "mdls [-name attributeName] [-raw [-nullMarker markerString]] file"


PA = Popen(['mdfind',
            '-0',
            "kMDItemFocalLength == '*'"], stdout=-1, stderr=-1)
PB = Popen(['xargs',
            '-0',
            'mdls'], stdin=PA.stdout, stdout=-1, stderr=-1)
PC = Popen(['grep',
            '-E',
            '(PixelHeight|DisplayName|PixelWidth)'], stdin=PB.stdout, stdout=-1, stderr=-1)

remove_column = "ls -l $HOME | colrm  1 43"
grep_not = 'mdfind ipod | grep -v "Gmail" | grep -v "Automator" | grep "/kristen/" | wc -l'

NEVER_OPENED = "mdfind 'kMDItemLastUsedDate!=*' -onlyin ."
CONTENT_TYPE = "mdfind 'kMDItemContentType=*' -onlyin ."
WEBHISTORY="""mdfind kMDItemContentType="com.apple.safari.history" | grep -v youtube | grep -E '(process|pipe)' | uniq| sort"""
ANDAND = 'kMDItemContentType=*&&kMDItemFSName=*.ini'

pocoo = cmd("mdfind 'kMDItemURL=*pocoo*' -onlyin /Users/kristen/Library/Caches/Metadata/Safari/History")

yesterday = cmd("mdfind 'kMDItemFSCreationDate>$time.today(-1)'|uniq|sort")

m="""mdfind -onlyin "/Users/username/Documents/AAA/" "(  (kMDItemUserTags == 'Gray*'cdw) && (  (kMDItemDisplayName == '*$KMVAR_aa_f1*'c) || (kMDItemDisplayName == '*$KMVAR_aa_f2*'c)  )  )"""
SAVED ='/Users/kristen/Library/Saved Searches/copy_saved_search.savedSearch'
PS ='-AaCcEefhjlMmrSTvwXx'

cc ='ps -ax -E-f -j -l -v'

P = 'ps -o command|lstart|msgrcv|msgsnd|pri|pid|ppid|start|stat|time'
PP = 'ps -ax -o pid -o ppid -o stat=STATE -o time -o etime -o args=CMD'
PP_HEADERS='PID  PPID STATE  ELAPSED CMD'
import io, _io
#['mdfind',
#'(InRange(kMDItemFSCreationDate,$time.today(-14d),$time.today(+1d)) && (kMDItemContentTypeTree = public.content) && InRange(kMDItemContentModificationDate,$time.this_week,$time.this_week(+1)))']
#--xattr, --user --url -X GET , -O, --remote-name --output FILE
#--netrc --netrc-file --head
#--dump-header FILE
# --data DATA ,--data-urlencode DATA
#--config FILE
#--basic












CALLERS = ['mdfind kMDItemContentType=com.apple.safari.history',
           'grep -v youtube',
           'grep -E (process|pipe)',
           'uniq',
           'sort']
proc0 = Popen(shlex.split(CALLERS[0]), universal_newlines=True, stdout=-1, stderr=-1)
proc1 = Popen(shlex.split(CALLERS[1]), universal_newlines=True, stdin=proc0.stdout, stdout=-1)

proc2 = Popen(args=['grep', '-E', '(process|pipe)'], universal_newlines = True,  stdin=proc1.stdout, stdout= -1)
proc3 = Popen(shlex.split(CALLERS[3]), universal_newlines=True, stdin=proc2.stdout, stdout=-1)
proc4 = Popen(shlex.split(CALLERS[4]), universal_newlines=True, stdin=proc3.stdout, stdout=-1)


def info(obj):
	result, err= Popen(['info', obj], universal_newlines=True,
	              stdout=-1, shell=0).communicate()
	if isinstance(result, bytes):
		result = result.decode()
	print(result)
	return result


class SubProcess(object):
	UNIVERSAL_NEWLINES = True
	_PREEXEC_FN = None
	STDOUT = -1
	STDERR = -1
	
	def __init__(self, stdin_from=None, stdout_to = None,
	             stderr_to = None, *args, **kwargs):
		if stdin_from and isinstance(stdin_from (subprocess.Popen, SubProcess)):
			self.stdin = stdin_from
		if stdout_to:
			self.stdout = -1 #todo fix
			
		else:
			for k,v in kwargs.items():
				setattr(self, k,v)
	
		
			
		
		
	


PS_O = ['%cpu',
        '%mem',
        'acflag',
        'acflg',
        'args',
        'blocked',
        'caught',
        'comm',
        'command',
        'cpu',
        'cputime',
        'etime',
        'f',
        'flags',
        'gid',
        'group',
        'ignored',
        'inblk',
        'inblock',
        'jobc',
        'ktrace',
        'ktracep',
        'lim',
        'login',
        'logname',
        'lstart',
        'majflt',
        'minflt',
        'msgrcv',
        'msgsnd',
        'ni',
        'nice',
        'nivcsw',
        'nsignals',
        'nsigs',
        'nswap',
        'nvcsw',
        'nwchan',
        'oublk',
        'oublock',
        'p_ru',
        'paddr',
        'pagein',
        'pcpu',
        'pending',
        'pgid',
        'pid',
        'pmem',
        'ppid',
        'pri',
        'pstime',
        'putime',
        're',
        'rgid',
        'rgroup',
        'rss',
        'ruid',
        'ruser',
        'sess',
        'sig',
        'sigmask',
        'sl',
        'start',
        'stat',
        'state',
        'stime',
        'svgid',
        'svuid',
        'tdev',
        'time',
        'tpgid',
        'tsess',
        'tsiz',
        'tt',
        'tty',
        'ucomm',
        'uid',
        'upr',
        'user',
        'usrpri',
        'utime',
        'vsize',
        'vsz',
        'wchan',
        'wq',
        'wqb',
        'wql',
        'wqr',
        'xstat']

if __name__ == '__main__': print(__file__)