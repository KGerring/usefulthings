from inspect import signature, Parameter, _empty, Signature
from startups.helpers.introspection import arg

#_ParameterKind.VAR_KEYWORD if **kwargs
#_ParameterKind.VAR_POSITIONAL if *args
#Parameter.KEYWORD_ONLY if kwarg after *args
#Parameter.POSITIONAL_OR_KEYWORD is most flexible

_xtube_user = 'youtube_dl.extractor.xtube.XTubeUserIE'
#'https://www.xtube.com/profile/Mystic86-36973801/favvideos'

_chr = chr
_range = range


def consume_literal(literal):
	return lambda: [_chr(literal)]


def consume_range(start, end):
	return lambda: [_chr(literal) for literal in _range(start, end)]


def consume_branch(unknown, branches):
	return lambda: (choice() for choices in (consume((tokens,)) for tokens in random.choice(branches)) for choice in
					choices)


def consume_in(*tokens):
	choices = consume(tokens)
	return lambda: random.choice([value for choice in choices for value in choice()])


def consume_at(position):
	return lambda: Position[str(position).lower()]


def consume_max_repeat(start, end, tokens):
	choices = consume(tokens)
	return lambda: [choice() for choice in choices for i in range(0, random.randint(start, min(end, 255)))]


def consume_subpattern(id, tokens):
	choices = consume(tokens)
	return lambda: [choice() for choice in choices]


def consume(tokens):
	return [globals()['consume_{}'.format(str(name).lower())](*to_tuple(args)) for name, args in tokens]






def get_signature(obj):
	return arg(obj, True)

def param_values(sigspec):
	return list(sigspec.parameters.values())



def has_kwargs(sigspec):
	if isinstance(sigspec, Signature):
		return any(x.kind == x.VAR_KEYWORD for x in sigspec.parameters.values())
	else:
		sigspec = get_signature(sigspec)
		return any(x.kind == x.VAR_KEYWORD for x in sigspec.parameters.values())

def get_regular(sigspec):
	if isinstance(sigspec, Signature):
		sig = sigspec
	else:
		sig = get_signature(sigspec)
	return [(x.name, x.default) for x in sig.parameters.values()
			if x.kind in (x.POSITIONAL_ONLY, x.POSITIONAL_OR_KEYWORD, x.VAR_POSITIONAL)]



[(x.name, x.kind) for x in arg(attrgetter).parameters.values()]


def num_pos_args(sigspec):
	""" Return the number of positional arguments.  ``f(x, y=1)`` has 1"""
	return sum(1 for x in sigspec.parameters.values()
			   if x.kind == x.POSITIONAL_OR_KEYWORD
			   and x.default is x.empty)


def get_exclude_keywords(num_pos_only, sigspec):
	""" Return the names of position-only arguments if func has **kwargs"""
	if num_pos_only == 0:
		return ()
	has_kwargs = any(x.kind == x.VAR_KEYWORD for x in sigspec.parameters.values())
	if not has_kwargs:
		return ()
	pos_args = list(sigspec.parameters.values())[:num_pos_only]
	return tuple(x.name for x in pos_args)


def get_param_info(sig):
	defaults = []
	for param in sig.parameters.values():
		if param.default is not param.empty:
			defaults.append((param.name, param.default))
	return defaults


T =     TEMPLATE =      0x1  # Template (present because re module has it).
I =     IGNORECASE =    0x2  # Ignore case.
L =     LOCALE =        0x4  # Assume current 8-bit locale.
M =     MULTILINE =     0x8  # Make anchors look for newline.
S =     DOTALL =        0x10  # Make dot match newline.
U =     UNICODE =       0x20  # Assume Unicode locale.
X =     VERBOSE =       0x40  # Ignore whitespace and comments.
A =     ASCII =         0x80  # Assume ASCII locale.
V1 =    VERSION1 =      0x100  # New enhanced behaviour.
D =     DEBUG =         0x200  # Print parsed pattern.
R =     REVERSE =       0x400  # Search backwards.
W =     WORD =          0x800  # Default Unicode word breaks.
B =     BESTMATCH =     0x1000  # Best fuzzy match.
V0 =    VERSION0 =      0x2000  # Old legacy behaviour.
F =     FULLCASE =      0x4000  # Unicode full case-folding.
E =     ENHANCEMATCH =  0x8000  # Attempt to improve the fit after finding the first fuzzy match.
P =     POSIX =         0x10000  # POSIX-style matching (leftmost longest).

'pip list --format=custom --disable-pip-version-check -o'

from unicode_python.data import DATA_DIR, FILE_LIST

VF = lambda txt: U('VULGAR FRACTION %s' % txt)
from sympy.core.alphabets import greeks
from sympy.utilities.iterables import common_prefix, common_suffix
frac = {(1, 2): VF('ONE HALF'), (1, 3): VF('ONE THIRD'), (2, 3): VF('TWO THIRDS'), (1, 4): VF('ONE QUARTER'),
		(3, 4): VF('THREE QUARTERS'), (1, 5): VF('ONE FIFTH'), (2, 5): VF('TWO FIFTHS'), (3, 5): VF('THREE FIFTHS'),
		(4, 5): VF('FOUR FIFTHS'), (1, 6): VF('ONE SIXTH'), (5, 6): VF('FIVE SIXTHS'), (1, 8): VF('ONE EIGHTH'),
		(3, 8): VF('THREE EIGHTHS'), (5, 8): VF('FIVE EIGHTHS'), (7, 8): VF('SEVEN EIGHTHS')}


