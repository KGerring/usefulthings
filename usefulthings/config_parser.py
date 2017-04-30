#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = config_parser
# author=AutisticScreeching
# date = 4/4/17
import sys, os
import configparser
from configparser import (ConfigParser as _ConfigParser, RawConfigParser, SectionProxy,
                          MissingSectionHeaderError, DuplicateOptionError, DuplicateSectionError,
                          _UNSET, Interpolation, DEFAULTSECT, ConverterMapping, NoOptionError, NoSectionError
                          )
from py._iniconfig import SectionWrapper, IniConfig, iscommentline
from pathlib import Path
from orderedmultidict import omdict
from collections.abc import MutableMapping
from collections import OrderedDict as _default_dict, ChainMap as _ChainMap, defaultdict
import re
import itertools
from usefulthings.log import configure_stream
from botocore.configloader import raw_config_parse
INI = '/Users/kristen/.config/revealme.ini'
CONFIG = '/Users/kristen/.config/pythonista.ini'

from os.path import basename, splitext, abspath

LEVELS = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}

VERBOSE = True

if VERBOSE:
	logger = configure_stream(level='DEBUG', use_logfile=False)
	#logger.removeHandler(logger.handlers[0])
	if len(logger.handlers) == 2:
		logger.removeHandler(logger.handlers[0])

else:
	logger = configure_stream(level='INFO', use_logfile=False)
	#logger.removeHandler(logger.handlers[0])
	#logger.handlers = logger.handlers[-1]


class PrefixDict():pass


class MultiConfig(object):
	def __init__(self, files=None, *args, **kwargs):
		self.files = []
		self.config = dict()
		for file in files:
			self.files.append(file)
		for i, file in enumerate(files):
			self.config[i] = file
			
	@staticmethod
	def parse_config_file(filename, subsections=True):
		return raw_config_parse(config_filename=filename, parse_subsections=subsections)
		#return parsed
	
	def add_file(self, files=None, prefix = '{}'):
		if not files:
			files = self.files
		else:
			self.files.extend(files)
			
	def get_base(self, filename):
		return splitext(basename(abspath(filename)))
		
		
translator = dict([('_2d', '-'),
              ('_2D', '-'),
              ('_2E', '.'),
              ('_2e', '.'),
              ('_2F', '/'),
              ('_2f', '/'),
              ('_3A', ':'),
              ('_3a', ':'),
              ('_40', '@'),
              ('_5f', '_'),
              ('_5F', '_'),
                ('_2b', '+'),
                ('_2B','+')])
#re.sub('(_)(\d)([A-Za-z])', '%\\2\\3', C)


