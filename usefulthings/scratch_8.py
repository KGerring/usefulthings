from __future__ import absolute_import, unicode_literals
from startups import *
import sys, os
import re, regex
from startups.core import unpickler
import node.base
import node.events
import node.behaviors
import node.parts
import node.serializer
import node.utils
from node.behaviors import alias, attributes, cache, common, events, fallback, lifecycle, mapping, nodespace,nodify,order,reference,storage

from node.base import OrderedNode, Node, BaseNode
from functools import singledispatch
from decorator import dispatch_on
import _regex_core
import sre_parse
from sre_parse import (_UNITCODES, Tokenizer, SubPattern, Pattern, CHCODES, CATEGORIES)
import sre_compile
from sre_compile import _equivalences
import sre_constants
from random import choice, randint
import regex
from _regex_core import FULL_CASE_FOLDING
import six
import operator
import _regex_core as core
import operator
from _regex_core import _check_group_features





def make_possesive(element, min_count, max_count):
	from _regex_core import Atomic, GreedyRepeat


def parse_hex(source, info, in_set):
	saved_ignore = source.ignore_space
	source.ignore_space = False
	ch = source.get()
	source.ignore_space = saved_ignore
	if ch in HEX_ESCAPES:
		return parse_hex_escape(source, info, ch, HEX_ESCAPES[ch], in_set, ch)
	
	elif ch == "L" and not in_set:
		return parse_string_set(source, info)
	
	elif ch == "N":
		return parse_named_char(source, info, in_set)
	
	elif ch in ALPHA:
		if not in_set:
			if info.flags & WORD:
				value = WORD_POSITION_ESCAPES.get(ch)
			else:
				value = POSITION_ESCAPES.get(ch)
			if value:
				return value
		value = CHARSET_ESCAPES.get(ch)
		if value:
			return value
		value = CHARACTER_ESCAPES.get(ch)
		if value:
			return Character(ord(value))
		return make_character(info, ord(ch), in_set)
	
		
		
		
		
def test_core(func, string):
	from startups.regular import _regex_core as core
	src = core.Source(string)
	info = core.Info()
	if isinstance(func, str):
		func = getattr(core, func)
	return func(src, info)


	
		






	


def set_call_ref(self):
	key = self._key
	setattr(self.info, 'call_refs', {'0': key})
	return self


def has_group_calls(self):
	return self.info.group_calls


def check_group_features(info, parsed):
	"""Checks whether the reverse and fuzzy features of the group calls match
	the groups which they call.
	"""
	from _regex_core import REVERSE, Fuzzy, CallRef
	call_refs = {}
	additional_groups = []
	for call, reverse, fuzzy in info.group_calls:
		# Look up the reference of this group call.
		key = (call.group, reverse, fuzzy)
		ref = call_refs.get(key)
		if ref is None:
			# This group doesn't have a reference yet, so look up its features.
			if call.group == 0:
				# Calling the pattern as a whole.
				rev = bool(info.flags & REVERSE)
				fuz = isinstance(parsed, Fuzzy)
				if (rev, fuz) != (reverse, fuzzy):
					# The pattern as a whole doesn't have the features we want,
					# so we'll need to make a copy of it with the desired
					# features.
					additional_groups.append((CallRef(len(call_refs), parsed),
					                          reverse, fuzzy))
			else:
				# Calling a capture group.
				def_info = info.defined_groups[call.group]
				group = def_info[0]
				if def_info[1:] != (reverse, fuzzy):
					# The group doesn't have the features we want, so we'll
					# need to make a copy of it with the desired features.
					additional_groups.append((group, reverse, fuzzy))
			ref = len(call_refs)
			call_refs[key] = ref
		call.call_ref = ref
	info.call_refs = call_refs
	info.additional_groups = additional_groups


#todo value
def fold_case(c):
	from _regex_core import FULL_CASE_FOLDING
	import _regex
	#folded = "".join(chr(i.value) for i in items)
	return _regex.fold_case(FULL_CASE_FOLDING, c)

#todo ADD
def get_expanded():
	import _regex
	return _regex.get_expand_on_folding()


__invert__ = operator.__invert__
__not__ = operator.not_
core.SetDiff = operator.__sub__
core.SetSymDiff = operator.__xor__
core.SetInter = operator.__and__
core.SetUnion = operator.__or__






def get_arguments(cls):
	from inspect import isclass
	if isclass(cls):
		return list(arg(cls).parameters.values())


