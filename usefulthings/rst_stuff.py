#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = rst_stuff
# author=AutisticScreeching
# date = 5/8/17
import sys, os
__path__ = os.path.dirname(__file__)

from requests import get
from pyfetcher.xpathlexer import XPathExpr, JQueryTranslator, get_node_text, render_html, fromstring, make_tree, prepare_url as _prepare_url
from pyquery.cssselectpatch import JQueryTranslator
from pathlib import Path
from string import Formatter
import tabulate
import _string
import parse
from functools import partial
TABLE_FORMATS = 'simple,plain,grid,fancy_grid,pipe,orgtbl,jira,psql,rst,mediawiki,moinmoin,html,latex,latex_booktabs,tsv,textile'.split(',')
PATH = Path(__path__)

BASE_HTML =     'http://docutils.sf.net/docs/ref/rst/'
QUICKREF =      'http://docutils.sourceforge.net/docs/user/rst/quickref.html'
CHEATSHEET =    'http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt'
DIRECTIVES =    'http://docutils.sf.net/docs/ref/rst/directives.html'
ROLES =         'http://docutils.sf.net/docs/ref/rst/roles.html'
RST =           'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html'
INTRODUCTION =  'http://docutils.sf.net/rst.html'

prepare_rst = partial(_prepare_url, url='http://docutils.sf.net/docs/ref/rst/')
prepare_user = partial(_prepare_url, url='http://docutils.sourceforge.net/docs/user/rst/')
prepare_net = partial(_prepare_url, url='http://docutils.sf.net')
SPHINX = '/Users/kristen/anaconda/lib/python3.6/site-packages/sphinx'
EXTENSIONS = ('autodoc', 'doctest', 'intersphinx', 'todo', 'coverage',
              'imgmath', 'mathjax', 'ifconfig', 'viewcode', 'githubpages')

from sphinx.util.osutil import make_filename

parts = ['/Users/kristen/anaconda/bin/python3.6',
         '/Applications/PyCharm.app/Contents/helpers/rest_runners/rst2smth.py',
         'rst2html',
         '/Users/kristen/PycharmProjects/proj/usefulthings/usefulthings/rst_information.rst',
         '/Users/kristen/PycharmProjects/proj/usefulthings/usefulthings/rst_information.html']


def publish_cmdline(reader=None, reader_name='standalone',
                    parser=None, parser_name='restructuredtext',
                    writer=None, writer_name='html',
                    settings=None, settings_spec=None,
                    settings_overrides=None, config_section=None,
                    enable_exit_status=True, argv=None,
                    usage='', description=''):
	pub = Publisher(reader, parser, writer, settings=None)
	pub.set_components(reader_name, parser_name, writer_name)
	output = pub.publish(
			argv, usage, description,
			config_section=None, enable_exit_status=True)
	return output


formatter = Formatter()

#self = self.vformat(format_string, args, kwargs)
to_r = formatter.convert_field(value='3', conversion='r')
formatter.format_field(value=+43000, format_spec='> 4,.0F')


ALLOWED_TYPES = parse.ALLOWED_TYPES


def print_types():
	results = dict()
	for TYPE in ALLOWED_TYPES:
		expression = '{:' + TYPE + '}'
		results[TYPE]=parse.compile(expression)._expression
	return results
		
	
extract='[[fill]align][0][width][.precision][type]'
e = parse.extract_format('3>03.2e', None)
n= parse.extract_format('x^03.2n', '')


class Format(object):
	ALIGN_RE = re.compile('<|>|=|^')
	FILL_RE = '[^}{]'
	SIGN_RE = '+|-|\\s'
	WIDTH_RE = '\d+'
	grouping ='[_,]{0,1}'
	TYPE ='[bcdeEfFgGnosxX%]{1}'
	format_spec = '[[fill]align][sign][#][0][width][,][.precision][type]'
	FORMAT_SPEC = '[[fill]align][sign][#][0][width][grouping_option][.precision][type]'
	__align = ['<', '>', '=', '^']
	__sign = ['+', '-', ' ']
	__grouping_option = ['_', ',']
	__type = ['b', 'c', 'd', 'e', 'E', 'f', 'F', 'g', 'G', 'n', 'o', 's', 'x', 'X', '%']
	
	def __init__(self, type='s'):
		self._type = type
		print('The _hash option is only valid for integers, and only for binary, octal, or hexadecimal output')
	



COMPATIBLE_FORMATS = dict(int={'{:c}', '{:b}', '{:f}', '{:o}', '{:e}', '{:n}', '{:x}', '{:g}', '{:d}'})

floatfmt = floatfmt = {'%', 'e', 'f', 'g', 'n', 'E', 'F', 'G'}
hash_int = {'#b', '#o', '#x', '#X'}
intfmt = floatfmt  |{'b', 'c', 'd', 'o', 'x', 'X'}
_int = intfmt | hash_int



formatter.parse('_{0!r:s}').__next__()

