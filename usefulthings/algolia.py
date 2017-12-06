#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = algolia
# author=SluttyScience
# author_email='KGerring@gmail.com'
# date = 11/10/17
""" filename = algolia"""
from __future__ import absolute_import, unicode_literals
from startups import *
import sys, os
import regex


from startups.helpers.third_party import get_algolia

algolia, client = get_algolia()

def examples():
	p = algolia.Index(client, 'pypi')
	ex = p.search_for_facet_values('requires-dist', 'requests')


def get_algolia_values():
	from startups.helpers.third_party import get_keychain
	key = get_keychain()
	key.generate_parsers()
	if key._new_parser is not None:
		return key._new_parser.items('algolia')

#'/1/indexes/pypi/settings?getVersion=2'
#r = t.req(False, '/1/indexes/pypi/settings?getVersion=2', 'GET', params={}, data={}, request_options = None)
#r = t._session_req('AG163LOZ6M.algolia.net', path='/1/indexes/pypi/settings?getVersion=2', meth='GET',
#                   timeout=t.timeout, params={}, data={}, headers=headers)
#
#r = cl._transport.session.request('GET', url='https://AG163LOZ6M.algolia.net/1/indexes/pypi/settings?getVersion=2',
#                                  timeout=t.timeout, headers=headers, params={}, data={})
#
def get_logs(client, offset=0, length=10, type='all', request_options=None):
	"""
	onlyErrors
	:param client:
	:param offset:
	:param length:
	:param type: `all` is default, `query`, `build`, `error`
		query: Retrieve only the queries.
		build: Retrieve only the build operations.
		error: Retrieve only the errors (same as onlyErrors parameters)
	:param request_options:
	:return:
	"""
	return client.get_logs(offset=offset, length=length, type=type, request_options=request_options)




#req
#'is_search', 'path', 'meth', 'params', and 'data'

# mm = ac.init_index('mdfind')
# mm.get_object('26902241')
# sr = mm.search('date')
# hits = sr.get('nbHits')
BLUE = '\x1b[34m{0}\x1b[0m'
EM_REGEX = regex.compile("r<em>[^<]*</em>")

#'/1/indexes/pypi'

#SSL_CERTIFICATE_DOMAIN

#regex.findall('\-\s*\w+\:', d)
"""- attributesToHighlight: a string that contains the list of
                attributes you want to highlight according to the query.
                Attributes are separated by a comma. You can also use a string
                array encoding (for example ['name','address']). If an
                attribute has no match for the query, the raw value is returned.
                By default all indexed text attributes are highlighted. You
                can use `*` if you want to highlight all textual attributes.
                Numerical attributes are not highlighted. A matchLevel is
                returned for each highlighted attribute and can contain:
                    - full: if all the query terms were found in the attribute,
                    - partial: if only some of the query terms were found,
                    - none: if none of the query terms were found.
                    
                attributesToSnippet: ['name:10','content:10'])
minWordSizefor1Typo = 3
minWordSizefor2Typos=7
_rankingInfo
getRankingInfo=1,

numericFilters
Supported operands are `<`, `<=`, `=`, `>` and `>=`


- tagFilters: filter the query by a set of tags. You can AND
                tags by separating them by commas. To OR tags, you must add
                parentheses. For example, tags=tag1,(tag2,tag3) means
                tag1 AND (tag2 OR tag3). You can also use a string array encoding,
                for example tagFilters: ['tag1',['tag2','tag3']] means
                tag1 AND (tag2 OR tag3). At indexing, tags should be added in
                the _tags** attribute of objects (for example
                {'_tags':['tag1','tag2']}).

 At indexing, tags should be added in
                the _tags** attribute of objects (for example
                {'_tags':['tag1','tag2']}).

- facetFilters: filter the query by a list of facets. Facets
                are separated by commas and each facet is encoded as
                `attributeName:value`. For example:
                `facetFilters=category:Book,author:John%20Doe`. You can also
                use a string array encoding (for example

                
"""
S= dict(page=0, hitsPerPage=20, attributesToRetrieve="*"

class SearchResult(object):
	KEYS = ['hits', 'nbHits', 'page', 'nbPages', 'hitsPerPage', 'processingTimeMS', 'exhaustiveNbHits', 'query',
	        'params']
	def __init__(self, _data):
		self._data = _data
		self.nbHits = _data.get('nbHits', 0)
		self.page = _data.get('page', 0)
		self.nbPages = _data.get('nbPages')
		self.hitsPerPage = _data.get('hitsPerPage')
		self.query = _data.get('query')
		self._params = _data.get('params')
		self.exhaustiveNbHits = _data.get('exhaustiveNbHits')
		self._hits = _data.get('hits')
		
	def clean_params(self):
		from urllib.parse import unquote
		params = [param.split('=',1) for param in unquote(self._params).split('&')]
		
		
	

class Hit(object):
	def __init__(self, _data):
		self._data = _data
		self.objectID = _data.get('objectID')
		self._highlightResult = _data.get('_highlightResult')
		
		

class IndexSettings(object):
	def __init__(self, _data):
		self._data = _data
		
	@property
	def attributesForFaceting(self):
		"""
		searchable() and filterOnly()
		:return:
		"""
		return self._data.get('attributesForFaceting')
	
	@property
	def searchableAttributes(self):
		"""
		The order in which attributes are listed defines their ranking priority:
		matches in attributes at the beginning of the list will be considered more important
		than matches in attributes further down the list.
		To assign the same priority to several attributes, pass them within the same string, separated by commas
		Within a given attribute, matches near the beginning of the text are considered more important than matches near the end. You can disable this behavior by
		wrapping your attribute name inside an `unordered()`
		
		:return:
		"""
		return self._data.get('searchableAttributes')
	
	@property
	def unretrievableAttributes(self):
		"""List of attributes that cannot be retrieved at query time.
		These attributes can still be used for indexing and/or ranking."""
		return self._data.get('unretrievableAttributes')
	
	@property
	def attributesToRetrieve(self):
		"""Make all attributes as retrievable by default
		index.set_settings({'attributesToRetrieve': ['*']})
		"""
		return self._data.get('attributesToRetrieve', '*')

if __name__ == '__main__': print(__file__)