class Choice(list):
	"""
	Used to represent multiple possibilities at this point in a pattern string.
	We use a distinguished type, rather than a list, so that the usage in the
	code is clear.
	"""


class Group(list):
	"""
	Used to represent a capturing group in the pattern string.
	"""


class NonCapture(list):
	"""
	Used to represent a non-capturing group in the pattern string.
	"""


class RegexHelper(object):
	ESCAPE_MAPPINGS = dict(A=None, B=None, D='x', S='x', W='!', Z=None, b=None, d='0', s=' ', w='x')
	def __init__(self, pattern):
		self.pattern = pattern
	
	def normalize(self, pattern):
		r"""
		Given a reg-exp pattern, normalizes it to an iterable of forms that
		suffice for reverse matching. This does the following:

		(1) For any repeating sections, keeps the minimum number of occurrences
			permitted (this means zero for optional groups).
		(2) If an optional group includes parameters, include one occurrence of
			that group (along with the zero occurrence case from step (1)).
		(3) Select the first (essentially an arbitrary) element from any character
			class. Select an arbitrary character for any unordered class (e.g. '.'
			or '\w') in the pattern.
		(4) Ignore look-ahead and look-behind assertions.
		(5) Raise an error on any disjunctive ('|') constructs.

		Django's URLs for forward resolving are either all positional arguments or
		all keyword arguments. That is assumed here, as well. Although reverse
		resolving can be done using positional args when keyword args are
		specified, the two cannot be mixed in the same reverse() call.
		"""
		# Do a linear scan to work out the special features of this pattern. The
		# idea is that we scan once here and collect all the information we need to
		# make future decisions.
		result = []
		non_capturing_groups = []
		consume_next = True
		pattern_iter = self.next_char(iter(pattern))
		num_args = 0
		
		# A "while" loop is used here because later on we need to be able to peek
		# at the next character and possibly go around without consuming another
		# one at the top of the loop.
		try:
			ch, escaped = next(pattern_iter)
		except StopIteration:
			return [('', [])]
		
		try:
			while True:
				if escaped:
					result.append(ch)
				elif ch == '.':
					# Replace "any character" with an arbitrary representative.
					result.append(".")
				elif ch == '|':
					# FIXME: One day we'll should do this, but not in 1.0.
					raise NotImplementedError('Awaiting Implementation')
				elif ch == "^":
					pass
				elif ch == '$':
					break
				elif ch == ')':
					# This can only be the end of a non-capturing group, since all
					# other unescaped parentheses are handled by the grouping
					# section later (and the full group is handled there).
					#
					# We regroup everything inside the capturing group so that it
					# can be quantified, if necessary.
					start = non_capturing_groups.pop()
					inner = NonCapture(result[start:])
					result = result[:start] + [inner]
				elif ch == '[':
					# Replace ranges with the first character in the range.
					ch, escaped = next(pattern_iter)
					result.append(ch)
					ch, escaped = next(pattern_iter)
					while escaped or ch != ']':
						ch, escaped = next(pattern_iter)
				elif ch == '(':
					# Some kind of group.
					ch, escaped = next(pattern_iter)
					if ch != '?' or escaped:
						# A positional group
						name = "_%d" % num_args
						num_args += 1
						result.append(Group((("%%(%s)s" % name), name)))
						self.walk_to_end(ch, pattern_iter)
					else:
						ch, escaped = next(pattern_iter)
						if ch in '!=<':
							# All of these are ignorable. Walk to the end of the
							# group.
							self.walk_to_end(ch, pattern_iter)
						elif ch in 'iLmsu#':
							warnings.warn(
									'Using (?%s) in url() patterns is deprecated.' % ch,
									RemovedInDjango21Warning
							)
							self.walk_to_end(ch, pattern_iter)
						elif ch == ':':
							# Non-capturing group
							non_capturing_groups.append(len(result))
						elif ch != 'P':
							# Anything else, other than a named group, is something
							# we cannot reverse.
							raise ValueError("Non-reversible reg-exp portion: '(?%s'" % ch)
						else:
							ch, escaped = next(pattern_iter)
							if ch not in ('<', '='):
								raise ValueError("Non-reversible reg-exp portion: '(?P%s'" % ch)
							# We are in a named capturing group. Extra the name and
							# then skip to the end.
							if ch == '<':
								terminal_char = '>'
							# We are in a named backreference.
							else:
								terminal_char = ')'
							name = []
							ch, escaped = next(pattern_iter)
							while ch != terminal_char:
								name.append(ch)
								ch, escaped = next(pattern_iter)
							param = ''.join(name)
							# Named backreferences have already consumed the
							# parenthesis.
							if terminal_char != ')':
								result.append(Group((("%%(%s)s" % param), param)))
								self.walk_to_end(ch, pattern_iter)
							else:
								result.append(Group((("%%(%s)s" % param), None)))
				elif ch in "*?+{":
					# Quantifiers affect the previous item in the result list.
					count, ch = self.get_quantifier(ch, pattern_iter)
					if ch:
						# We had to look ahead, but it wasn't need to compute the
						# quantifier, so use this character next time around the
						# main loop.
						consume_next = False
					
					if count == 0:
						if self.contains(result[-1], Group):
							# If we are quantifying a capturing group (or
							# something containing such a group) and the minimum is
							# zero, we must also handle the case of one occurrence
							# being present. All the quantifiers (except {0,0},
							# which we conveniently ignore) that have a 0 minimum
							# also allow a single occurrence.
							result[-1] = Choice([None, result[-1]])
						else:
							result.pop()
					elif count > 1:
						result.extend([result[-1]] * (count - 1))
				else:
					# Anything else is a literal.
					result.append(ch)
				
				if consume_next:
					ch, escaped = next(pattern_iter)
				else:
					consume_next = True
		except StopIteration:
			pass
		except NotImplementedError:
			# A case of using the disjunctive form. No results for you!
			return [('', [])]
		
		return list(zip(*self.flatten_result(result)))
	
	def next_char(self, input_iter):
		r"""
		An iterator that yields the next character from "pattern_iter", respecting
		escape sequences. An escaped character is replaced by a representative of
		its class (e.g. \w -> "x"). If the escaped character is one that is
		skipped, it is not returned (the next character is returned instead).

		Yields the next character, along with a boolean indicating whether it is a
		raw (unescaped) character or not.
		"""
		for ch in input_iter:
			if ch != '\\':
				yield ch, False
				continue
			ch = next(input_iter)
			representative = self.ESCAPE_MAPPINGS.get(ch, ch)
			if representative is None:
				continue
			yield representative, True
	
	def walk_to_end(self, ch, input_iter):
		"""
		The iterator is currently inside a capturing group. We want to walk to the
		close of this group, skipping over any nested groups and handling escaped
		parentheses correctly.
		"""
		if ch == '(':
			nesting = 1
		else:
			nesting = 0
		for ch, escaped in input_iter:
			if escaped:
				continue
			elif ch == '(':
				nesting += 1
			elif ch == ')':
				if not nesting:
					return
				nesting -= 1
	
	def get_quantifier(self, ch, input_iter):
		"""
		Parse a quantifier from the input, where "ch" is the first character in the
		quantifier.

		Returns the minimum number of occurrences permitted by the quantifier and
		either None or the next character from the input_iter if the next character
		is not part of the quantifier.
		"""
		if ch in '*?+':
			try:
				ch2, escaped = next(input_iter)
			except StopIteration:
				ch2 = None
			if ch2 == '?':
				ch2 = None
			if ch == '+':
				return 1, ch2
			return 0, ch2
		
		quant = []
		while ch != '}':
			ch, escaped = next(input_iter)
			quant.append(ch)
		quant = quant[:-1]
		values = ''.join(quant).split(',')
		
		# Consume the trailing '?', if necessary.
		try:
			ch, escaped = next(input_iter)
		except StopIteration:
			ch = None
		if ch == '?':
			ch = None
		return int(values[0]), ch
	
	def flatten_result(self, source):
		"""
		Turns the given source sequence into a list of reg-exp possibilities and
		their arguments. Returns a list of strings and a list of argument lists.
		Each of the two lists will be of the same length.
		"""
		if source is None:
			return [''], [[]]
		if isinstance(source, Group):
			if source[1] is None:
				params = []
			else:
				params = [source[1]]
			return [source[0]], [params]
		result = ['']
		result_args = [[]]
		pos = last = 0
		for pos, elt in enumerate(source):
			if isinstance(elt, str):
				continue
			piece = ''.join(source[last:pos])
			if isinstance(elt, Group):
				piece += elt[0]
				param = elt[1]
			else:
				param = None
			last = pos + 1
			for i in range(len(result)):
				result[i] += piece
				if param:
					result_args[i].append(param)
			if isinstance(elt, (Choice, NonCapture)):
				if isinstance(elt, NonCapture):
					elt = [elt]
				inner_result, inner_args = [], []
				for item in elt:
					res, args = self.flatten_result(item)
					inner_result.extend(res)
					inner_args.extend(args)
				new_result = []
				new_args = []
				for item, args in zip(result, result_args):
					for i_item, i_args in zip(inner_result, inner_args):
						new_result.append(item + i_item)
						new_args.append(args[:] + i_args)
				result = new_result
				result_args = new_args
		if pos >= last:
			piece = ''.join(source[last:])
			for i in range(len(result)):
				result[i] += piece
		return result, result_args
	
	def contains(self, source, inst):
		"""
		Returns True if the "source" contains an instance of "inst". False,
		otherwise.
		"""
		if isinstance(source, inst):
			return True
		if isinstance(source, NonCapture):
			for elt in source:
				if contains(elt, inst):
					return True
		return False

	



