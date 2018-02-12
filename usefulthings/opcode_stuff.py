#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = opcode_stuff
# author=KGerring
# author_email=''
# date = 12/11/17
""" filename = opcode_stuff"""
from __future__ import absolute_import, unicode_literals # isort:skip
from startups import *
import sys
import os
import regex
import re
import dis
import opcode
from toolz import partitionby
from numba import bytecode
from startups.misc import itemgetter, attrgetter
from collections import OrderedDict, defaultdict
import imp
from cx_Freeze import finder
from cx_Freeze.hooks import initialize
from modulefinder import ModuleFinder
from IPython.utils.capture import capture_output
from modulegraph import modulegraph
from startups.helpers.decorators import return_as
#from numba.analysis import CFGraph #_nodes,_preds, _succs,_edge_data,_entry_point
#from numba.controlflow import ControlFlowAnalysis

DIS_JOIN_PY37 = '/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/tmp3_jtpv3k'
DIS_JOIN_PY36 = '/var/folders/33/x2sr5vwx2dv48zl7f0s3vynw0000gn/T/tmpt5y8og4z'



NEW_INPY37 = """LOAD_METHOD(namei)
Loads a method named co_names[namei] from TOS object.
TOS is popped and method and TOS are pushed when interpreter can call unbound method directly.
TOS will be used as the first argument (self) by CALL_METHOD.
Otherwise, NULL and method is pushed (method is bound method or something else).

New in version 3.7.

CALL_METHOD(argc)
Calls a method. argc is number of positional arguments.
Keyword arguments are not supported.
This opcode is designed to be used with LOAD_METHOD.
Positional arguments are on top of the stack.
Below them, two items described in LOAD_METHOD on the stack.
All of them are popped and return value is pushed.

New in ve"""

LOAD_METHOD = 160
CALL_METHOD = 161

#get_instructions = Iterator for the opcodes in methods, functions or code
#/Users/kristen/Downloads/Python-3.7.0a4/Lib

#PickleShareDB
#OrderedSet
#fi = dill.dill._create_weakproxy(find, True)
#dill.dill._create_weakref

def _disassemble_recursive(co, *, file=None, depth=None):
	import dis
	
	dis.disassemble(co, file=file)
	if depth is None or depth > 0:
		if depth is not None:
			depth = depth - 1
		for x in co.co_consts:
			if hasattr(x, 'co_code'):
				print(file=file)
				print("Disassembly of %r:" % (x,), file=file)
				_disassemble_recursive(x, file=file, depth=depth)


def _disassemble_str(source, **kwargs):
	"""Compile the source string, then disassemble the code object."""
	import inspect
	import dis
	if not isinstance(source, str):
		try:
			source = inspect.getsource(source)
		except Exception:
			source = str
	_disassemble_recursive(dis._try_compile(source, '<dis>'), **kwargs)


FUNCTION_IDENTITY_ATTRS = ['arg_names', #list(pysig.parameters)
                           'code',      #dis._get_code_object(obj)
                           'filename',      #self.code.co_filename
                           'firstlineno',   #self.code.co_firstlineno
                           'func',          #func = obj
                           'func_name',     #obj.__name__
                           'func_qualname', #obj.__qualname__
                           'is_generator',  #inspect.isgeneratorfunction(obj)
                           'modname',       #inspect.getmodule(obj).__name__ or <dynamic>
                           'module',        #inspect.getmodule(obj)
                           'pysig',         #inspect.signature(obj)
                           'unique_name'    #unique_name = '{}${}'.format(self.func_qualname, uid)
                           ]


def from_func(obj):

	func = obj
	code = dis._get_code_object(obj)
	pysig = inspect.signature(obj)
	try:
		func_qualname = obj.__qualname__
	except AttributeError:
		func_qualname = obj.__name__
	self = bytecode.FunctionIdentity()
	self.func = func
	self.func_qualname = func_qualname
	self.func_name = func_qualname.split('.')[-1]
	self.code = code
	self.module = inspect.getmodule(func)
	self.modname = ('<dynamic>' if self.module is None else self.module.__name__)
	self.is_generator = inspect.isgeneratorfunction(func)
	self.pysig = pysig
	self.filename = code.co_filename
	self.firstlineno = code.co_firstlineno
	self.arg_names = list(pysig.parameters)
	uid = next(bytecode.FunctionIdentity._unique_ids)
	self.unique_name = '{}${}'.format(self.func_qualname, uid)
	return self


#source(CF.add_edge)

#'LOAD_BUILD_CLASS'
#'startups'

#t[20:26]