def _inner(strings, open_paren):
	from pygments.regexopt import commonprefix, escape, groupby, itemgetter, make_charset, re,regex_opt
	from pygments.regexopt import CS_ESCAPE, FIRST_ELEMENT
	from termcolor import cprint
	"""Return a regex that matches any string in the sorted list of strings."""
	close_paren = open_paren and ')' or ''
	# print strings, repr(open_paren)
	if not strings:
		cprint('-> nothing left', 'blue')
		return ''
	first = strings[0]      #get first in list
	if len(strings) == 1:
		cprint('-> only 1 string FIRST: {}'.format(first), 'blue')
		cprint(open_paren + escape(first) + close_paren, 'magenta')
		return open_paren + escape(first) + close_paren
	if not first:
		cprint('-> first string empty', 'blue')
		return open_paren + _inner(strings[1:], '(?:') + '?' + close_paren
	if len(first) == 1:
		# multiple one-char strings? make a charset
		oneletter = []
		rest = []
		for s in strings:
			if len(s) == 1:
				oneletter.append(s)         #make a simple [ABC]
			else:
				rest.append(s)
		if len(oneletter) > 1:
			cprint('we have more than one oneletter string; ONELETTER: {}'.format(str(oneletter)), 'blue')
			if rest:
				cprint('-> 1-character + REST: {}'.format(str(rest)), 'blue')      #other and Branch|[ABC]
				return open_paren + _inner(rest, '') + '|' + make_charset(oneletter) + close_paren
			cprint('-> only 1-character; no multi-length-string', 'blue')
			return open_paren + make_charset(oneletter) + close_paren
	prefix = commonprefix(strings)
	if prefix:
		plen = len(prefix)
									# we have a prefix for all strings
		cprint('-> prefix: {!r} of length {}'.format(prefix, str(plen)), 'blue')
		cprint(open_paren + escape(prefix) +
			   _inner([s[plen:] for s in strings],'(?:') + close_paren,'magenta')
		return open_paren + escape(prefix) + _inner([s[plen:] for s in strings], '(?:') + close_paren
	# is there a suffix?
	
	strings_rev = [s[::-1] for s in strings]
	suffix = commonprefix(strings_rev)
	if suffix:
		slen = len(suffix)
		cprint('-> suffix: {!r} of length {}'.format(suffix[::-1], str(slen)), 'blue')
		cprint(open_paren +
			   _inner(sorted(s[:-slen] for s in strings), '(?:') + escape(suffix[::-1]) + close_paren,
				'magenta')
		return open_paren + _inner(sorted(s[:-slen] for s in strings), '(?:') + escape(suffix[::-1]) + close_paren
	# recurse on common 1-string prefixes
	print('\x1b[34m-> last resort\x1b[0m\n\n#################################################')
	p = '(' + '|'.join(_inner(list(group[1]), '') for group in groupby(strings, lambda s: s[0] == first[0])) + close_paren
	cprint(p, 'magenta')
	return open_paren + '|'.join(_inner(list(group[1]), '')
								 for group in groupby(strings, lambda s: s[0] == first[0])) + close_paren


#######
import unittest


def skipUnlessHasattr(obj, attr):
	if hasattr(obj, attr):
		return lambda func: func
	return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))


class ExpectedFailureTestCase(unittest.TestCase):
	@unittest.expectedFailure
	def test_fail(self):
		self.assertEqual(1, 0, "broken")


class MyTestCase(unittest.TestCase):
	@unittest.skip("demonstrating skipping")
	def test_nothing(self):
		self.fail("shouldn't happen")
	
	@unittest.skipIf(mylib.__version__ < (1, 3),
					 "not supported in this library version")
	def test_format(self):
		# Tests that work for only a certain version of the library.
		pass
	
	@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
	def test_windows_support(self):
		# windows specific testing code
		pass



#assertRegex(text, regex, msg=None)
#assertNotRegex(text, regex, msg=None)

doctest.ELLIPSIS
doctest.SKIP

#doctest.testmod(verbose=True)
#doctest.testfile(filename) # test a txt as if its a huge docstring