ESCAPE_MAPPINGS = {'A': None, 'B': None, 'D': 'x', 'S': 'x', 'W': '!',
                   'Z': None,
                   'b': None, 'd': '0', 's': ' ', 'w': 'x'}


def next_char(input_iter):
	r"""
	An iterator that yields the next character from "pattern_iter", respecting
	escape sequences. An escaped character is replaced by a representative of
	its class (e.g. \w -> "x"). If the escaped character is one that is
	skipped, it is not returned (the next character is returned instead).

	Yields the next character, along with a boolean indicating whether it is a
	raw (unescaped) character or not.
	"""
	for ch in input_iter:
		if ch != '\\':
			yield ch, False
			continue
		ch = next(input_iter)
		representative = ESCAPE_MAPPINGS.get(ch, ch)
		if representative is None:
			continue
		yield representative, True
	
def walk_to_end(ch, input_iter):
	"""
	The iterator is currently inside a capturing group. We want to walk to the
	close of this group, skipping over any nested groups and handling escaped
	parentheses correctly.
	"""
	if ch == '(':
		nesting = 1
	else:
		nesting = 0
	for ch, escaped in input_iter:
		if escaped:
			continue
		elif ch == '(':
			nesting += 1
		elif ch == ')':
			if not nesting:
				return
			nesting -= 1