def scan_opcodes(co):
	import dis
	code = co.co_code
	names = co.co_names
	consts = co.co_consts
	STORE_OPS = (90, 97)
	IMPORT_NAME = 108
	IMPORT_FROM = 109
	IMPORT_STAR = 84
	LOAD_CONST = 100
	
	opargs = [(op, arg) for _, op, arg in dis._unpack_opargs(code) if op != dis.EXTENDED_ARG]
	for i, (op, oparg) in enumerate(opargs):
		if op in STORE_OPS:
			yield "store", (names[oparg],)
			continue
		if op == IMPORT_FROM:
			yield "import from", names[oparg]
			
		if (op == IMPORT_NAME and i >= 2
		    and opargs[i - 1][0] == opargs[i - 2][0] == LOAD_CONST):
			level = consts[opargs[i - 2][1]]
			fromlist = consts[opargs[i - 1][1]]
			if level == 0:  # absolute import
				yield "absolute_import", (fromlist, names[oparg])
			else:  # relative import
				yield "relative_import", (level, fromlist, names[oparg])
			continue


def _scan_bytecode_stores(co, m=None):
	constants = co.co_consts
	m = set([])
	for inst in dis.get_instructions(co):
		if inst.opname in ('STORE_NAME', 'STORE_GLOBAL'):
			name = co.co_names[inst.arg]
			print(inst.opname, name)
			#m.globalnames.add(name)
	cotype = type(co)
	for c in constants:
		if isinstance(c, cotype):
			print('scanning constant {}'.format(c))
			_scan_bytecode_stores(c, m=None)
####
####

#'IMPORT_NAME'

"""
CALL_FUNCTION(argc)

   Calls a function.  *argc* indicates the number of positional
   arguments. The positional arguments are on the stack, with the
   right-most argument on top.  Below the arguments, the function
   object to call is on the stack. Pops all function arguments, and
   the function itself off the stack, and pushes the return value.

   Changed in version 3.6: This opcode is used only for calls with
   positional arguments.

CALL_FUNCTION_KW(argc)

   Calls a function.  *argc* indicates the number of arguments
   (positional and keyword).  The top element on the stack contains a
   tuple of keyword argument names.  Below the tuple, keyword
   arguments are on the stack, in the order corresponding to the
   tuple.  Below the keyword arguments, the positional arguments are
   on the stack, with the right-most parameter on top.  Below the
   arguments, the function object to call is on the stack. Pops all
   function arguments, and the function itself off the stack, and
   pushes the return value.

   Changed in version 3.6: Keyword arguments are packed in a tuple
   instead of a dictionary, *argc* indicates the total number of
   arguments

CALL_FUNCTION_EX(flags)

   Calls a function. The lowest bit of *flags* indicates whether the
   var-keyword argument is placed at the top of the stack.  Below the
   var-keyword argument, the var-positional argument is on the stack.
   Below the arguments, the function object to call is placed. Pops
   all function arguments, and the function itself off the stack, and
   pushes the return value. Note that this opcode pops at most three
   items from the stack. Var-positional and var-keyword arguments are
   packed by "BUILD_MAP_UNPACK_WITH_CALL" and
   "BUILD_MAP_UNPACK_WITH_CALL".

   New in version 3.6.


MAKE_FUNCTION(argc)

   Pushes a new function object on the stack.  From bottom to top, the
   consumed stack must consist of values if the argument carries a
   specified flag value

   * "0x01" a tuple of default argument objects in positional order

   * "0x02" a dictionary of keyword-only parameters' default values

   * "0x04" an annotation dictionary

   * "0x08" a tuple containing cells for free variables, making a
     closure

   * the code associated with the function (at TOS1)

   * the *qualified name* of the function (at TOS)
   
   
LOAD_GLOBAL(namei)

   Loads the global named "co_names[namei]" onto the stack.
   
   
LOAD_ATTR(namei)

   Replaces TOS with "getattr(TOS, co_names[namei])".
   
   
LOAD_CONST(consti)

   Pushes "co_consts[consti]" onto the stack.

LOAD_NAME(namei)

   Pushes the value associated with "co_names[namei]" onto the stack.
   
STORE_ATTR(namei)

   Implements "TOS.name = TOS1", where *namei* is the index of name in
   "co_names".
   
LOAD_BUILD_CLASS

   Pushes "builtins.__build_class__()" onto the stack.  It is later
   called by "CALL_FUNCTION" to construct a class.
   
IMPORT_STAR

   Loads all symbols not starting with "'_'" directly from the module
   TOS to the local namespace. The module is popped after loading all
   names. This opcode implements "from module import *".
   
   """


