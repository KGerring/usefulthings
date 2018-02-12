#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = whoosh_info
# author= KGerring
# date = 2/10/18
# from startups import *
""" 


"""
from __future__ import absolute_import, unicode_literals # isort:skip
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

subpacks = ['whoosh.analysis',
            'whoosh.automata',
            'whoosh.codec',
            'whoosh.filedb',
            'whoosh.lang',
            'whoosh.lang.snowball',
            'whoosh.matching',
            'whoosh.qparser',
            'whoosh.query',
            'whoosh.support',
            'whoosh.util']
files = ['whoosh.analysis.acore',
         'whoosh.analysis.analyzers',
         'whoosh.analysis.filters',
         'whoosh.analysis.intraword',
         'whoosh.analysis.morph',
         'whoosh.analysis.ngrams',
         'whoosh.analysis.tokenizers',
         'whoosh.automata.fsa',
         'whoosh.automata.glob',
         'whoosh.automata.lev',
         'whoosh.automata.nfa',
         'whoosh.automata.reg',
         'whoosh.classify',
         'whoosh.codec.base',
         'whoosh.codec.memory',
         'whoosh.codec.plaintext',
         'whoosh.codec.whoosh3',
         'whoosh.collectors',
         'whoosh.columns',
         'whoosh.compat',
         'whoosh.externalsort',
         'whoosh.fields',
         'whoosh.filedb.compound',
         'whoosh.filedb.filestore',
         'whoosh.filedb.filetables',
         'whoosh.filedb.gae',
         'whoosh.filedb.structfile',
         'whoosh.formats',
         'whoosh.highlight',
         'whoosh.idsets',
         'whoosh.index',
         'whoosh.lang.dmetaphone',
         'whoosh.lang.isri',
         'whoosh.lang.lovins',
         'whoosh.lang.morph_en',
         'whoosh.lang.paicehusk',
         'whoosh.lang.phonetic',
         'whoosh.lang.porter',
         'whoosh.lang.porter2',
         'whoosh.lang.snowball.bases',
         'whoosh.lang.snowball.danish',
         'whoosh.lang.snowball.dutch',
         'whoosh.lang.snowball.english',
         'whoosh.lang.snowball.finnish',
         'whoosh.lang.snowball.french',
         'whoosh.lang.snowball.german',
         'whoosh.lang.snowball.hungarian',
         'whoosh.lang.snowball.italian',
         'whoosh.lang.snowball.norwegian',
         'whoosh.lang.snowball.portugese',
         'whoosh.lang.snowball.romanian',
         'whoosh.lang.snowball.russian',
         'whoosh.lang.snowball.spanish',
         'whoosh.lang.snowball.swedish',
         'whoosh.lang.stopwords',
         'whoosh.lang.wordnet',
         'whoosh.legacy',
         'whoosh.matching.binary',
         'whoosh.matching.combo',
         'whoosh.matching.mcore',
         'whoosh.matching.wrappers',
         'whoosh.multiproc',
         'whoosh.qparser.common',
         'whoosh.qparser.dateparse',
         'whoosh.qparser.default',
         'whoosh.qparser.plugins',
         'whoosh.qparser.syntax',
         'whoosh.qparser.taggers',
         'whoosh.query.compound',
         'whoosh.query.nested',
         'whoosh.query.positional',
         'whoosh.query.qcolumns',
         'whoosh.query.qcore',
         'whoosh.query.ranges',
         'whoosh.query.spans',
         'whoosh.query.terms',
         'whoosh.query.wrappers',
         'whoosh.reading',
         'whoosh.scoring',
         'whoosh.searching',
         'whoosh.sorting',
         'whoosh.spelling',
         'whoosh.support.base85',
         'whoosh.support.bench',
         'whoosh.support.charset',
         'whoosh.support.levenshtein',
         'whoosh.support.relativedelta',
         'whoosh.support.unicode',
         'whoosh.system',
         'whoosh.util.cache',
         'whoosh.util.filelock',
         'whoosh.util.loading',
         'whoosh.util.numeric',
         'whoosh.util.numlists',
         'whoosh.util.testing',
         'whoosh.util.text',
         'whoosh.util.times',
         'whoosh.util.varints',
         'whoosh.util.versions',
         'whoosh.writing']