#19 = sre_constants.LITERAL


#AB.parsed._merge_common_prefixes(AB.info, 0, AB.parsed.branches)
#AB.parsed._flush_char_prefix(info, reverse, prefixed, order, new_branches)

#_split_common_suffix
#_reduce_to_set
#b._flush_set_members(info, reverse, items, case_flags, new_branches)
#b._can_split(items, count)

_flush_set_members(info, reverse, items, case_flags, new_branches)


category_digit = '0123456789'


class Serializer(object):
	def __init__(self, **config):
		self.cfg = config
	
	@dispatch_on('obj')
	def write(self, obj):
		return obj
	
@Serializer.write.register(_regex_core.Character)
def writechar(self, obj):
	return chr(obj.value)

@Serializer.write.register(_regex_core.Literal)
@Serializer.write.register(_regex_core.String)
def writeliteral(self, obj):
	return ''.join(chr(c) for c in obj.characters)



#UNLIMITED

#self.constraints
CON ="dise"

#self.constraints["cost"]["max"]


#[self.constraints[e] for e in "dise"]
#[self.constraints["cost"][e] for e in 'dis']


def _dispatch_on(*dispatch_args):
	"""
	Factory of decorators turning a function into a generic function
	dispatching on the given arguments.
	"""
	assert dispatch_args, 'No dispatch args passed'
	dispatch_str = '(%s,)' % ', '.join(dispatch_args)
	
	def check(arguments, wrong=operator.ne, msg=''):
		"""Make sure one passes the expected number of arguments"""
		if wrong(len(arguments), len(dispatch_args)):
			raise TypeError('Expected %d arguments, got %d%s' %
			                (len(dispatch_args), len(arguments), msg))
	
	def gen_func_dec(func):
		"""Decorator turning a function into a generic function"""
		# first check the dispatch arguments
		argset = set(getfullargspec(func).args)
		if not set(dispatch_args) <= argset:
			raise NameError('Unknown dispatch arguments %s' % dispatch_str)
		typemap = {}
		
		def vancestors(*types):
			"""
			Get a list of sets of virtual ancestors for the given types
			"""
			check(types)
			ras = [[] for _ in range(len(dispatch_args))]
			for types_ in typemap:
				for t, type_, ra in zip(types, types_, ras):
					if issubclass(t, type_) and type_ not in t.mro():
						append(type_, ra)
			return [set(ra) for ra in ras]
		
		def ancestors(*types):
			"""
			Get a list of virtual MROs, one for each type
			"""
			check(types)
			lists = []
			for t, vas in zip(types, vancestors(*types)):
				n_vas = len(vas)
				if n_vas > 1:
					raise RuntimeError(
							'Ambiguous dispatch for %s: %s' % (t, vas))
				elif n_vas == 1:
					va, = vas
					mro = type('t', (t, va), {}).mro()[1:]
				else:
					mro = t.mro()
				lists.append(mro[:-1])  # discard t and object
			return lists
		
		def register(*types):
			"""
			Decorator to register an implementation for the given types
			"""
			check(types)
			
			def dec(f):
				check(getfullargspec(f).args, operator.lt, ' in ' + f.__name__)
				typemap[types] = f
				return f
			
			return dec
		
		def dispatch_info(*types):
			"""
			An utility to introspect the dispatch algorithm
			"""
			check(types)
			lst = []
			for anc in itertools.product(*ancestors(*types)):
				lst.append(tuple(a.__name__ for a in anc))
			return lst
		
		def _dispatch(dispatch_args, *args, **kw):
			types = tuple(type(arg) for arg in dispatch_args)
			try:  # fast path
				f = typemap[types]
			except KeyError:
				pass
			else:
				return f(*args, **kw)
			combinations = itertools.product(*ancestors(*types))
			next(combinations)  # the first one has been already tried
			for types_ in combinations:
				f = typemap.get(types_)
				if f is not None:
					return f(*args, **kw)
			# else call the default implementation
			return func(*args, **kw)
		
		return FunctionMaker.create(
				func, 'return _f_(%s, %%(shortsignature)s)' % dispatch_str,
				dict(_f_=_dispatch), register=register, default=func,
				typemap=typemap, vancestors=vancestors, ancestors=ancestors,
				dispatch_info=dispatch_info, __wrapped__=func)
	
	gen_func_dec.__name__ = 'dispatch_on' + dispatch_str
	return gen_func_dec