class MultiConfigParser(RawConfigParser):
	def __init__(self, *args, **kwargs):
		super(MultiConfigParser, self).__init__(*args, **kwargs)
		self.cursect = None
		self.files = []
		
	@staticmethod
	def raw_config(filename, parse_subsections=True):
		return raw_config_parse(config_filename=filename, parse_subsections=parse_subsections)
	
	def read(self, filenames, encoding=None):
		if isinstance(filenames, str):
			filenames = [filenames]
		self.files = []
		for filename in filenames:
			try:
				with open(filename, encoding=encoding) as fp:
					self._read(fp, filename)
			except OSError:
				continue
				self.files.append(filename)
		return self.files
	
	def options(self, section, with_defaults=False):
		try:
			opts = self._sections.get(section, dict()).copy()
		except KeyError:
			return None
		if with_defaults:
			opts.update(self._defaults)
		return list(opts.keys())
	
	def _get_(self):
		pass
	
	def items(self, section=_UNSET, raw=False, vars=None):
		"""Return a list of (name, value) tuples for each option in a section.

		All % interpolations are expanded in the return values, based on the
		defaults passed into the constructor, unless the optional argument
		`raw' is true.  Additional substitutions may be provided using the
		`vars' argument, which must be a dictionary whose contents overrides
		any pre-existing defaults.

		The section DEFAULT is special.
		"""
		if section is _UNSET:
			return super().items()
		d = self._defaults.copy()
		try:
			d.update(self._sections[section])
		except KeyError:
			if section != self.default_section:
				raise NoSectionError(section)
		# Update with the entry specific variables
		if vars:
			for key, value in vars.items():
				d[self.optionxform(key)] = value
		value_getter = lambda option: self._interpolation.before_get(self,
		                                                             section, option, d[option], d)
		if raw:
			value_getter = lambda option: d[option]
		return [(option, value_getter(option)) for option in d.keys()]
	
	def set(self, section, option, value=None):
		"""Set an option."""
		if value:
			value = self._interpolation.before_set(self, section, option, value)
		if not section or section == self.default_section:
			sectdict = self._defaults
		else:
			try:
				sectdict = self._sections[section]
			except KeyError:
				raise NoSectionError(section) from None
		sectdict[self.optionxform(option)] = value
	
	def setlist(self, section, option, value=None):
		"""Set an option."""
		if value:
			value = self._interpolation.before_set(self, section, option, value)
		if not section or section == self.default_section:
			sectdict = self._defaults
		else:
			try:
				sectdict = self._sections[section]
			except KeyError:
				self.add_section(section)
				sectdict = self._sections[section]
				#raise NoSectionError(section) from None
		
		sectdict[self.optionxform(option)] = value
	
	def __setitem__(self, key, value):
		# To conform with the mapping protocol, overwrites existing values in
		# the section.
		
		# XXX this is not atomic if read_dict fails at any point. Then again,
		# no update method in configparser is atomic in this implementation.
		if key == self.default_section:
			self._defaults.clear()
		elif key in self._sections:
			self._sections[key].clear()
		self.read_dict({key: value})
	
	def _unify_values(self, section, vars):
		"""Create a sequence of lookups with 'vars' taking priority over
		the 'section' which takes priority over the DEFAULTSECT.

		"""
		sectiondict = {}
		try:
			sectiondict = self._sections[section]
		except KeyError:
			if section != self.default_section:
				raise NoSectionError(section)
		# Update with the entry specific variables
		vardict = {}
		if vars:
			for key, value in vars.items():
				if value is not None:
					value = str(value)
				vardict[self.optionxform(key)] = value
		return _ChainMap(vardict, sectiondict, self._defaults)

	def _read(self, fp, fpname):
		"""Parse a sectioned configuration file.

		Each section in a configuration file contains a header, indicated by
		a name in square brackets (`[]'), plus key/value options, indicated by
		`name' and `value' delimited with a specific substring (`=' or `:' by
		default).

		Values can span multiple lines, as long as they are indented deeper
		than the first line of the value. Depending on the parser's mode, blank
		lines may be treated as parts of multiline values or ignored.

		Configuration files may include comments, prefixed by specific
		characters (`#' and `;' by default). Comments may appear on their own
		in an otherwise empty line or may be entered in lines holding values or
		section names.
		"""
		elements_added = set()
		cursect = None  # None, or a dictionary
		sectname = None
		optname = None
		lineno = 0
		indent_level = 0
		e = None  # None, or an exception
		for lineno, line in enumerate(fp, start=1):
			comment_start = sys.maxsize
			# strip inline comments
			#inline_prefixes = {p: -1 for p in self._inline_comment_prefixes}
			#while comment_start == sys.maxsize and inline_prefixes:
				#next_prefixes = {}
				#for prefix, index in inline_prefixes.items():
				#	index = line.find(prefix, index + 1)
					#if index == -1:
					#	continue
					#next_prefixes[prefix] = index
					#if index == 0 or (index > 0 and line[index - 1].isspace()):
						#comment_start = min(comment_start, index)
				#inline_prefixes = next_prefixes
			# strip full line comments
			for prefix in self._comment_prefixes:
				if line.strip().startswith(prefix):
					comment_start = 0
					break
			if comment_start == sys.maxsize:
				comment_start = None
			value = line[:comment_start].strip()
			logger.debug('value {}'.format(str(value)))
			if not value:
				#if self._empty_lines_in_values:
					# add empty line to the value, but only if there was no
					# comment on the line
				if (comment_start is None and cursect is not None and optname and cursect.get(optname) is not None):
					logger.debug('optname {}'.format(optname))
					logger.debug('cursect {}'.format(cursect))
					cursect[optname].append('')  # newlines added at join
				#else:
					# empty line marks end of value
					#indent_level = sys.maxsize
				#continue
			# continuation line?
			first_nonspace = self.NONSPACECRE.search(line)
			cur_indent_level = first_nonspace.start() if first_nonspace else 0
			if (cursect is not None and optname and cur_indent_level > indent_level):
				cursect[optname].append(value)
			# a section header or option header?
			else:
				indent_level = cur_indent_level
				# is it a section header?
				mo = self.SECTCRE.match(value)
				if mo:
					sectname = mo.group('header')
					logger.debug('SECTNAME ==> {}'.format(sectname))
					if sectname in self._sections: #todo in section; adding
						if self._strict and sectname in elements_added:
							raise DuplicateSectionError(sectname, fpname, lineno)
						##todo split cursect into the section
						cursect = self._sections[sectname]
						logger.debug('cursect {}'.format(cursect))
						elements_added.add(sectname)
					elif sectname == self.default_section:
						cursect = self._defaults
					else:
						#todo blank cursect, add to self._section and self._proxies
						cursect = omdict()
						self._sections[sectname] = cursect
						self._proxies[sectname] = SectionProxy(self, sectname)
						elements_added.add(sectname)
					# So sections can't start with a continuation line
					optname = None
				# no section header in the file?
				#todo add it to default?
				elif cursect is None:
					raise MissingSectionHeaderError(fpname, lineno, line)
				# an option line?
				else:
					#NO section Name
					mo = self._optcre.match(value)
					if mo:
						optname, vi, optval = mo.group('option', 'vi', 'value')
						if not optname:
							e = self._handle_error(e, fpname, lineno, line)
						optname = self.optionxform(optname.rstrip())
						if (sectname, optname) in elements_added:
							if self._strict:
								raise DuplicateOptionError(sectname, optname, fpname, lineno)
							if not self._strict:
								if optval is not None:
									optval = optval.strip()
									if cursect[optname] is not None:
										cursect[optname].add(optval)
									elif cursect[optname] is None:
										cursect[optname] = [optval]
									else:
										cursect[optname] = [optval]
								else:
									cursect[optname] = None

						elements_added.add((sectname, optname))
					else:
						# a non-fatal parsing error occurred. set up the
						# exception but keep going. the exception will be
						# raised at the end of the file and will contain a
						# list of all bogus lines
						e = self._handle_error(e, fpname, lineno, line)
						
		self._join_multiline_values()
		self.files.append(fpname)
		# if any parsing errors occurred, raise an exception
		#if e:
			#pass
			#raise e pass
	def read_dict(self, dictionary, source='<dict>'):
		"""Read configuration from a dictionary.

		Keys are section names, values are dictionaries with keys and values
		that should be present in the section. If the used dictionary type
		preserves order, sections and their keys will be added in order.

		All types held in the dictionary are converted to strings during
		reading, including section names, option names and keys.

		Optional second argument is the `source' specifying the name of the
		dictionary being read.
		"""
		elements_added = set()
		for section, optionkeys in dictionary.items():
			section = str(section)
			try:
				self.add_section(section)
			except (DuplicateSectionError, ValueError):
				if self._strict and section in elements_added:
					raise
			elements_added.add(section)
			for option, value in optionkeys.items():
				option = self.optionxform(str(option))
				if value is not None:
					value = str(value)
				if self._strict and (section, option) in elements_added:
					self.setlist(section, option, value)
					#raise DuplicateOptionError(section, key, source)
				elements_added.add((section, option))
				self.set(section, option, value)