def _scan_bytecode(co):
	constants = co.co_consts
	level = None
	fromlist = None
	prev_insts = []
	starimports = OrderedSet([])
	globalnames = OrderedSet([])
	importnames = OrderedSet([])
	localnames =  OrderedSet([])
	
	for inst in dis.get_instructions(co):
		if inst.opname == 'IMPORT_NAME':
			assert prev_insts[-2].opname == 'LOAD_CONST'
			assert prev_insts[-1].opname == 'LOAD_CONST'
			level =     co.co_consts[prev_insts[-2].arg]
			fromlist =  co.co_consts[prev_insts[-1].arg]
			
			
			assert fromlist is None or type(fromlist) is tuple
			name = co.co_names[inst.arg]
			have_star = False
			if fromlist is not None:
				fromlist = set(fromlist)
				if '*' in fromlist:
					fromlist.remove('*')
					have_star = True
				#"absolute_import", (fromlist, names[oparg])
				#"relative_import", (level, fromlist, names[oparg])
			#print(name, fromlist, level)   (fromlist, names[oparg])
				importnames.add((name, tuple(fromlist)))
				for item in fromlist:
					print('from -> {}.{} ({})'.format(name, item, inst.offset))
			if have_star:
				starimports.add(name)
				print('star -> {} ({})'.format(name, inst.offset))
			if not have_star and fromlist is None:
				importnames.append(name)
			#imported_module = self._safe_import_hook(name, m, fromlist, level)[0]
			#if have_star:
			#	m.globalnames.update(imported_module.globalnames)
			#	m.starimports.update(imported_module.starimports)
			#	if imported_module.code is None:
			#		m.starimports.add(name)
		elif inst.opname in ('STORE_NAME', 'STORE_GLOBAL'):
			# keep track of all global names that are assigned to
			name = co.co_names[inst.arg]
			if inst.opname == 'STORE_GLOBAL':
				localnames.add(name)
			globalnames.add(name)
			print('name -> {} ({})'.format(name, inst.offset))
			
		prev_insts.append(inst)
		#print(len(prev_insts))
		#print([inst.offset for inst in prev_insts])
		del prev_insts[:-2]
	cotype = type(co)
	for c in constants:
		if hasattr(c, 'co_code'):
			print('*'*60)
			print('checking {!r} in {!r} ({})'.format(c.co_name, c.co_filename, inst.offset))
			_scan_bytecode(c)

	return (starimports, globalnames, importnames, localnames)



#G._load_module('startups', fp, startups.__path__[0], info)
#list(G.graph.iterdfs('startups'))
#list(g._iterbfs('startups'))
#g.head(5)
#all_edges
#back_bfs
#back_dfs
#edge_by_id
#edge_by_node
#edge_data
#forw_bfs
#forw_dfs

#inc_degree,out_degree #int
#inc_edges,out_edges #edge number
#inc_nbrs,out_nbrs



TERM_OPS =  bytecode.TERM_OPS
NO_ARG_LEN = bytecode.NO_ARG_LEN
JUMP_OPS = bytecode.JUMP_OPS
JREL_OPS = bytecode.JREL_OPS
JABS_OPS = bytecode.JABS_OPS

#bytecode.ByteCodeIter

class OpCodes(object):
	from toolz import merge
	hasconst = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasconst])
	hascompare = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hascompare])
	hasfree = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasfree])
	hasjabs = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasjabs])
	hasjrel = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasjrel])
	haslocal = dict([(op, opcode.opname.__getitem__(op)) for op in dis.haslocal])
	hasname = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasname])
	hasnargs = dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasnargs])
	cmp_op = dis.cmp_op
	
	jump_ops = merge(hasjabs, hasjrel)
	
	JABS_OPS = [(op, opcode.opname[op]) for op in bytecode.JABS_OPS]
	JUMP_OPS = [(op, opcode.opname[op]) for op in bytecode.JUMP_OPS]
	TERM_OPS = [(op, opcode.opname[op]) for op in bytecode.TERM_OPS]
	
	def __init__(self, op=None):
		self.op = op
		if not self.op:
			self.opname = None
		else:
			self.opname = opcode.opname.__getitem__(self.op)
	
	@classmethod
	def _has(self, name):
		try:
			return getattr(self, name)
		except AttributeError:
			seq = getattr(dis, name)
			val = dict([(op, opcode.opname.__getitem__(op)) for op in seq])
			setattr(self, name, val)
			return val
	
	
	def _get(self, name, seq = []):
		try:
			return getattr(self, name)
		except AttributeError:
			val = dict([(op, opcode.opname.__getitem__(op)) for op in seq])
			setattr(self, name, val)
			return val


