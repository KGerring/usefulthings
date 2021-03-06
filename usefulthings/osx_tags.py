#!/usr/bin/env
# -*- coding: utf-8 -*-
# author=KGerring
# date = 3/4/17
import sys, os
from shutil import which
import subprocess



BLUE = '\x1b[34m{}\x1b[0m'
WARNING = '\x1b[4m\x1b[31m{}\x1b[0m'


class Tag(object):
	def __init__(self, tag):
		self.tag = tag
		self.comparable_name = self.tag.lower()
	
	@property
	def visible_name(self):
		return self.tag
	
	def __eq__(self, other):
		return other.comparable_name == self.comparable_name
	
	def __hash__(self):
		return self.comparable_name.__hash__()
	

OP = "s:a:r:m:f:l".split()
op = 'set add remove match find list'.split()

def tags_contains(s):
	return '(kMDItemUserTags = {!r}cd)'.format('*'+s+'*')

def tags_not(s):
	if s == '*':
		s = re.escape('*')
	return '(kMDItemUserTags != {!r}cd)'.format(s)

def tags_matches(s):
	return '(kMDItemUserTags = {!r}cdw)'.format(s + '*')

def tags_is(s):
	return '(kMDItemUserTags = {!r}cd)'.format(s)

ii = '({})'.format(' && '.join(map(tags_is, ['todo', 'Important'])))




FIND = '((kMDItemUserTags != "\\*"cd) && (kMDItemUserTags = "todo*"cdw) && (kMDItemUserTags = "*impo*"cd))'


class Tagger(object):
	MINLEN = 31
	startingSepator = "\t"
	tagseps = (",", "    ")
	WILDCARD = "*"
	
	OPTS = "s:a:r:m:f:lAeRdnNtTgG0hv"
	def __init__(self, *args, **kwargs):
		self.operationMode = '--list'
		self.displayAllFiles = False
		self.recurseDirectories = False
		self.enterDirectories = False
		self.searchScope = None
		self.outputFlags = 0
		self.nulTerminate = False
		self.name_flag = 0
		self.tags_flag = 0
		self.garrulous_flag = 0
		self.tags = None
		self.urls = None
	
	def change_options(self, opts):
		"""
		tagsOnSeparateLines = (outputFlags & OutputFlagsGarrulous)
		printTags = (outputFlags & OutputFlagsTags)
		
		
		
		:param opts:
		:return:
		"""
		if 'A' in opts:
			self.displayAllFiles = True
		if 'e' in opts:
			self.enterDirectories = True
		if 'R' or 'd' in opts:
			self.recurseDirectories = True
		if 'n' in opts:
			self.name_flag = 2
		if 'N' in opts:
			self.name_flag = 1
		if 't' in opts:
			self.tags_flag = 2
		if 'T' in opts:
			self.tags_flag = 1
		if 'g' in opts:
			self.garrulous_flag = 2
		if 'G' in opts:
			self.garrulous_flag = 1
		
		if '--home' in opts:
			self.searchScope = '--home'
		
		if '--local' in opts:
			self.searchScope = '--local'
		if '--network' in opts:
			self.searchScope = '--network'
		if '0' in opts:
			self.nulTerminate = True
			
	def do_action(self, tags=[], urls = []):
		self.tags
		self.urls = urls

	def doAdd(self, urls=None, tags=[]):
		"""
		--all, --enter, and --recursive apply
		
		(tags.existing | tags.new)
		
		:param urls:
		:param tags:
		:return:
		"""
		if not urls: return
		pass
	
	def doRemove(self, tags, urls):
		"""
		matchAny = self.wildcard
		
		set (minusSet:self.tags)
		:param tags:
		:param urls:
		:return:
		"""
	
	def doMatch(self, tags, urls, any=True, none=False):
		"""
		matchAny = "*"
		matchNone = ""
		
		if matchAny && tagCount > 0 or (matchNone && tagCount == 0) or self.tags isSubsetOfSet:
		print
		
		
		
		:param tags:
		:param urls:
		:param any:
		:param none:
		:return:
		"""
		pass
	
	def doFind(self):
		"""
		kMDItemUserTags = '*"
		
		:return:
		"""
		pass
	
	def mdls(self):
		"""
		kMDItemPath
		
		:return:
		"""
		
		
#o = output("tag --match '*' --tags -G --enter *")



