#!/usr/bin/env
# -*- coding: utf-8 -*-
# author=KGerring
# date = 3/4/17
import sys, os

BLUE = '\x1b[34m{}\x1b[0m'
WARNING = '\x1b[4m\x1b[31m{}\x1b[0m'



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
"""

#todo tag --no-name * to list in . but not show files
#--garrulous
 

def verify_tags(tags=None):
	if isinstance(tags, (list, tuple)):
		tags = ','.join([tag.strip() for tag in tags])
	elif (isinstance(tags, str) and tags.contains(',')):
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

def recurse_tag(tags= '', directory = '.'):
	"""return sh('find . -exec tag --add tagname file {} \;  -print ')"""
	pass