from whoosh.index import create_in, open_dir, FileIndex, Index
from whoosh.fields import *
from whoosh.qparser import QueryParser, to_word, RegexTagger, NotGroup, OrGroup, AndGroup, AndNotGroup, AndMaybeGroup
from whoosh.query import *
from whoosh.analysis import Filter
import whoosh.qparser
import whoosh.qparser.default
import whoosh.multiproc
import whoosh.matching.wrappers, whoosh.matching.mcore
import whoosh.analysis.acore, whoosh.analysis.analyzers, whoosh.analysis.filters
import whoosh.index, whoosh.idsets, whoosh.formats, whoosh.filedb, whoosh.codec.whoosh3

from whoosh.fields import (merge_fielddict, merge_schema, merge_schemas, ensure_schema, UnknownFieldError,
                           SchemaClass, Schema, BOOLEAN, COLUMN, FieldType, ID, IDLIST, KEYWORD, NUMERIC,
                           STORED, TEXT)

from whoosh.qparser import SimpleParser, QueryParser, MultifieldParser, RegexTagger

from whoosh.query import Wildcard, TermRange, Term, Span, Regex, Sequence, Require, Query, Prefix, Not, Or, And, AndMaybe, AndNot
from whoosh.analysis import RegexAnalyzer

from  whoosh.analysis import PathTokenizer
import whoosh.qparser.common
import whoosh.qparser.dateparse
import whoosh.query.qcore
from whoosh.query.positional import Phrase
from whoosh.qparser.syntax  import AndGroup
import whoosh.query.terms
from whoosh.sorting import add_sortable, FieldFacet
from whoosh.index import LockError


"""writer.add_document(title=u"Title to be indexed", _stored_title=u"Stored title")

with ix.searcher() as searcher:
	searcher = ix.searcher()
	stored_fields = searcher.stored_fields(docnum)

	
parser = QueryParser("content", ix.schema)
myquery = parser.parse(querystring)
print(parser.parse(u"render OR (title:shade keyword:animate)"))
print(parser.parse(u"*end*"))

_stored_<fieldname>, add_field,_read_toc,_reader,_segments, remove_field

__slotnames__, _dyn_fields, _fields, _subfields, items, names

"""


class InfoSchema(SchemaClass):
	objectID = ID(stored=True, unique= True, sortable=True)
	args = KEYWORD(commas=True, stored=True, scorable=True)
	base_class = TEXT(stored=True)
	docstring = TEXT(stored=True)
	definition = TEXT(stored=True)
	file = ID(stored=True)
	fullname = TEXT(field_boost=2.0, stored=True, sortable = True, phrase=False)
	module = TEXT(stored=True)
	name = TEXT(stored=True)
	package = TEXT(stored=True)
	signature = TEXT(stored=True)
	source = TEXT(stored=True)
	string_form = TEXT(stored=True)
	tags = KEYWORD(stored=True)
	type_name = TEXT(stored=True)
	date_created = DATETIME
	
	#writer.commit(optimize=True)
	#add("*_id", fields.ID, glob=True)
	#D.parse_query('date', '2018-01-12')


def search(searcher):
	terms = True
	scored = False

F = whoosh.formats.Frequency

from whoosh.formats import CharacterBoosts, Characters, Existence, Format, Frequency, PositionBoosts, Positions

FORMATS = [CharacterBoosts, Characters, Existence, Format, Frequency, PositionBoosts, Positions]


	
#RegexTokenizer, 	RegexAnalyzer,KeywordAnalyzer,CompositeAnalyzer,CommaSeparatedTokenizer, Tokenizer
#_terms, _segment, _gen, most_frequent_terms, most_distinctive_terms, lexicon,iter_field,frequency
#._terms._fieldmap
	
EXTEXT = TEXT(field_boost=2.0, stored = True, sortable=True)

#search
#searcher.lexicon('fullname')
"""analyzer = format = scorable = stored = unique = vector = None
    indexed = True
    multitoken_query = "default"
    sortable_typecode = None
    column_type = None
    
    searcher.all_stored_fields()
    
    
    """#unique


META = whoosh.fields.MetaSchema
#class SchemaClass(with_metaclass(MetaSchema, Schema)):
	#def __new__(cls, *args, **kwargs):
		#obj = super(Schema, cls).__new__(Schema)
		#kw = getattr(cls, "_clsfields", {})
		#kw.update(kwargs)
		#obj.__init__(*args, **kw)
		#return obj
		



def searcher_documents(searcher):
	return list(searcher.documents())

	




if __name__ == '__main__': print(__file__)