'''
>>> print(list(range(20))) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
[0,    1, ...,   18,    19]


>>> C() #doctest: +ELLIPSIS
<__main__.C instance at 0x...>

https://docs.python.org/3/library/doctest.html#doctest.run_docstring_examples


import unittest
import doctest
import my_module_with_doctests

def load_tests(loader, tests, ignore):
	tests.addTests(doctest.DocTestSuite(my_module_with_doctests))
	return tests
	
#There are two main functions for creating unittest.TestSuite instances from text files and modules with doctests:



doctest.DocFileSuite(*paths, module_relative=True, package=None, setUp=None, tearDown=None, globs=None, optionflags=0, parser=DocTestParser(), encoding=None)
"""
	#Convert doctest tests from one or more text files to a unittest.TestSuite.
Optional argument package is a Python package or the name of a Python package whose directory should be used as the base directory for module-relative filenames in paths. If no package is specified, then the calling module’s directory is used as the base directory for module-relative filenames. It is an error to specify package if module_relative is False.

Optional argument setUp specifies a set-up function for the test suite.
This is called before running the tests in each file. The setUp function will be passed a DocTest object.
The setUp function can access the test globals as the globs attribute of the test passed.

Optional argument tearDown specifies a tear-down function for the test suite. This is called after running the tests in each file. The tearDown function will be passed a DocTest object. The setUp function can access the test globals as the globs attribute of the test passed.
"""

CR = '/Users/kristen/PycharmProjects/proj/unicode_python/unicode_python/data/regex_3/_regex_unicode.c'



static\s*?
RE_UINT8\s*?
re_(?P<name>[a-z_]+)_stage_(?P<stage>\d+)\[\]\s*?
=\s*?{(.+)}\;


'''

CR = '/Users/kristen/PycharmProjects/proj/unicode_python/unicode_python/data/regex_3/_regex_unicode.c'


import regex
name_stage = regex.compile(r're_(?P<name>[a-z_]+)_stage_(?P<stage>\d+)\[\]\s*?')

table = regex.compile('re_(?P<name>[a-z_]+)_stage_(?P<stage>\d+)\[\]\s*?=\s*?{\n(?P<table>[\s\d,]+)\}\;')


TEMPLATE = r're_{0[0]}_stage_{0[1]}\[\]\s*?'
TEMPLATE_1 = '=\s*?{\n(?P<table>[\s\d,]+)\}\;'



def get_table(match):
	if m:
		_table = match.group('table')
		table = regex.sub('\s', '', _table).strip(',')
		return [int(t) for t in table.split(',')]

def clean_table(int_table):
	table = regex.sub('\s', '', int_table).strip(',')
	return [int(t) for t in table.split(',')]

def get_chart(match):
	name = match.group('name')
	stage = match.group('stage')
	table = get_table(match)
	return name, stage, table



func = regex.compile(r're_get_(?P<name>[a-z_]+)\(.+\)\s*?\{(?P<body>.+)\s*'
					 r'return value\;\s*\}', regex.DOTALL)

#func.search(CR).group(2)
#func.search(CR).group('body')

def make_expression(name, prefix=''):
	"""
	're_get_bidi_mirrored\((.+)return value\;'
	:param name:
	:return:
	"""
	if not prefix:
		prefix = ''
	e = '{}{}'.format(prefix, name)
	expr = e +'\((.*)\s*return value\;\n\}'
	return regex.compile(expr, regex.DOTALL)

var = regex.compile('RE_UINT\d+\s*?(?P<var>[a-z_]+)\;')

first_field_shift = regex.compile(r'f \= ch \>\> (?P<field_shift>\d+)\;')
first_block_shift = regex.compile(r're_[a-z_]+_stage_1\[f\] \<\< (?P<block_shift>\d+)\;')

field_shift = regex.compile(r'f = code >> (?P<field_shift>\d+)\;')
block_shift = regex.compile(r're_(?P<name>[a-z_]+)_stage_(?P<stage>\d+)\[pos \+ f\] \<\< (?P<block_shift>\d+)\;')




FIRST_CODE = """
	f = ch >> {field_shift}
	code = ch ^ (f << {field_shift})
	pos = re_{name}_stage_1[f] << {block_shift}
"""


CODE = """
	f = code >> {field_shift}
	code ^= f << {field_shift}
	pos = re_{name}_stage_{stage}[pos + f] << {block_shift}
"""


END_BINARY = """
				pos += code
				value = (re_{name}_stage_{stage}[pos >> 3] >> (pos & 0x7)) & 0x1
				"""
END_ELSE = """
	value = re_{name}_stage_{stage}[pos + code]"""





stage =regex.compile(r'static RE_UINT8 '
			  r're_([a-z_]+)_stage_(\d+)\[\]\s*?'
			  r'=\s*?{(.+)}\;',
			  regex.VERBOSE|regex.V1)



def make_regex(*args, **kwargs):
	"""
	u = output('regexgen "attribute::att" "@att"')

	:param args:
	:param kwargs: flags
		-g      global match; find all matches rather than stopping after the first match
		-i      ignore case
		-m      multiline
		-u      unicode; treat pattern as a sequence of unicode code points
		
	:return:
	"""
	if kwargs and 'flags' in kwargs:
		flags = kwargs.get('flags', None)
	else:
		flags = ' '
		
	strings = args
	template = '"{}"'
	st = ' '.join([template.format(s) for s in strings])
	
	command_flags = 'regexgen {} '.format(flags)
	return command_flags + st


def regexgen(command):
	from startups.core import output
	result = output(command)
	return result.strip('/gimu')