STACK_DICT = '''{
	"-3": ["STORE_SUBSCR"],
	"-2": ["MAP_ADD", "STORE_ATTR", "DELETE_SUBSCR", "CALL_FUNCTION_KW", "MAKE_FUNCTION"],
	"-1": ["BINARY_SUBSCR", "IMPORT_NAME", "STORE_ANNOTATION", "INPLACE_POWER", "STORE_FAST", "CALL_FUNCTION", "RETURN_VALUE", "BUILD_CONST_KEY_MAP", "INPLACE_AND", "YIELD_FROM", "INPLACE_MULTIPLY", "BINARY_AND", "BINARY_POWER", "WITH_CLEANUP_FINISH", "SET_ADD", "STORE_GLOBAL", "INPLACE_ADD", "INPLACE_RSHIFT", "BINARY_ADD", "BINARY_SUBTRACT", "BINARY_RSHIFT", "RAISE_VARARGS", "BUILD_MAP", "BINARY_TRUE_DIVIDE", "INPLACE_FLOOR_DIVIDE", "BINARY_OR", "IMPORT_STAR", "END_FINALLY", "DELETE_ATTR", "BINARY_MULTIPLY", "POP_TOP", "BINARY_MODULO", "BINARY_FLOOR_DIVIDE", "INPLACE_TRUE_DIVIDE", "POP_JUMP_IF_TRUE", "INPLACE_XOR", "LIST_APPEND", "STORE_NAME", "INPLACE_OR", "BUILD_SLICE", "INPLACE_LSHIFT", "POP_JUMP_IF_FALSE", "INPLACE_MODULO", "PRINT_EXPR", "BINARY_LSHIFT", "INPLACE_MATRIX_MULTIPLY", "BINARY_MATRIX_MULTIPLY", "STORE_DEREF", "CALL_FUNCTION_EX", "COMPARE_OP", "INPLACE_SUBTRACT", "BINARY_XOR"],
	"0": ["DELETE_GLOBAL", "UNARY_INVERT", "LOAD_ATTR", "FORMAT_VALUE", "GET_AWAITABLE", "POP_EXCEPT", "JUMP_FORWARD", "BUILD_TUPLE_UNPACK_WITH_CALL", "BUILD_LIST", "SETUP_LOOP", "DELETE_FAST", "SETUP_ANNOTATIONS", "BUILD_LIST_UNPACK", "BUILD_STRING", "CONTINUE_LOOP", "GET_YIELD_FROM_ITER", "BUILD_TUPLE", "ROT_THREE", "UNARY_NEGATIVE", "POP_BLOCK", "BUILD_MAP_UNPACK", "UNARY_NOT", "YIELD_VALUE", "DELETE_NAME", "BUILD_MAP_UNPACK_WITH_CALL", "BUILD_TUPLE_UNPACK", "JUMP_ABSOLUTE", "GET_AITER", "ROT_TWO", "BUILD_SET", "GET_ITER", "BREAK_LOOP", "DELETE_DEREF", "JUMP_IF_FALSE_OR_POP", "UNPACK_SEQUENCE", "BUILD_SET_UNPACK", "JUMP_IF_TRUE_OR_POP", "UNARY_POSITIVE"],
	"1": ["GET_ANEXT", "UNPACK_EX", "LOAD_CLASSDEREF", "LOAD_CLOSURE", "LOAD_BUILD_CLASS", "IMPORT_FROM", "LOAD_FAST", "WITH_CLEANUP_START", "LOAD_DEREF", "DUP_TOP", "LOAD_CONST", "LOAD_NAME", "LOAD_GLOBAL", "FOR_ITER", "BEFORE_ASYNC_WITH"],
	"2": ["DUP_TOP_TWO"],
	"6": ["SETUP_ASYNC_WITH", "SETUP_EXCEPT", "SETUP_FINALLY"],
	"7": ["SETUP_WITH"]}'''
STACKDICT = '''{
	"-3": [60],
	"-2": [61, 95, 132, 141, 147],
	"-1": [1, 16, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 55, 56, 57, 59, 62, 63, 64, 65, 66, 67, 70, 72, 75, 76, 77, 78, 79, 82, 83, 84, 88, 90, 96, 97, 105, 107, 108, 114, 115, 125, 127, 130, 131, 133, 137, 142, 145, 146, 156],
	"0": [2, 3, 10, 11, 12, 15, 50, 68, 69, 73, 80, 85, 86, 87, 89, 91, 92, 98, 102, 103, 104, 106, 110, 111, 112, 113, 119, 120, 126, 138, 149, 150, 151, 152, 153, 155, 157, 158],
	"1": [4, 51, 52, 71, 81, 93, 94, 100, 101, 109, 116, 124, 135, 136, 148],
	"2": [5],
	"3": [],
	"6": [121, 122, 154],
	"7": [143]}'''


@return_as(dict)
def linestarts(code):
	if inspect.iscode(code):
		return dis.findlinestarts(code)


@return_as(set)
def labels(code):
	if inspect.iscode(code):
		return dis.findlabels(code.co_code)


def _compute_used_globals(func, table = None, co_consts = None, co_names = None):
	"""
	Compute the globals used by the function with the given
	bytecode table.
	"""
	import types
	d = {}
	if not co_consts:
		co_consts = func.__code__.co_consts
	if not co_names:
		co_names = func.__code__.co_names
	if not table:
		table = dis.get_instructions(func.__code__)
	
	if inspect.isfunction(func):
		globs = func.__globals__
	else:
		try:
			globs = vars(func)
		except TypeError:
			globs = dict()
			
	builtins = globs.get('__builtins__', __builtins__)
	if isinstance(builtins, types.ModuleType):
		builtins = builtins.__dict__
	# Look for LOAD_GLOBALs in the bytecode
	if isinstance(table, dict):
		table = table.values()
		
	for inst in table:
		if inst.opname == 'LOAD_GLOBAL':
			name = co_names[inst.arg]
			if name not in d:
				try:
					value = globs[name]
				except KeyError:
					value = builtins[name]
				d[name] = value
	# Add globals used by any nested code object
	for co in co_consts:
		if isinstance(co, types.CodeType):
			subtable = dis.get_instructions(co)
			d.update(_compute_used_globals(func, subtable, co.co_consts, co.co_names))
	return d



	