OPTIONS = """-v   --version      Display version
-h   --help         Display this help
-A   --all          Display invisible files while enumerating
-e   --enter        Enter/enumerate directories provided
-d   --descend      Recursively descend into directories
-n   --name         Turn on filename display in output (default)
-N   --no-name      Turn off filename display in output (list, find, match)
-t   --tags         Turn on tags display in output (find, match)
-T   --no-tags      Turn off tags display in output ((list))
-G   --no-garrulous Display tags comma-separated after filename (default)
-g   --garrulous    Display tags each on own line (list, find, match)
-H   --home         Find tagged files in user home directory
-L   --local        Find tagged files in home + local filesystems
-R   --network      Find tagged files in home + local + network filesystems
-0   --nul          Terminate lines with NUL ( ) for use with xargs -0
"""
ACTIONS = """tag -a   --add <tags> <path>...        Add tags to file
tag -r   --remove <tags> <path>...     Remove tags from file
tag -s   --set <tags> <path>...        Set tags on file
tag -m   --match <tags> <path>...      Display files with matching tags
tag -l   --list <path>...              List the tags on file
tag -f   --find <tags> <path>...       Find all files with tags, limited to paths if present



++++++++

 -a , --add <tags> <path>...     Add tags to file
 -r , --remove <tags> <path>...  Remove tags from file
 -s , --set <tags> <path>...     Set tags on file
 -m , --match <tags> <path>...   Display files with matching tags
 -l , --list <path>...           List the tags on file
 -f , --find <tags> <path>...    Find all files with tags (-A, -e, -R ignored)
 
-v , --version      ,Display version
-h , --help         ,Display this help
-A , --all          ,Display invisible files while enumerating
-e , --enter        ,Enter and enumerate directories provided
-R , --recursive    ,Recursively process directories
-n , --name         ,Turn on filename display in output (default)
-N , --no-name      ,Turn off filename display in output (list, find, match)
-t , --tags         ,Turn on tags display in output (find, match)
-T , --no-tags      ,Turn off tags display in output (list)
-g , --garrulous    ,Display tags each on own line (list, find, match)
-G , --no-garrulous ,Display tags comma-separated after filename (default)
-H , --home         ,Find tagged files in user home directory
-L , --local        ,Find tagged files in home + local filesystems
-R , --network      ,Find tagged files in home + local + network filesystems
-0 , --nul          ,Terminate lines with NUL (\0) for use with xargs -0

"""
tags = [['-v', '--version', 'Display version'],
        ['-h', '--help', 'Display this help'],
        ['-A', '--all', 'Display invisible files while enumerating'],
        ['-e', '--enter', 'Enter and enumerate directories provided'],
        ['-R', '--recursive', 'Recursively process directories'],
        ['-n', '--name', 'Turn on filename display in output (default)'],
        ['-N', '--no-name', 'Turn off filename display in output (list', 'find', 'match)'],
        ['-t', '--tags', 'Turn on tags display in output (find', 'match)'],
        ['-T', '--no-tags', 'Turn off tags display in output (list)'],
        ['-g', '--garrulous', 'Display tags each on own line (list', 'find', 'match)'],
        ['-G', '--no-garrulous', 'Display tags comma-separated after filename (default)'],
        ['-H', '--home', 'Find tagged files in user home directory'],
        ['-L', '--local', 'Find tagged files in home + local filesystems'],
        ['-R', '--network', 'Find tagged files in home + local + network filesystems'],
        ['-0', '--nul', 'Terminate lines with NUL (\x00) for use with xargs -0']]

#todo tag --no-name * to list in . but not show files
#--garrulous
"""        -g | --garrulous    Display tags each on own line (list, find, match)
        -G | --no-garrulous Display tags comma-separated after filename (default)
        -0 | --nul          Terminate lines with NUL (\0) for use with xargs -0

"""

def verify_tags(tags=None):
	if isinstance(tags, (list, tuple)):
		tags = ','.join([tag.strip() for tag in tags])
	elif (isinstance(tags, str) and ',' in tags):
		tags = ','.join([tagname.strip() for tagname in tags.split(',')])
	else:
		tags = tags
	return tags


def verify_filelist(files=None):
	if isinstance(files, (list, tuple)):
		files = ' '.join([tag.strip() for tag in files])
	elif (isinstance(files, str) and files.contains(',')):
		files = ' '.join([tagname.strip() for tagname in files.split(',')])
	else:
		files = files
	return files


def add_tags(tags=None, files=None, options=None):
	tags = verify_tags(tags=tags)
	files = verify_filelist(files=files)
	command = 'tag --add {tags} {files}'.format(tags=tags, files=files)
	return command


def remove_tags(tags=None, files=None, options=None):
	"""Remove specific tags from a file(s). Tags not named will remain"""
	tags = verify_tags(tags=tags)
	files = verify_filelist(files=files)
	template = 'tag --remove {tags} {files}'
	return template.format(tags=tags, files=files)