def _vformat(self, format_string, args, kwargs, used_args, recursion_depth=2, auto_arg_index=0):
	if recursion_depth < 0:
		raise ValueError('Max string recursion exceeded')
	result = []
	for literal_text, field_name, format_spec, conversion in self.parse(format_string):
		# output the literal text
		if literal_text:
			result.append(literal_text)
		# if there's a field, output it
		if field_name is not None:
			# this is some markup, find the object and do
			#  the formatting
			# handle arg indexing when empty field_names are given.
			if field_name == '':
				if auto_arg_index is False:
					raise ValueError('cannot switch from manual field '
					                 'specification to automatic field '
					                 'numbering')
				field_name = str(auto_arg_index)
				auto_arg_index += 1
			elif field_name.isdigit():
				if auto_arg_index:
					raise ValueError('cannot switch from manual field '
					                 'specification to automatic field '
					                 'numbering')
				# disable auto arg incrementing, if it gets
				# used later on, then an exception will be raised
				auto_arg_index = False
			# given the field_name, find the object it references
			#  and the argument it came from
			obj, arg_used = self.get_field(field_name, args, kwargs)
			used_args.add(arg_used)
			# do any conversion on the resulting object
			obj = self.convert_field(obj, conversion)
			# expand the format spec, if needed
			format_spec, auto_arg_index = self._vformat(
					format_spec, args, kwargs,
					used_args, recursion_depth - 1,
					auto_arg_index=auto_arg_index)
			# format the object and append to the result
			result.append(self.format_field(obj, format_spec))
	return ''.join(result), auto_arg_index


SET = set('abcdefghijklmnopqrstuvwxyz')
def check_format(s):
	keep = set([])
	old = list('abcdefghijklmnopqrstuvwxyz')
	
	for fmt in old:
		try:
			s.__format__(fmt)
			keep.add(fmt)
		except ValueError:
			pass
	return keep
		



def display_func(s: str, args) -> str:
	print(repr(s))
	print('.format')
	print(args)
	print('=')
	res = s.format(args)
	print(res)


def check_type(func, arg_name, arg_type, arg_value):
	if (not isinstance(arg_value, arg_type)):
		raise ValueError(
			'{func}: wrong type of {arg!r} argument, {exp!r} expected, got {got!r}'.format(func=func.__qualname__,
			                                                                               arg=arg_name,
			                                                                               exp=arg_type.__name__,
			                                                                               got=type(
				                                                                               arg_value).__name__))


FORMAT_SPEC ='[[fill]align][sign][#][0][width][grouping_option][.precision][type]'
align = ['<', '>', '=', '^']
sign= ['+', '-', ' ']
grouping_option = ['_',',']

_type = ['b', 'c', 'd', 'e', 'E', 'f', 'F', 'g', 'G', 'n', 'o', 's', 'x', 'X', '%']

A = '{:<14}'
ALIGN ='<'
FILL = ' '

print('{:>30}', '{:>30}'.format('right aligned'))



E = '{fill}{align}{sign}{width}{grouping}{precision}{type}'.format(fill=' ', align='^', sign='+', width=3, grouping='_',
                                                                   precision='.0', type='E')

char_type ='{0:c}'
int_type = '{0:#d}'
hex_type = '{0:#x}'
oct_type = '{0:#o}'
bin_type = '{0:#b}'
ff= formatter.format_field(42000.0, '=-10_.1E')

yesno_mapping = {
	"yes":  True, "no": False,
	"on":   True, "off": False,
	"true": True, "false": False,
}
@parse.with_pattern(r"|".join(yesno_mapping))
def parse_yesno(text):
	return yesno_mapping[text.lower()]


@parse.with_pattern(r"\d+")
def parse_number(text): return int(text)

format_string_syntax ='http://docs.python.org/library/string.html#format-string-syntax'
specification = 'http://docs.python.org/library/string.html#format-specification-mini-language'

rst = partial(_prepare_url, url='http://docutils.sourceforge.net/docs/user/rst')

padleft = tabulate._padleft
padright = tabulate._padright
padboth = tabulate._padboth


def make_tree(url):
	text = get(url).content
	return fromstring(text)


def make_table(data, headers=(), tablefmt='grid', floatfmt='g', missingval="", numalign = 'decimal', stralign='left'):
	"""
	:param data:
	:param headers: can be (), `keys` or `firstrow`
	:param tablefmt: one of simple, plain, grid, fancy_grid, pipe, orgtbl, jira, psql, rst, mediawiki, moinmoin, html, latex, latex_booktabs, tsv, textile
	:param floatfmt:
	:param missingval: what to put in for missing-value, ""
	:param numalign: `decimal` is default, or `left`, `center`, `right`
	:param stralign:
	:return:
	"""
	
	return tabulate.tabulate(tabular_data=data, headers=headers, tablefmt=tablefmt, floatfmt= floatfmt, numalign =numalign, stralign=stralign)
	







if __name__ == '__main__': print(__file__)