class ByteCodeInstruction(dis.Instruction):
	__fields__ = ('opname', 'opcode', 'arg', 'argval', 'argrepr', 'offset', 'starts_line', 'is_jump_target', 'lineno', 'next')
	_parent = None
	
	@property
	def next(self):
		return self.offset + 2
	
	@property
	def lineno(self):
		if self.starts_line:
			return self.starts_line
		return -1
	
	@lineno.setter
	def lineno(self, lineno):
		self.lineno = lineno
		
	def set_parent(self, parent):
		self._parent = parent
		
	def _todict(self):
		return (self.offset, self)
	

class Instructions(object):
	def __init__(self, codeobj):
		self.code = codeobj
		self.instructions = OrderedDict()
		self._processed = OrderedSet()
		
		
	def add_instruction(self, inst):
		if inst in self._processed:
			return
		else:
			item = ByteCodeInstruction._make(inst)
			item.set_parent(self.code)
			self.instructions[item.offset] = item
			self._processed.add(inst)


#fl.gi_frame.f_locals


#byte_increments = code.co_lnotab[0::2]
#line_increments = code.co_lnotab[1::2]

#todo add
def __dictiter__(obj):
	return ((inst.offset, inst) for inst in dis.get_instructions(obj))


def __iter__(self):
	co = self.codeobj
	self._linestarts
	_cell_names = co.co_cellvars + co.co_freevars
	consts = co.co_consts
	names = co.co_names
	firstline = co.co_firstlineno
	_line_offset = 0
	current_offset = self.current_offset
	#pp(list(C['co_lnotab']))
	
	return _get_instructions_bytes(co.co_code, co.co_varnames, co.co_names,
	                               co.co_consts, _cell_names,
	                               self._linestarts,
	                               line_offset=self._line_offset)


def _get_instructions_bytes(code, varnames=None, names=None, constants=None,
                            cells=None, #code.co_cellvars + code.co_freevars,
                            linestarts=None, line_offset=0):
	"""Iterate over the instructions in a bytecode string.
	Generates a sequence of Instruction namedtuples giving the details of each
	opcode.  Additional information about the code's runtime environment
	(e.g. variable names, constants) can be specified using optional
	arguments.
	"""
	
	if not linestarts:
		linestarts = linestarts(code)
	labels = findlabels(code)
	starts_line = None
	for offset, op, arg in dis._unpack_opargs(code):
		if linestarts is not None:
			starts_line = linestarts.get(offset, None)
			if starts_line is not None:
				starts_line += line_offset
		is_jump_target = offset in labels
		argval = None
		argrepr = ''
		if arg is not None:
			#  Set argval to the dereferenced value of the argument when
			#  available, and argrepr to the string representation of argval.
			#    _disassemble_bytes needs the string repr of the
			#    raw name index for LOAD_GLOBAL, LOAD_CONST, etc.
			argval = arg
			
			if op in dis.hasconst:
				argval, argrepr = dis._get_const_info(arg, constants)
			elif op in dis.hasname:
				argval, argrepr = dis._get_name_info(arg, names)
			elif op in dis.hasjrel:
				argval = offset + 2 + arg
				argrepr = "to " + repr(argval)
				
			elif op in dict([(op, opcode.opname.__getitem__(op)) for op in dis.haslocal]):
				argval, argrepr = dis._get_name_info(arg, varnames)
				
			elif op in dict([(op, opcode.opname.__getitem__(op)) for op in dis.hascompare]):
				argval = dis.cmp_op[arg]
				argrepr = argval
				#name =
				
			elif op in dict([(op, opcode.opname.__getitem__(op)) for op in dis.hasfree]):
				argval, argrepr = dis._get_name_info(arg, cells)
			
			elif op == dis.FORMAT_VALUE:
				argval = ((None, str, repr, ascii)[arg & 0x3], bool(arg & 0x4))
				argrepr = ('', 'str', 'repr', 'ascii')[arg & 0x3]
				if argval[1]:
					if argrepr:
						argrepr += ', '
					argrepr += 'with format'
		yield Instruction(opname[op], op, arg, argval, argrepr, offset, starts_line, is_jump_target)



class _ByteCodeInst(bytecode.ByteCodeInst):
	#slots =('offset', 'next', 'opcode', 'opname', 'arg', 'lineno')
	_argval = None
	_prev = None
	_iter = None
	_stack = None
	
	def argval(self, ): pass
	
	def __init__(self, offset, opcode, arg, nextoffset):
		super(ByteCodeInst, self).__init__(offset, opcode, arg, nextoffset)
		self.offset = offset
		self.next = nextoffset
		self.opcode = opcode
		self.opname = dis.opname[opcode]
		self.arg = arg
		self.lineno = -1  # unknown line number


class ByteCodeIter(object):
	def __init__(self, code):
		from numba.bytecode import _unpack_opargs
		self.code = code
		self.iter = iter(bytecode._unpack_opargs(self.code.co_code))
	
	def __iter__(self):
		return self
	
	def _fetch_opcode(self):
		return next(self.iter)
	
	def next(self):
		from numba.bytecode import ByteCodeInst
		offset, opcode, arg, nextoffset = self._fetch_opcode()
		return offset, ByteCodeInst(offset=offset, opcode=opcode, arg=arg, nextoffset=nextoffset)
	
	__next__ = next
	
	def read_arg(self, size):
		buf = 0
		for i in range(size):
			_offset, byte = next(self.iter)
			buf |= byte << (8 * i)
		return buf


