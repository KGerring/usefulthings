#!/usr/bin/env
# -*- coding: utf-8 -*-
# author=AutisticScreeching
# date = 3/4/17

import sys, os
import ast, _ast
from astunparse import unparse
import re, regex
#from kgerringrc import *
from tempfile import NamedTemporaryFile
from shutil import copyfile, move
from guidata import qapplication
from guidata.dataset.dataitems import FilesOpenItem
from guidata.dataset.datatypes import DataSet
import click

RE_KRISTEN = re.compile(r'(\S+)/Kristen(?P<rem>[^,]+)?')
RE_PYCHARM_PROJECTS = re.compile('/Applications/PycharmProjects1(?P<rem>[^,]+)?')
RE_CREATION_DATE = r'#\s*?date\s*?=\s*?(\d+)//(\d+)//(\d+)\s*'

RE_SEARCH_PATHS =re.compile('((?:SEARCH_PATHS)\s*?=\s*?\[(?P<line>[^,\]]+,?\s*)*\])') #TESTED
RE_REMOVE_OSGETLOG = regex.compile("(if\s*os\.getlogin\(\)\s*==\s*'Kristen'+:\s*(.+)pass)", re.S) #TESTED



@click.command()
@click.option('--file', help='The Text you want')
def fix_remove_osgetlog(file):
	with open(file) as reader:
		text = reader.read()
	RE_REMOVE_OSGETLOG = regex.compile("(if\s*os\.getlogin\(\)\s*==\s*'Kristen'+:\s*(.+)pass)", re.S)  # TESTED
	subbed = RE_REMOVE_OSGETLOG.sub('', text)
	subbed = RE_SEARCH_PATHS.sub('', subbed)
	click.echo(subbed)



def fix_pycharm_projects(text):
	#return RE_PYCHARM_PROJECTS.sub("/Users/kristen/PycharmProjects\g<rem>", text)
	return text.replace('PycharmProjects1', 'PycharmProjects').replace(
		'/Applications/PycharmProjects', '/Users/kristen/PycharmProjects')


def fix_kristen(text):
	return RE_KRISTEN.sub('\g<1>/kristen\g<rem>', text)


def fix_text(text):
	if not text:
		pass
	else: return fix_kristen(fix_pycharm_projects(text))
	

def parse_sourcefile(source_or_file):
	if os.path.exists(source_or_file):
		source = open(source_or_file).read()
	elif isinstance(source_or_file, (str, bytes)):
			source = source_or_file
	else:
		source = source_or_file[:]
	try:
		parsed = ast.parse(source)
		return parsed
	except (SyntaxError, AttributeError):
		print("Problem with {!r}".format(source_or_file))
		return None

def fix_search_paths(parsed):
	keep = []
	if not parsed: return None
	else:
		
		for item in parsed.body:
			if isinstance(item, _ast.If) and 'os.getlogin' in unparse(item.test).strip():
				pass
			
			elif isinstance(item, _ast.Assign) and 'SEARCH_PATHS' in unparse(item.targets).strip():
					pass
			
			else:
				keep.append(item)
		
		return unparse(keep)

def fix(file):
	ast_parsed = parse_sourcefile(file)
	if ast_parsed is None:
		return None
	else:
		fixed = fix_search_paths(ast_parsed)
		all_fixed = fix_text(fixed)
		return all_fixed

def overwrite(path):
	if not path: return "Problem!"
	else:
		fixed_file = fix(path)
		print(path)
		with open(path, 'w') as writer:
			writer.write(fixed_file)
			print('DONE!')

def safe_overwrite(path, temporary=None):
	if temporary is None:
		temporary = expand('~/temporary_file')
	else:
		temporary = temporary
	fixed_file = fix(path)
	#binary_fixed = encode(fixed_file)
	#temp.write(binary_fixed)
	with open(temporary, 'w') as writer: writer.write(fixed_file)
	
	print('tempfile written')
	base, ext = os.path.splitext(path)
	if ext is not None:
		new_name = base+'.bak'
		move(path, new_name)
	else:
		move(path, join(path, '.bak'))
		
	copyfile(temporary, path)
	
	return path

SCRIPT = """choose file with prompt "Choose file to convert:" default location "Macintosh HD:Users:kristen:PycharmProjects" as alias invisibles true multiple selections allowed true"""


class MyFilePicker(DataSet):
	files = FilesOpenItem(label='choose files', basedir='/Users/kristen/PycharmProjects')
	
def do_app(): #todo remove
	app = qapplication()
	mydialog = MyFilePicker()
	if mydialog.edit():
		print(mydialog.to_string())
		mydialog.view()
	return mydialog.files

def iterate_files(safe=False):
	files = do_app()
	for file in files:
		if safe:
			fixed = safe_overwrite(file)
			print(fixed)
		else:
			fixed = overwrite(file)
			print(fixed)

######

#TODO 'find . -exec tag --add tagname file {} \;  -print '

if __name__ == '__main__':
	#files = do_app()
	#FILE = '/Users/kristen/PycharmProjects/Important_Things/usefulthings/aws_stuff.py'
	#print(open(FILE).read())
	#print('\x1b[35m{}\x1b[0m:'.format('#'*40))
	#test_aws = fix(FILE)
	#print(test_aws)
	#safe_overwrite(FILE)
	#FILES = iterate_files(safe=False)
	fix_remove_osgetlog()



	
	
	
		