##
def add_converter(key='key', ext=None): pass

def _read(self, fp, fpname, strict=None, rSECTRE='\[(?P<header>[^]]+)\]'):
	"""Parse a sectioned configuration file.

	Each section in a configuration file contains a header, indicated by
	a name in square brackets (`[]'), plus key/value options, indicated by
	`name' and `value' delimited with a specific substring (`=' or `:' by
	default).

	Values can span multiple lines, as long as they are indented deeper
	than the first line of the value. Depending on the parser's mode, blank
	lines may be treated as parts of multiline values or ignored.

	Configuration files may include comments, prefixed by specific
	characters (`#' and `;' by default). Comments may appear on their own
	in an otherwise empty line or may be entered in lines holding values or
	section names.
	"""
	if not strict:
		_strict = self._strict
	else:
		_strict = strict
	sectnames = []
	cursects = []
	elements_added = set()
	cursect = None  # None, or a dictionary
	sectname = None
	optname = None
	lineno = 0
	indent_level = 0
	default_section = 'DEFAULT'
	defaults = self.default_section, self._defaults
	all_sections = itertools.chain((defaults,), self._sections.items())
	_inline_comment_prefixes = self._inline_comment_prefixes
	_comment_prefixes = self._comment_prefixes
	_empty_lines_in_values = True
	e = None  # None, or an exception
	for lineno, line in enumerate(fp, start=1):
		comment_start = sys.maxsize
		# strip inline comments
		# inline_prefixes = {p: -1 for p in _inline_comment_prefixes}
		# while comment_start == sys.maxsize and inline_prefixes:
		#	next_prefixes = {}
		#	for prefix, index in inline_prefixes.items():
		#		index = line.find(prefix, index + 1)
		#		if index == -1:
		#			continue
		#		next_prefixes[prefix] = index
		#		if index == 0 or (index > 0 and line[index - 1].isspace()):
		#			comment_start = min(comment_start, index)
		#	inline_prefixes = next_prefixes
		# strip full line comments
		for prefix in self._comment_prefixes:
			if line.strip().startswith(prefix):
				comment_start = 0
				break
		if comment_start == sys.maxsize:
			comment_start = None
		value = line[:comment_start].strip()
		if not value:
			if self._empty_lines_in_values:
				# add empty line to the value, but only if there was no
				# comment on the line
				if (comment_start is None and
						    cursect is not None and
					    optname and
						    cursect[optname] is not None):
					cursect[optname].append('')  # newlines added at join
			else:
				# empty line marks end of value
				indent_level = sys.maxsize
			continue
		# continuation line?
		first_nonspace = self.NONSPACECRE.search(line)
		# first_nonspace = re.compile(r'\S', re.UNICODE).search(line)
		cur_indent_level = first_nonspace.start() if first_nonspace else 0
		if (cursect is not None and optname and cur_indent_level > indent_level):
			cursect[optname].append(value)
		# print(value)
		# a section header or option header?
		else:
			indent_level = cur_indent_level
			# is it a section header?
			mo = self.SECTCRE.match(value)
			if mo:
				sectname = mo.group('header')
				sectnames.append(sectname)
				print('sectname0', sectname)
				if sectname in self._sections:
					if _strict and sectname in elements_added:
						raise DuplicateSectionError(sectname, fpname, lineno)
					cursect = self._sections[sectname]
					# print('cursect', cursect)
					elements_added.add(sectname)
				elif sectname == self.default_section:
					cursect = self._defaults
				else:
					print('NEW_CURSECT')
					cursect = omdict()
					self._sections[sectname] = cursect
					self._proxies[sectname] = SectionProxy(self, sectname)
					elements_added.add(sectname)
				# So sections can't start with a continuation line
				optname = None
			# no section header in the file?
			elif cursect is None:
				raise MissingSectionHeaderError(fpname, lineno, line)
			# an option line?
			else:
				mo = self._optcre.match(value)
				if mo:
					optname, vi, optval = mo.group('option', 'vi', 'value')
					if not optname:
						e = self._handle_error(e, fpname, lineno, line)
					optname = self.optionxform(optname.rstrip())
					if (sectname, optname) in elements_added:
						if _strict:
							raise DuplicateOptionError(sectname, optname, fpname, lineno)
						if optval is not None:
							optval = optval.strip()
							cursect.add(optname, optval)
					if (_strict and (sectname, optname) in elements_added):
						raise DuplicateOptionError(sectname, optname, fpname, lineno)
					elements_added.add((sectname, optname))
					# This check is fine because the OPTCRE cannot
					# match if it would set optval to None
					if optval is not None:
						optval = optval.strip()
						# print('sectname', sectname)
						# print('cursect', cursect)
						# print('optname', optname)
						# print('optval', optval)
						cursect[optname] = [optval]
					else:
						# valueless option handling
						cursect[optname] = None
				else:
					# a non-fatal parsing error occurred. set up the
					# exception but keep going. the exception will be
					# raised at the end of the file and will contain a
					# list of all bogus lines
					e = self._handle_error(e, fpname, lineno, line)
	self._join_multiline_values()
	self.files.append(fpname)
	# if any parsing errors occurred, raise an exception
	if e:
		raise e
	# return elements_added