def bytecode_table(co):
	return OrderedDict(bytecode.ByteCodeIter(co))


class CodeIter(dict):
	def __init__(self, obj):
		import types
		self.obj = obj
		if isinstance(obj, types.CodeType):
			self.code = obj
		else:
			self.code = b''
		
		self.table = bytecode_table(self.code)
	
	def compute_table(self, code):
		return bytecode_table(code)
	
	def bytecode(self, code):
		if inspect.iscode(code):
			return bytecode.ByteCodeIter(code)
	
	def byte(self, code):
		if inspect.iscode(code):
			table = bytecode.OrderedDict(bytecode.ByteCodeIter(code))
		# self._compute_lineno(table, code)
	
	def find_global(self, inst):
		if inst.opname == 'LOAD_GLOBAL':
			name = co_names[inst.arg]
	
	@classmethod
	def _compute_lineno(cls, table, code):
		"""
		Compute the line numbers for all bytecode instructions.
		"""
		for offset, lineno in dis.findlinestarts(code):
			if offset in table:
				table[offset].lineno = lineno
		known = -1
		for inst in table.values():
			if inst.lineno >= 0:
				known = inst.lineno
			else:
				inst.lineno = known
		return table
	
	def make_table(self, code):
		pass


class PeekableIterator(object):
	"""
	An iterator which wraps any iterable and makes it possible to peek to see
	what's the next item.
	"""
	
	def __init__(self, iterable):
		# type: (Iterable) -> None
		from collections import deque
		self.remaining = deque()  # type: deque
		self._iterator = iter(iterable)
		self._position = 0
	
	def __iter__(self):
		# type: () -> PeekableIterator
		return self
	
	def __next__(self):
		# type: () -> Any
		"""Return the next item from the iterator."""
		if self.remaining:
			return self.remaining.popleft()
		return next(self._iterator)
	
	next = __next__  # Python 2 compatibility
	
	def push(self, item):
		# type: (Any) -> None
		"""Push the `item` on the internal stack, it will be returned on the
		next :meth:`next` call.
		"""
		self.remaining.append(item)
	
	def peek(self):
		# type: () -> Any
		"""Return the next item without changing the state of the iterator."""
		item = next(self)  # type: ignore
		self.push(item)
		return item
	
	def previous(self):
		p = self._position
		if p >= len(self):
			raise StopIteration
		elif p < 0:
			raise TypeError
		self._position = p = p - 1
		return self[p:p + 1]
	
	def setPosition(self, position):
		if self._position >= len(self):
			raise StopIteration
		self._position = position
	
	def getPosition(self):
		if self._position >= len(self):
			raise StopIteration
		if self._position >= 0:
			return self._position
		else:
			return None
	
	def skip(self, chars=None):
		"""Skip past a list of characters"""
		p = self.position  # use property for the error-checking
		while p < len(self):
			c = self[p:p + 1]
			if c not in chars:
				self._position = p
				return c
			p += 1
		self._position = p
		return None
	
	def skipUntil(self, chars):
		p = self.position
		while p < len(self):
			c = self[p:p + 1]
			if c in chars:
				self._position = p
				return c
			p += 1
		self._position = p
		return None


class Peekable(object):
	"""Iterator that supports peeking at the next item in the iterable."""
	
	def __init__(self, iterable):
		from collections import deque
		
		if inspect.isgenerator(iterable):
			self.iterator = iterable
		else:
			self.iterator = iter(iterable)
		self.item = None
		self._peeked = deque()
		self._seen = OrderedSet()
		
	def add(self, item):
		if item not in self._seen:
			self._seen.add(item)
	
	@property
	def _position(self):
		return len(self._peeked)
	
	@property
	def _current_offset(self):
		if self._peeked:
			return self._peeked[-1].offset
		return 0
		
	def push(self, item):
		if item not in self._peeked:
			self._peeked.append(item)
	
	def peek(self):
		"""Get the next item in the iterable without advancing our position."""
		if (not self.item):
			try:
				self.item = next(self.iterator)
				self.push(self.item)
				self.add(self.item)
			except StopIteration:
				return None
		return self.item
	
	def __next__(self):
		"""Get the next item in the iterable and advance our position."""
		item = self.peek()
		self.add(item)
		self.item = None
		return item
	
	

def peek(seq):
	""" Retrieve the next element of a sequence

	Returns the first element and an iterable equivalent to the original
	sequence, still having the element retrieved.

	>>> seq = [0, 1, 2, 3, 4]
	>>> first, seq = peek(seq)
	>>> first
	0
	>>> list(seq)
	[0, 1, 2, 3, 4]
	"""
	import itertools
	iterator = iter(seq)
	first = next(iterator)
	second = next(iterator)
	return first, second, itertools.chain([first, second], iterator)

#scan_code