def remove_all_tags(files=None, options=None):
	"""Remove ALL tag associations from the file(s)"""
	files = verify_filelist(files=files)
	template = 'tag --remove \\* {files}'
	return template.format(files=files)


def replace_tags(tags=None, files=None):
	"THIS DOESN'T ADD TO IT. IT REPLACES"
	tags = verify_tags(tags=tags)
	files = verify_filelist(files=files)
	command = 'tag --set {tags} {files}'.format(tags=tags, files=files)
	return command


def match_all_tagged(files=None, options=None, recursive=False):
	if ((not files) or (options is not None)):
		if (not recursive):
			return "tag --match '*' --tags *"
		else:
			return "tag --match '*' --descend ."
	else:
		files = verify_filelist(files=files)
		return "tag --match '*' --tags {files}".format(files=files)


def match_all_untagged(files=None, options=None, recursive=False):
	if ((not files) or (options is not None)):
		if (not recursive):
			return "tag --match '' *"
		else:
			return "tag --match '' --descend ." #todo --recursive but --enter to enter
	else:
		files = verify_filelist(files=files)
		return "tag --match '' {files}".format(files=files)


def list_all_tags_in_cwd(recursive=False):
	if recursive:
		return 'tag --list --descend .'
	else:
		return 'tag'


def find_all_files_with_tags():
	return "tag --find '*'"


def find_all_files_with_no_tags():
	return "tag --find ''"


def find_tags(tags=None, files=None, options=None):
	"""options can be '--home', '--local', or '--network'
	for home directory, local disk, or network, respectively"""
	tags = verify_tags(tags=tags)
	if ((not files) and (options is not None)):
		return 'tag --find {tags} {options}'.format(tags=tags, options=options)
	elif (files and (options is not None)):
		files = verify_filelist(files=files)
		return 'tag --find {tags} {options} {files}'.format(tags=tags, options=options, files=files)
	else:
		files = verify_filelist(files=files)
		return 'tag --find {tags} {files}'.format(tags=tags, files=options)


def recursive_tagging(tags=None, path='.'):
	tags = verify_tags(tags=tags)
	return 'tag -e -d --add {tags} {path}'.format(tags=tags, path=path)


def tag_stats():
	from collections import Counter
	from kgerringrc import cmd
	command = "tag --find '*' --tags --no-name --garrulous"
	print(repr(command))
	alltags = cmd(command)
	cnt = Counter(alltags)
	unique = sorted(list(set(alltags)))
	return (cnt, unique)


def master_list():
	from kgerringrc import cmd
	rows = cmd("tag --find '*' --tags")
	lines = [row.split('\t') for row in rows]
	entries = [(file.strip(), set(tags.strip().split(','))) for (file, tags) in lines]
	return entries


def recursively_tag_with_tag(directory='.'): #todo
	"""http://apple.stackexchange.com/questions/106654/how-can-i-apply-tags-in-mavericks-recursively
	You can leave the `-type f` argument off if you want to tag the subdirectories as well as the files.
	Finally, you can change the `find yourDirName -type f` to   `find yourDirName -iname "*.ext"`
	if you want to only tag certain file types/extensions."""
	directory = directory
	make_file = 'touch -c samplefile'
	open_file = 'open .'
	FinderInfo = 'find yourDirName -type f | xargs xattr -wx com.apple.FinderInfo "`xattr -px sampleFile`"'
	UserTags = 'find yourDirName -type f | xargs xattr -wx com.apple.metadata:_kMDItemUserTags "`xattr -px com.apple.metadata:_kMDItemUserTags sampleFile`"'

def recurse_tag(tags= '', directory = '.', ext='.py'):
	"""return sh('find . -exec tag --add tagname file {} \;  -print ')
	noset_ITERATE_TAGS ='find . -exec tag --add tagname file {} \;  -print '"""
	noset_ITERATE_TAGS = 'find . -exec tag --add tagname file {} \;  -print '
	from startups.core import output
	tags = verify_tags(tags=tags)
	from pathlib import Path
	if os.path.exists(directory):
		p = Path(directory)
		glob = p.rglob('[!_][!_]*[!_][!_].py')
	#.absolute().as_posix()
	TEMPLATE = 'tag --add {tags} {file}'
	for pth in p.rglob('[!_][!_]*[!_][!_].py'): #todo fix
		if pth.absolute().exists():
			file = pth.absolute().as_posix()
			print(output(TEMPLATE.format(tags=tags, file=file)))
			
			
			

	
	