##
class MultiRawConfigParser(MutableMapping):
	"""ConfigParser that does not do interpolation."""
	
	# Regular expressions for parsing section headers and options
	_SECT_TMPL = r"""
        \[                                 # [
        (?P<header>[^]]+)                  # very permissive!
        \]                                 # ]
        """
	_OPT_TMPL = r"""
        (?P<option>.*?)                    # very permissive!
        \s*(?P<vi>{delim})\s*              # any number of space/tab,
                                           # followed by any of the
                                           # allowed delimiters,
                                           # followed by any space/tab
        (?P<value>.*)$                     # everything up to eol
        """
	_OPT_NV_TMPL = r"""
        (?P<option>.*?)                    # very permissive!
        \s*(?:                             # any number of space/tab,
        (?P<vi>{delim})\s*                 # optionally followed by
                                           # any of the allowed
                                           # delimiters, followed by any
                                           # space/tab
        (?P<value>.*))?$                   # everything up to eol
        """
	_NV = """(?P<option>.*?)\s*(?:(?P<vi>{delim})\s*(?P<value>.*))?$"""
	
	# Interpolation algorithm to be used if the user does not specify another
	_DEFAULT_INTERPOLATION = Interpolation()
	# Compiled regular expression for matching sections
	SECTCRE = re.compile(_SECT_TMPL, re.VERBOSE)
	# Compiled regular expression for matching options with typical separators
	OPTCRE = re.compile(_OPT_TMPL.format(delim="=|:"), re.VERBOSE)
	# Compiled regular expression for matching options with optional values
	# delimited using typical separators
	OPTCRE_NV = re.compile(_OPT_NV_TMPL.format(delim="=|:"), re.VERBOSE)
	# Compiled regular expression for matching leading whitespace in a line
	NONSPACECRE = re.compile(r"\S")
	# Possible boolean values in the configuration.
	BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
	                  '0': False, 'no': False, 'false': False, 'off': False}
	
	def __init__(self, defaults=None, dict_type=omdict,
	             allow_no_value=False, *, delimiters=('=', ':'),
	             comment_prefixes=('#', ';'), inline_comment_prefixes=None,
	             strict=False, empty_lines_in_values=True,
	             default_section=DEFAULTSECT,
	             interpolation=_UNSET, converters=_UNSET):
		
		self._dict = dict_type
		self._sections = self._dict()
		self._defaults = self._dict()
		self._converters = ConverterMapping(self)
		self._proxies = self._dict()
		self._proxies[default_section] = SectionProxy(self, default_section)
		if defaults:
			for key, value in defaults.items():
				self._defaults[self.optionxform(key)] = value
		self._delimiters = tuple(delimiters)
		if delimiters == ('=', ':'):
			self._optcre = self.OPTCRE_NV if allow_no_value else self.OPTCRE
		else:
			d = "|".join(re.escape(d) for d in delimiters)
			if allow_no_value:
				self._optcre = re.compile(self._OPT_NV_TMPL.format(delim=d),
				                          re.VERBOSE)
			else:
				self._optcre = re.compile(self._OPT_TMPL.format(delim=d),
				                          re.VERBOSE)
		self._comment_prefixes = tuple(comment_prefixes or ())
		self._inline_comment_prefixes = tuple(inline_comment_prefixes or ())
		self._strict = strict
		self._allow_no_value = allow_no_value
		self._empty_lines_in_values = empty_lines_in_values
		self.default_section = default_section
		self._interpolation = interpolation
		if self._interpolation is _UNSET:
			self._interpolation = self._DEFAULT_INTERPOLATION
		if self._interpolation is None:
			self._interpolation = Interpolation()
		if converters is not _UNSET:
			self._converters.update(converters)
	
	def defaults(self):
		return self._defaults
	
	def sections(self):
		"""Return a list of section names, excluding [DEFAULT]"""
		# self._sections will never have [DEFAULT] in it
		return list(self._sections.keys())
	
	def add_section(self, section):
		"""Create a new section in the configuration.

		Raise DuplicateSectionError if a section by the specified name
		already exists. Raise ValueError if name is DEFAULT.
		"""
		if section == self.default_section:
			raise ValueError('Invalid section name: %r' % section)
		
		if section in self._sections:
			raise DuplicateSectionError(section)
		self._sections[section] = self._dict()
		self._proxies[section] = SectionProxy(self, section)
	
	def has_section(self, section):
		"""Indicate whether the named section is present in the configuration.

		The DEFAULT section is not acknowledged.
		"""
		return section in self._sections
	
	def options(self, section):
		"""Return a list of option names for the given section name."""
		try:
			opts = self._sections[section].copy()
		except KeyError:
			raise NoSectionError(section) from None
		opts.update(self._defaults)
		return list(opts.keys())
	
	def read(self, filenames, encoding=None):
		"""Read and parse a filename or a list of filenames.

		Files that cannot be opened are silently ignored; this is
		designed so that you can specify a list of potential
		configuration file locations (e.g. current directory, user's
		home directory, systemwide directory), and all existing
		configuration files in the list will be read.  A single
		filename may also be given.

		Return list of successfully read files.
		"""
		if isinstance(filenames, str):
			filenames = [filenames]
		read_ok = []
		for filename in filenames:
			try:
				with open(filename, encoding=encoding) as fp:
					self._read(fp, filename)
			except OSError:
				continue
			read_ok.append(filename)
		return read_ok
	
	def read_file(self, f, source=None):
		"""Like read() but the argument must be a file-like object.

		The `f' argument must be iterable, returning one line at a time.
		Optional second argument is the `source' specifying the name of the
		file being read. If not given, it is taken from f.name. If `f' has no
		`name' attribute, `<???>' is used.
		"""
		if source is None:
			try:
				source = f.name
			except AttributeError:
				source = '<???>'
		self._read(f, source)
	
	def read_string(self, string, source='<string>'):
		"""Read configuration from a given string."""
		sfile = io.StringIO(string)
		self.read_file(sfile, source)
	
	def read_dict(self, dictionary, source='<dict>'):
		"""Read configuration from a dictionary.

		Keys are section names, values are dictionaries with keys and values
		that should be present in the section. If the used dictionary type
		preserves order, sections and their keys will be added in order.

		All types held in the dictionary are converted to strings during
		reading, including section names, option names and keys.

		Optional second argument is the `source' specifying the name of the
		dictionary being read.
		"""
		elements_added = set()
		for section, keys in dictionary.items():
			section = str(section)
			try:
				self.add_section(section)
			except (DuplicateSectionError, ValueError):
				if self._strict and section in elements_added:
					raise
			elements_added.add(section)
			for key, value in keys.items():
				key = self.optionxform(str(key))
				if value is not None:
					value = str(value)
				if self._strict and (section, key) in elements_added:
					raise DuplicateOptionError(section, key, source)
				elements_added.add((section, key))
				self.set(section, key, value)
	
	def readfp(self, fp, filename=None):
		"""Deprecated, use read_file instead."""
		warnings.warn(
				"This method will be removed in future versions.  "
				"Use 'parser.read_file()' instead.",
				DeprecationWarning, stacklevel=2
		)
		self.read_file(fp, source=filename)
	
	def get(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
		"""Get an option value for a given section.

		If `vars' is provided, it must be a dictionary. The option is looked up
		in `vars' (if provided), `section', and in `DEFAULTSECT' in that order.
		If the key is not found and `fallback' is provided, it is used as
		a fallback value. `None' can be provided as a `fallback' value.

		If interpolation is enabled and the optional argument `raw' is False,
		all interpolations are expanded in the return values.

		Arguments `raw', `vars', and `fallback' are keyword only.

		The section DEFAULT is special.
		"""
		try:
			d = self._unify_values(section, vars)
		except NoSectionError:
			if fallback is _UNSET:
				raise
			else:
				return fallback
		option = self.optionxform(option)
		try:
			value = d[option]
		except KeyError:
			if fallback is _UNSET:
				raise NoOptionError(option, section)
			else:
				return fallback
		
		if raw or value is None:
			return value
		else:
			return self._interpolation.before_get(self, section, option, value,
			                                      d)
	
	def _get(self, section, conv, option, **kwargs):
		return conv(self.get(section, option, **kwargs))
	
	def _get_conv(self, section, option, conv, *, raw=False, vars=None,
	              fallback=_UNSET, **kwargs):
		try:
			return self._get(section, conv, option, raw=raw, vars=vars,
			                 **kwargs)
		except (NoSectionError, NoOptionError):
			if fallback is _UNSET:
				raise
			return fallback
	
	# getint, getfloat and getboolean provided directly for backwards compat
	def getint(self, section, option, *, raw=False, vars=None,
	           fallback=_UNSET, **kwargs):
		return self._get_conv(section, option, int, raw=raw, vars=vars,
		                      fallback=fallback, **kwargs)
	
	def getfloat(self, section, option, *, raw=False, vars=None,
	             fallback=_UNSET, **kwargs):
		return self._get_conv(section, option, float, raw=raw, vars=vars,
		                      fallback=fallback, **kwargs)
	
	def getboolean(self, section, option, *, raw=False, vars=None,
	               fallback=_UNSET, **kwargs):
		return self._get_conv(section, option, self._convert_to_boolean,
		                      raw=raw, vars=vars, fallback=fallback, **kwargs)
	
	def items(self, section=_UNSET, raw=False, vars=None):
		"""Return a list of (name, value) tuples for each option in a section.

		All % interpolations are expanded in the return values, based on the
		defaults passed into the constructor, unless the optional argument
		`raw' is true.  Additional substitutions may be provided using the
		`vars' argument, which must be a dictionary whose contents overrides
		any pre-existing defaults.

		The section DEFAULT is special.
		"""
		if section is _UNSET:
			return super().items()
		d = self._defaults.copy()
		try:
			d.update(self._sections[section])
		except KeyError:
			if section != self.default_section:
				raise NoSectionError(section)
		# Update with the entry specific variables
		if vars:
			for key, value in vars.items():
				d[self.optionxform(key)] = value
		value_getter = lambda option: self._interpolation.before_get(self,
		                                                             section, option, d[option], d)
		if raw:
			value_getter = lambda option: d[option]
		return [(option, value_getter(option)) for option in d.keys()]
	
	def popitem(self):
		"""Remove a section from the parser and return it as
		a (section_name, section_proxy) tuple. If no section is present, raise
		KeyError.

		The section DEFAULT is never returned because it cannot be removed.
		"""
		for key in self.sections():
			value = self[key]
			del self[key]
			return key, value
		raise KeyError
	
	def optionxform(self, optionstr):
		return optionstr.lower()
	
	def has_option(self, section, option):
		"""Check for the existence of a given option in a given section.
		If the specified `section' is None or an empty string, DEFAULT is
		assumed. If the specified `section' does not exist, returns False."""
		if not section or section == self.default_section:
			option = self.optionxform(option)
			return option in self._defaults
		elif section not in self._sections:
			return False
		else:
			option = self.optionxform(option)
			return (option in self._sections[section]
			        or option in self._defaults)
	
	def set(self, section, option, value=None):
		"""Set an option."""
		if value:
			value = self._interpolation.before_set(self, section, option,
			                                       value)
		if not section or section == self.default_section:
			sectdict = self._defaults
		else:
			try:
				sectdict = self._sections[section]
			except KeyError:
				raise NoSectionError(section) from None
		sectdict[self.optionxform(option)] = value
	
	def write(self, fp, space_around_delimiters=True):
		"""Write an .ini-format representation of the configuration state.

		If `space_around_delimiters' is True (the default), delimiters
		between keys and values are surrounded by spaces.
		"""
		if space_around_delimiters:
			d = " {} ".format(self._delimiters[0])
		else:
			d = self._delimiters[0]
		if self._defaults:
			self._write_section(fp, self.default_section,
			                    self._defaults.items(), d)
		for section in self._sections:
			self._write_section(fp, section,
			                    self._sections[section].items(), d)
	
	def _write_section(self, fp, section_name, section_items, delimiter):
		"""Write a single section to the specified `fp'."""
		fp.write("[{}]\n".format(section_name))
		for key, value in section_items:
			value = self._interpolation.before_write(self, section_name, key,
			                                         value)
			if value is not None or not self._allow_no_value:
				value = delimiter + str(value).replace('\n', '\n\t')
			else:
				value = ""
			fp.write("{}{}\n".format(key, value))
		fp.write("\n")
	
	def remove_option(self, section, option):
		"""Remove an option."""
		if not section or section == self.default_section:
			sectdict = self._defaults
		else:
			try:
				sectdict = self._sections[section]
			except KeyError:
				raise NoSectionError(section) from None
		option = self.optionxform(option)
		existed = option in sectdict
		if existed:
			del sectdict[option]
		return existed
	
	def remove_section(self, section):
		"""Remove a file section."""
		existed = section in self._sections
		if existed:
			del self._sections[section]
			del self._proxies[section]
		return existed
	
	def __getitem__(self, key):
		if key != self.default_section and not self.has_section(key):
			raise KeyError(key)
		return self._proxies[key]
	
	def __setitem__(self, key, value):
		# To conform with the mapping protocol, overwrites existing values in
		# the section.
		
		# XXX this is not atomic if read_dict fails at any point. Then again,
		# no update method in configparser is atomic in this implementation.
		if key == self.default_section:
			self._defaults.clear()
		elif key in self._sections:
			self._sections[key].clear()
		self.read_dict({key: value})
	
	def __delitem__(self, key):
		if key == self.default_section:
			raise ValueError("Cannot remove the default section.")
		if not self.has_section(key):
			raise KeyError(key)
		self.remove_section(key)
	
	def __contains__(self, key):
		return key == self.default_section or self.has_section(key)
	
	def __len__(self):
		return len(self._sections) + 1  # the default section
	
	def __iter__(self):
		# XXX does it break when underlying container state changed?
		return itertools.chain((self.default_section,), self._sections.keys())
	
	def _read(self, fp, fpname):
		"""Parse a sectioned configuration file.

		Each section in a configuration file contains a header, indicated by
		a name in square brackets (`[]'), plus key/value options, indicated by
		`name' and `value' delimited with a specific substring (`=' or `:' by
		default).

		Values can span multiple lines, as long as they are indented deeper
		than the first line of the value. Depending on the parser's mode, blank
		lines may be treated as parts of multiline values or ignored.

		Configuration files may include comments, prefixed by specific
		characters (`#' and `;' by default). Comments may appear on their own
		in an otherwise empty line or may be entered in lines holding values or
		section names.
		"""
		elements_added = set()
		cursect = None  # None, or a dictionary
		sectname = None
		optname = None
		lineno = 0
		indent_level = 0
		e = None  # None, or an exception
		for lineno, line in enumerate(fp, start=1):
			comment_start = sys.maxsize
			# strip inline comments
			inline_prefixes = {p: -1 for p in self._inline_comment_prefixes}
			while comment_start == sys.maxsize and inline_prefixes:
				next_prefixes = {}
				for prefix, index in inline_prefixes.items():
					index = line.find(prefix, index + 1)
					if index == -1:
						continue
					next_prefixes[prefix] = index
					if index == 0 or (index > 0 and line[index - 1].isspace()):
						comment_start = min(comment_start, index)
				inline_prefixes = next_prefixes
			# strip full line comments
			for prefix in self._comment_prefixes:
				if line.strip().startswith(prefix):
					comment_start = 0
					break
			if comment_start == sys.maxsize:
				comment_start = None
			value = line[:comment_start].strip()
			if not value:
				if self._empty_lines_in_values:
					# add empty line to the value, but only if there was no
					# comment on the line
					if (comment_start is None and
							    cursect is not None and
						    optname and
							    cursect[optname] is not None):
						cursect[optname].append('')  # newlines added at join
				else:
					# empty line marks end of value
					indent_level = sys.maxsize
				continue
			# continuation line?
			first_nonspace = self.NONSPACECRE.search(line)
			cur_indent_level = first_nonspace.start() if first_nonspace else 0
			if (cursect is not None and optname and
					    cur_indent_level > indent_level):
				cursect[optname].append(value)
			# a section header or option header?
			else:
				indent_level = cur_indent_level
				# is it a section header?
				mo = self.SECTCRE.match(value)
				if mo:
					sectname = mo.group('header')
					if sectname in self._sections:
						if self._strict and sectname in elements_added:
							raise DuplicateSectionError(sectname, fpname,
							                            lineno)
						cursect = self._sections[sectname]
						elements_added.add(sectname)
					elif sectname == self.default_section:
						cursect = self._defaults
					else:
						cursect = self._dict()
						self._sections[sectname] = cursect
						self._proxies[sectname] = SectionProxy(self, sectname)
						elements_added.add(sectname)
					# So sections can't start with a continuation line
					optname = None
				# no section header in the file?
				elif cursect is None:
					raise MissingSectionHeaderError(fpname, lineno, line)
				# an option line?
				else:
					mo = self._optcre.match(value)
					if mo:
						optname, vi, optval = mo.group('option', 'vi', 'value')
						if not optname:
							e = self._handle_error(e, fpname, lineno, line)
						optname = self.optionxform(optname.rstrip())
						if (self._strict and
								    (sectname, optname) in elements_added):
							raise DuplicateOptionError(sectname, optname,
							                           fpname, lineno)
						elements_added.add((sectname, optname))
						# This check is fine because the OPTCRE cannot
						# match if it would set optval to None
						if optval is not None:
							optval = optval.strip()
							cursect[optname] = [optval]
						else:
							# valueless option handling
							cursect[optname] = None
					else:
						# a non-fatal parsing error occurred. set up the
						# exception but keep going. the exception will be
						# raised at the end of the file and will contain a
						# list of all bogus lines
						e = self._handle_error(e, fpname, lineno, line)
		self._join_multiline_values()
		# if any parsing errors occurred, raise an exception
		if e:
			raise e
	
	def _join_multiline_values(self):
		defaults = self.default_section, self._defaults
		all_sections = itertools.chain((defaults,),
		                               self._sections.items())
		for section, options in all_sections:
			for name, val in options.items():
				if isinstance(val, list):
					val = '\n'.join(val).rstrip()
				options[name] = self._interpolation.before_read(self,
				                                                section,
				                                                name, val)
	
	def _handle_error(self, exc, fpname, lineno, line):
		if not exc:
			exc = ParsingError(fpname)
		exc.append(lineno, repr(line))
		return exc
	
	def _unify_values(self, section, vars):
		"""Create a sequence of lookups with 'vars' taking priority over
		the 'section' which takes priority over the DEFAULTSECT.

		"""
		sectiondict = {}
		try:
			sectiondict = self._sections[section]
		except KeyError:
			if section != self.default_section:
				raise NoSectionError(section)
		# Update with the entry specific variables
		vardict = {}
		if vars:
			for key, value in vars.items():
				if value is not None:
					value = str(value)
				vardict[self.optionxform(key)] = value
		return _ChainMap(vardict, sectiondict, self._defaults)
	
	def _convert_to_boolean(self, value):
		"""Return a boolean value translating from other types if necessary.
		"""
		if value.lower() not in self.BOOLEAN_STATES:
			raise ValueError('Not a boolean: %s' % value)
		return self.BOOLEAN_STATES[value.lower()]
	
	def _validate_value_types(self, *, section="", option="", value=""):
		"""Raises a TypeError for non-string values.

		The only legal non-string value if we allow valueless
		options is None, so we need to check if the value is a
		string if:
		- we do not allow valueless options, or
		- we allow valueless options but the value is not None

		For compatibility reasons this method is not used in classic set()
		for RawConfigParsers. It is invoked in every case for mapping protocol
		access and in ConfigParser.set().
		"""
		if not isinstance(section, str):
			raise TypeError("section names must be strings")
		if not isinstance(option, str):
			raise TypeError("option keys must be strings")
		if not self._allow_no_value or value:
			if not isinstance(value, str):
				raise TypeError("option values must be strings")
	
	@property
	def converters(self):
		return self._converters



if __name__ == '__main__':
	MCP = MultiConfigParser()
	logger.debug('START')
	iniconfig = MCP.raw_config(INI)
	config = MCP.raw_config(CONFIG)
	MCP.read_dict(iniconfig)
	MCP.read_dict(config)