scan_opcodes = lazyimport('modulefinder.ModuleFinder').scan_opcodes

#ensure_fromlist


#logging.root.setLevel(logging.DEBUG)
#bytecode.FunctionIdentity.from_function
#bytecode.ByteCode
#ByteCodeInst
#ByteCodeIter
#_ScanCode in _LoadModule,

"""
DEBUG:root:Adding module [importpy.isort] [PY_SOURCE]
DEBUG:root:Adding module [importpy] [PKG_DIRECTORY]
DEBUG:root:Adding module [importpy.tools] [PY_SOURCE]
DEBUG:root:Adding module [importpy.tools] [PKG_DIRECTORY]
DEBUG:root:Adding module [importpy.tools.codetools] [PY_SOURCE]
"""

def stack_effects(opcode, oparg=None):
	return opcode.stack_effect(opcode=opcode, oparg=oparg)


def stack_table(d):
	from collections import OrderedDict, defaultdict
	stacks = defaultdict(set)
	stack_names = defaultdict(set)
	for k,v in d.items():
		try:
			stack = opcode.stack_effect(k)
			stacks[stack].add(k)
			stack_names[stack].add(v)
		except ValueError:
			try:
				stack = opcode.stack_effect(k, 0)
				stacks[stack].add(k)
				stack_names[stack].add(v)
			except ValueError:
				pass
				
	
	return stacks,stack_names

def opmap_reversed():
	return {v:k for k,v in opcode.opmap.items()}

def opcode_to_opname(seq):
	lst = []
	for s in seq:
		c = opcode.opname[s]
		if c is not None:
			lst.append(c)
	return lst

def is_poptop(item):
	if isinstance(item, str):
		return item == 'POP_TOP'
	elif isinstance(item, int):
		return item == 1
	elif isinstance(item, dis.Instruction):
		return item.opname == 'POP_TOP'


def _unpack_opargs(code):
	extended_arg = 0
	for i in range(0, len(code), 2):
		op = code[i]
		if op >= opcode.HAVE_ARGUMENT:
			arg = code[i + 1] | extended_arg
			extended_arg = (arg << 8) if op == opcode.EXTENDED_ARG else 0
		else:
			arg = None
		yield (i, op, arg)


def _scancode(co):
	import opcode
	arguments = []
	args = []
	opmap = opcode.opmap.copy()
	importedModule = None
	topLevel = True
	STORE_OPS = (90, 97)
	
	for opindex, op, oparg in dis._unpack_opargs(co.co_code):
		opname = opcode.opname[op]
		print(opindex, op, opname, oparg)
		
		if op >= dis.HAVE_ARGUMENT:
			if op in dis.hasconst:
				arg = [code.co_consts[oparg]]
				print('hasconst')
			elif op in dis.hasname:
				arg = [code.co_names[oparg]]
				print('hasname')
			elif op in dis.hasjrel:
				arg = [i + oparg]
				print('hasjrel')
			elif op in dis.haslocal:
				arg = [code.co_varnames[oparg]]
				print('haslocal')
			elif op in dis.hascompare:
				arg = [dis.cmp_op[oparg]]
				print(op, 'hascompare')
			elif op in dis.hasfree:
				arg = [free[oparg]]
				print(op, 'hasfree')
			else:
				arg = [oparg]
			args.append(arg)
			print('arg', arg)
		
		if op == opmap.get('LOAD_CONST'):
			arguments.append(co.co_consts[oparg])
			print('LOAD_CONST -> {}'.format(co.co_consts[oparg]))
			continue
		
		elif op == opmap.get('IMPORT_NAME'):
			name = co.co_names[oparg]
			print('IMPORT_NAME ->' + name)
			if len(arguments) >= 2:
				relativeImportIndex, fromList = arguments[-2:]
			else:
				relativeImportIndex = -1
				#fromList, = arguments
				fromList = arguments[0] if arguments else []
		
		elif op == opmap.get('IMPORT_STAR') and topLevel and importedModule is not None:
			pass
			
		elif topLevel and op in STORE_OPS:
			name = co.co_names[oparg]
			arguments.append(name)
		
			
	return arguments
			
			
		
#_AddBaseModules
#_AddModule
#_DetermineParent
#_FindModule
#_GetParentByName
#_ImportAllSubModules
#_ImportDeferredImports
#_ImportModule
#_InternalImportModule
#_LoadModule
#_LoadPackage
#_ReplacePathsInCode
#_ScanCode

#MF._GetParentByName('xml.parsers')
#source(MF._InternalImportModule)
#fp, path, info = self._FindModule(searchName, path, namespace)

def _FindModule(name, path, namespace):
	import imp
	import sys
	try:
		# imp loads normal modules from the filesystem
		return imp.find_module(name, path)
	except ImportError:
		if namespace and name in sys.modules:
			# Namespace package (?)
			module = sys.modules[name]
			info = ("", "", imp.PKG_DIRECTORY)
			return None, list(module.__path__)[0], info

#_ScanCode

#importedModule = self._ImportModule(name, deferredImports, module, relativeImportIndex)