def _dispatch(dispatch_args, *args, **kw):
	typemap = {}
	types = tuple(type(arg) for arg in dispatch_args)
	try:  # fast path
		f = typemap[types]
	except KeyError:
		pass
	else:
		return f(*args, **kw)
	combinations = itertools.product(*ancestors(*types))
	next(combinations)  # the first one has been already tried
	for types_ in combinations:
		f = typemap.get(types_)
		if f is not None:
			return f(*args, **kw)
	# else call the default implementation
	return func(*args, **kw)


def _inner(strings, open_paren):
	from pygments.regexopt import commonprefix, escape, groupby, itemgetter, make_charset, re, regex_opt
	from pygments.regexopt import CS_ESCAPE, FIRST_ELEMENT
	from termcolor import cprint
	"""Return a regex that matches any string in the sorted list of strings."""
	close_paren = open_paren and ')' or ''
	# print strings, repr(open_paren)
	if not strings:
		cprint('-> nothing left', 'blue')
		return ''
	first = strings[0]  # get first in list
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
				oneletter.append(s)  # make a simple [ABC]
			else:
				rest.append(s)
		if len(oneletter) > 1:
			cprint('we have more than one oneletter string; ONELETTER: {}'.format(str(oneletter)), 'blue')
			if rest:
				cprint('-> 1-character + REST: {}'.format(str(rest)), 'blue')  # other and Branch|[ABC]
				return open_paren + _inner(rest, '') + '|' + make_charset(oneletter) + close_paren
			cprint('-> only 1-character; no multi-length-string', 'blue')
			return open_paren + make_charset(oneletter) + close_paren
	prefix = commonprefix(strings)
	if prefix:
		plen = len(prefix)
		# we have a prefix for all strings
		cprint('-> prefix: {!r} of length {}'.format(prefix, str(plen)), 'blue')
		cprint(open_paren + escape(prefix) +
		       _inner([s[plen:] for s in strings], '(?:') + close_paren, 'magenta')
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
	p = '(' + '|'.join(
			_inner(list(group[1]), '') for group in groupby(strings, lambda s: s[0] == first[0])) + close_paren
	cprint(p, 'magenta')
	return open_paren + '|'.join(_inner(list(group[1]), '')
	                             for group in groupby(strings, lambda s: s[0] == first[0])) + close_paren


def parse_sub_cond(source, state, condgroup, verbose): pass





if __name__ == '__main__':
	ab = ['aa', 'ab', 'ba', 'bb']
	inner(ab)


