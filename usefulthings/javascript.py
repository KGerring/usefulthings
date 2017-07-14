#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = javascript
# author=SluttyScience
# date = 7/13/17
from startups import *
import sys, os
from pygments.lexers.javascript import JavascriptLexer
import re, regex
import pygments.token
from pygments.token import string_to_tokentype, Token, is_token_subtype, STANDARD_TYPES

STANDARD = {v:k for k,v in STANDARD_TYPES.items()}


class PeekableIterator(object):
	'Iterator that supports peeking at the next item in the iterable.'
	
	def __init__(self, iterable):
		self.iterator = iter(iterable)
		self.item = None
	
	def peek(self):
		'Get the next item in the iterable without advancing our position.'
		if (not self.item):
			try:
				self.item = next(self.iterator)
			except StopIteration:
				return None
		return self.item
	
	def __next__(self):
		'Get the next item in the iterable and advance our position.'
		item = self.peek()
		self.item = None
		return item


declaration = string_to_tokentype('Declaration')
other = string_to_tokentype('Other')
punctuation = string_to_tokentype('Punctuation')

Double = r'"(\\\\\\\\|\\\\"|[^"])*"'
Single= r"'(\\\\\\\\|\\\\'|[^'])*'"
BUILTIN = regex.compile(r'(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|Promise|Proxy|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|isSafeInteger|parseFloat|parseInt|document|this|window)\b')
CONSTANT = regex.compile(r'(true|false|null|NaN|Infinity|undefined)\b')
RESERVED = regex.compile(r'(abstract|boolean|byte|char|class|const|debugger|double|enum|export|extends|final|float|goto|implements|import|int|interface|long|native|package|private|protected|public|short|static|super|synchronized|throws|transient|volatile)\b')
DECLARATION = regex.compile(r'(var|let|with|function)\b')
KEYWORD = regex.compile(r'(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|yield|this|of)\b')
OP = regex.compile(r'\+\+|--|~|&&|\?|:|\\|\||\\\\(?=\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?')

#NodeTest.NAMETESTANY
#2 == /*Node.ATTRIBUTE_NODE*/
comment = "comment"

ELEMENT_NODE =1
ATTRIBUTE_NODE = 2
TEXT_NODE = 3
CDATA_SECTION_NODE = 4
PROCESSING_INSTRUCTION_NODE = 7
COMMENT_NODE = 8
DOCUMENT_NODE = 9
DOCUMENT_FRAGMENT = 11
XML_NAMESPACE_URI = "http://www.w3.org/XML/1998/namespace"
XMLNS_NAMESPACE_URI = "http://www.w3.org/2000/xmlns/"
XPATH_NAMESPACE_NODE = ''
#XPATH_NAMESPACE_NODE

#NAMETESTPREFIXANY
NAMETESTRESOLVEDANY = "{" + "this.value" + "}*"
NAMETESTANY = 0
NAMETESTPREFIXANY = 1
NAMETESTQNAME = 2
COMMENT = 3 #"comment()"
TEXT = 4 #"text()"
PI = 5 #"processing-instruction()"
NODE = 6 #"node()"

AXISPT = regex.compile(r'(?:::)')

class NodeTest(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
		
#FunctionResolver
#XNumber
#XBoolean
#Operators.equals
numberFormat = regex.compile(r'^\s*-?[0-9]*\.?[0-9]+\s*$')

#XNodeSet
ids = regex.compile(r'[\x0d\x0a\x09\x20]+')
'n.localName | baseName | target | nodeName'

ANY_TYPE = 0;
NUMBER_TYPE = 1;
STRING_TYPE = 2;
BOOLEAN_TYPE = 3;
UNORDERED_NODE_ITERATOR_TYPE = 4;
ORDERED_NODE_ITERATOR_TYPE = 5;
UNORDERED_NODE_SNAPSHOT_TYPE = 6;
ORDERED_NODE_SNAPSHOT_TYPE = 7;
ANY_UNORDERED_NODE_TYPE = 8;
FIRST_ORDERED_NODE_TYPE = 9;

#STEP('ancestor')
SPLITPATH =regex.compile(r'^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$')
EXP =regex.compile(r'[eEsSfFdDlL]')
ELEMENT= regex.compile(r'^([#.]?)([a-z0-9\\*_-]*)((\|)([a-z0-9\\*_-]*))?')
ATTR = regex.compile(r'^\[([^\]]*)\]')
ATTV = regex.compile(r'^\[\s*([^~=\s]+)\s*(~?=)\s*"([^"]+)"\s*\]')
PSEUDO = regex.compile(r'^:([a-z_-])+')
COMBINATOR = regex.compile(r'^(\s*[>+\s])?')
COMMA = regex.compile(r'^\s*,')
if __name__ == '__main__': print(__file__)