#pos = name.rfind(".")
#searchName = name[pos + 1:]
#parentName = name[:pos]
#fp, path, info = self._FindModule(searchName, path, namespace)
#module = self._LoadModule(name, fp, path, info, deferredImports, parentModule, namespace)


#arg=113, argval='main'
#_as_opcodes

#BB._compute_used_globals(BB.func_id.func, BB.table, BB.co_consts, BB.co_names)

#table.values()


#'LOAD_CONST' (const)-> 'MAKE_FUNCTION' -> 'STORE_NAME' (names)

# 'LOAD_CONST' -> 'LOAD_CONST'

#IMPORT_NAME -> IMPORT_FROM --> STORE_NAME

#IMPORT_FROM --> STORE_NAME (names)

#LOAD_CONST ->


def get_used_globals(self):
	"""
	Get a {name: value} map of the globals used by this code
	object and any nested code objects.
	"""
	return self._compute_used_globals(self.func_id.func, self.table,
	                                  self.co_consts, self.co_names)


class OpByteCode(object):
	"""
	The decoded bytecode of a function, and related information.
	"""
	__slots__ = ('func_id', 'co_names', 'co_varnames', 'co_consts', 'co_cellvars', 'co_freevars', 'table', 'labels')
	
	def __init__(self, func_id):
		if not hasattr(func_id, 'code'):
			code =  func_id
			self.func_id = code.co_name
		else:
			code = func_id.code
			self.func_id = func_id
		
		self.func_id = func_id
		labels = set(dis.findlabels(code.co_code))
		labels.add(0)
		# A map of {offset: ByteCodeInst}
		table = OrderedDict(bytecode.ByteCodeIter(code))
		self._compute_lineno(table, code)
		self.co_names = code.co_names
		self.co_varnames = code.co_varnames
		self.co_consts = code.co_consts
		self.co_cellvars = code.co_cellvars
		self.co_freevars = code.co_freevars
		self.table = table
		self.labels = sorted(labels)
	
	@classmethod
	def _compute_lineno(cls, table, code):
		"""
		Compute the line numbers for all bytecode instructions.
		"""
		for offset, lineno in dis.findlinestarts(code):
			if offset in table:
				table[offset].lineno = lineno
		known = -1
		for inst in table.values():
			if inst.lineno >= 0:
				known = inst.lineno
			else:
				inst.lineno = known
		return table
	
	def __iter__(self):
		return utils.itervalues(self.table)
	
	def __getitem__(self, offset):
		return self.table[offset]
	
	def __contains__(self, offset):
		return offset in self.table
	
	def dump(self):
		def label_marker(i):
			if i[1].offset in self.labels:
				return '>'
			else:
				return ' '
		
		return '\n'.join('%s %10s\t%s' % ((label_marker(i),) + i) for i in self.table.items())
	
	@classmethod
	def _compute_used_globals(cls, func, table = None, co_consts = None, co_names = None):
		"""
		Compute the globals used by the function with the given
		bytecode table.
		"""
		import types
		import numba.utils
		from collections import OrderedDict
		
		if not co_names:
			co_names = func.__code__.co_names
		if not co_consts:
			co_consts = func.__code__.co_consts
		if not table:
			table = OrderedDict(bytecode.ByteCodeIter(func.__code__))
			print('table')
		d = {}
		globs = getattr(func, '__globals__',dict())
		builtins = globs.get('__builtins__', numba.utils.builtins)
		if isinstance(builtins, types.ModuleType):
			builtins = builtins.__dict__
		# Look for LOAD_GLOBALs in the bytecode
		for inst in table.values():
			if inst.opname == 'LOAD_GLOBAL':
				name = co_names[inst.arg]
				if name not in d:
					try:
						value = globs[name]
					except KeyError:
						value = builtins.get(name, None)
					d[name] = value
		# Add globals used by any nested code object
		for co in co_consts:
			if isinstance(co, types.CodeType):
				subtable = OrderedDict(bytecode.ByteCodeIter(co))
				d.update(cls._compute_used_globals(func, subtable, co.co_consts, co.co_names))
		return d
	
	def get_used_globals(self):
		"""
		Get a {name: value} map of the globals used by this code
		object and any nested code objects.
		"""
		return self._compute_used_globals(self.func_id.func, self.table,  self.co_consts, self.co_names) #todo change!





class ByteCodeIter(object):
	def __init__(self, code):
		from numba.bytecode import _unpack_opargs
		self.code = code
		self.iter = iter(_unpack_opargs(self.code.co_code))
	
	def __iter__(self):
		return self
	
	def _fetch_opcode(self):
		return next(self.iter)
	
	def next(self):
		from numba.bytecode import ByteCodeInst
		offset, opcode, arg, nextoffset = self._fetch_opcode()
		return offset, ByteCodeInst(offset=offset, opcode=opcode, arg=arg, nextoffset=nextoffset)
	
	__next__ = next
	
	def read_arg(self, size):
		buf = 0
		for i in range(size):
			_offset, byte = next(self.iter)
			buf |= byte << (8 * i)
		return buf


###
if __name__ == '__main__': print(__file__)