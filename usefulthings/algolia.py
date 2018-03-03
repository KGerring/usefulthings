#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = algolia
# author=KGerring
# author_email='KGerring@gmail.com'
# date = 11/10/17
""" filename = algolia"""
from __future__ import absolute_import, unicode_literals # isort:skip
from startups import *
from startups.settings import LoggerManager
import sys, os
import regex
from addict import Dict
from urllib.parse import urlencode
from algoliasearch.helpers import urlify, CustomJSONEncoder
from algoliasearch.index import IndexIterator, Index
from algoliasearch.transport import Transport, HTTPAdapter, Session
from algoliasearch.client import Client, RequestOptions
import startups.helpers._ipython.info
from startups.helpers.third_party import get_algolia
from werkzeug.datastructures import (CombinedMultiDict, MultiDict)
from IPython.utils.ipstruct import Struct

logger_manager = LoggerManager(__name__)
logger = getattr(logger_manager, "base_logger", None)


INSTANT_SEARCH = '/Users/kristen/PycharmProjects/instantsearch.js'

algolia, client = get_algolia()

#'https://ag163loz6m.algolia.net/1/indexes/pypi/settings?getVersion=2'
HEADERS = {'X-Algolia-Application-Id': '', 'X-Algolia-API-Key': ''}
SEARCH_ONLY = '2067cb9414d100f6ab8a0e8283a4be0b'


RULES = []

def __req():
	def _session_req(self, host, path, meth, timeout, params, data, headers):
		url = 'https://%s%s' % (host, path)
		res = self.session.request(
				meth, url, params=params, data=data, timeout=timeout,
				headers=headers)
		
		

_multiple_queries = """
queries, index_name_key='indexName', strategy='none', request_options=None
"""


#list_clusters

def __get_transport_headers(transport):
	self._transport.headers = {
		'X-Algolia-Application-Id': app_id,
		'Content-Type': 'gzip',
		'Accept-Encoding': 'gzip',
		'User-Agent': 'Algolia for Python (%s)' % VERSION
	}
	self._app_id = app_id
	self.api_key = api_key
	
	app_id = transport.headers.get('X-Algolia-Application-Id')
	api_key = transport.headers.get('X-Algolia-API-Key')
	


#__func__.__closure__[0].cell_contents


def acl(client, api_key):
	return client.get_api_key_acl(api_key)


def has_closure(meth):
	if hasattr(meth, '__closure__'):
		return getattr(meth, '__closure__', None)

#headers, get_logs, _transport, _req, _api_key, _app_id

#_transport.session

def examples():
	p = algolia.Index(client, 'pypi')
	ex = p.search_for_facet_values('requires-dist', 'requests')





def get_algolia_values():
	from startups.helpers.third_party import get_keychain
	key = get_keychain()
	key.generate_parsers()
	if key._new_parser is not None:
		return key._new_parser.items('algolia')


def search(index, query = '', args = None, request_options=None):
	if args is None:
		args = {}
	args['query'] = query
	params = {'params': urlencode(urlify(args))}
	return index._req(True, '/query', 'POST', request_options, data=params)

def __req(self, is_search =True, path='/query', meth ='POST', request_options=None, params=None, data=None):
	path = '%s%s' % (self._request_path, path)
	if data is None:
		data = {}
	data['apiKey'] = self.api_key


def search_facet_values(index, facet_name, facet_query='', query=None, request_options=None):
	if query is None:
		query = {}
	query['facetQuery'] = facet_query
	path = '/facets/%s/query' % (facet_name)
	path = '%s%s' % (index._request_path, path)
	print(path)
	return index.search_for_facet_values(facet_name=facet_name, facet_query=facet_query, query=query, request_options=request_options)


#url = 'https://%s%s' % (host, path)
	
#r = self._app_req if APPENGINE else self._session_req
#return r(host, path, meth, timeout, params, data, headers)

#c._transport.req


#'/1/indexes/pypi/settings?getVersion=2'
#r = t.req(False, '/1/indexes/pypi/settings?getVersion=2', 'GET', params={}, data={}, request_options = None)
#r = t._session_req('AG163LOZ6M.algolia.net', path='/1/indexes/pypi/settings?getVersion=2', meth='GET',
#                   timeout=t.timeout, params={}, data={}, headers=headers)
#
#r = cl._transport.session.request('GET', url='https://AG163LOZ6M.algolia.net/1/indexes/pypi/settings?getVersion=2',
#                                  timeout=cl._transport.timeout, headers=cl._transport.headers, params={}, data={})
#




headers = ['name', 'scope', 'type', 'default', 'formerly', 'description']
result = [
          ('query', 'search', str, '""', 'If empty or absent, the textual search will match any object.'),
          ('searchableAttributes', 'settings', list, [], 'attributesToIndex;unordered()'),
          ('attributesForFaceting', 'settings', list, [], 'filterOnly|searchable|'),
          ('unretrievableAttributes', 'settings', list, [], ''),
          ('attributesToRetrieve', 'both', list, '*', 'attributes'),
          ('restrictSearchableAttributes', 'search', list, 'searchableAttributes', 'subset of searchableAttributes'),
	
	
	
	
	('allowCompressionOfIntegerArray', 'settings', '', '', ''),
          ('attributeForDistinct', 'settings', '', '', ''),
          ('camelCaseAttributes', 'settings', '', '', ''),
          ('customRanking', 'settings', '', '', ''),
          ('decompoundedAttributes', 'settings', '', '', ''),
          ('disablePrefixOnAttributes', 'settings', '', '', ''),
          ('disableTypoToleranceOnWords', 'settings', '', '', ''),
          ('numericAttributesForFiltering', 'settings', '', '', ''),
          ('paginationLimitedTo', 'settings', '', '', ''),
          ('ranking', 'settings', list, ["typo", "geo", "words", "filters", "proximity", "attribute", "exact", "custom"], ''),
          ('replicas', 'settings', '', '', ''),
          ('search', 'settings', '', '', ''),
          ('separatorsToIndex', 'settings', '', '', ''),
          ('analytics', 'search', '', '', ''),
          ('analyticsTags', 'search', '', '', ''),
          ('aroundLatLng', 'search', '', '', ''),
          ('aroundLatLngViaIP', 'search', '', '', ''),
          ('aroundPrecision', 'search', '', '', ''),
          ('aroundRadius', 'search', '', '', ''),
          ('clickAnalytics', 'search', '', '', ''),
          ('enableRules', 'search', '', '', ''),
          ('facetFilters', 'search', '', '', ''),
          ('facetingAfterDistinct', 'search', '', '', ''),
          ('facets', 'search', '', '', ''),
          ('filters', 'search', '', '', ''),
          ('getRankingInfo', 'search', '', '', ''),
          ('insideBoundingBox', 'search', '', '', ''),
          ('insidePolygon', 'search', '', '', ''),
          ('length', 'search', '', '', ''),
          ('minimumAroundRadius', 'search', '', '', ''),
          ('numericFilters', 'search', '', '', ''),
          ('offset', 'search', '', '', ''),
          ('optionalFilters', 'search', '', '', ''),
          ('page', 'search', '', '', ''),
          ('percentileComputation', 'search', '', '', ''),
          ('queryType', 'search', '', '', ''),
          ('ruleContexts', 'search', '', '', ''),
          ('setting', 'search', '', '', ''),
          ('settings', 'search', '', '', ''),
          ('sumOrFiltersScores', 'search', '', '', ''),
          ('synonyms', 'search', '', '', ''),
          ('advancedSyntax', 'both', '', '', ''),
          ('allowTyposOnNumericTokens', 'both', '', '', ''),
          ('attributesToHighlight', 'both', '', '', ''),
          ('attributesToSnippet', 'both', '', '', ''),
          ('disableExactOnAttributes', 'both', '', '', ''),
          ('disableTypoToleranceOnAttributes', 'both', '', '', ''),
          ('distinct', 'both', '', '', ''),
          ('exactOnSingleWordQuery', 'both', '', '', ''),
          ('highlightPostTag', 'both', '', '', ''),
          ('highlightPreTag', 'both', '', '', ''),
          ('hitsPerPage', 'both', '', '', ''),
          ('ignorePlurals', 'both', '', '', ''),
          ('maxFacetHits', 'both', '', '', ''),
          ('maxValuesPerFacet', 'both', '', '', ''),
          ('minProximity', 'both', '', '', ''),
          ('minWordSizefor1Typo', 'both', '', '', ''),
          ('minWordSizefor2Typos', 'both', '', '', ''),
          ('optionalWords', 'both', '', '', ''),
          ('removeStopWords', 'both', '', '', ''),
          ('removeWordsIfNoResults', 'both', '', '', ''),
          ('replaceSynonymsInHighlight', 'both', '', '', ''),
          ('responseFields', 'both', '', '', ''),
          ('restrictHighlightAndSnippetArrays', 'both', '', '', ''),
          ('snippetEllipsisText', 'both', '', '', ''),
          ('sortFacetValuesBy', 'both', '', '', ''),
          ('typoTolerance', 'both', '', '', '')]


def get_logs(client, offset=0, length=10, indexName = None, type='all', request_options=None):
	"""
	onlyErrors
	:param client:
	:param offset: default is 0
	:param length: default is 10, max is 1000
	:param indexName: optional or None
	:param type: `all` is default, `query`, `build`, `error`
		query: Retrieve only the queries.
		build: Retrieve only the build operations.
		error: Retrieve only the errors (same as onlyErrors parameters)
	:param request_options:
	:return:
	"""
	logs = client.get_logs(offset=offset, length=length, type=type, request_options=request_options)
	if isinstance(logs, dict) and 'logs' in logs:
		return logs.get('logs')
	
	
	
	#Referer

#def split_log_query_params(): pass


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

ANDNOT,ANDMAYBE,
not='(^|(?<=(\\s|[()])))NOT(?=\\s)'
and_ = '(?<=\\s)AND(?=\\s)'
or_ = '(?<=\\s)OR(?=\\s)'
req = '(^|(?<=\\s))REQUIRE(?=\\s)'
Range =r'''(?P<open>\{|\[)(?P<start>(\'[^\']*?\'\s+)|([^\]}]+?(?=[Tt][Oo])))'''

https://whoosh.readthedocs.io/en/latest/querylang.html

#"whoosh library"~5
render AND shading == render shading

render AND shading OR modeling
render NOT modeling
alpha NOT (beta OR gamma)
(render AND shading) OR modeling
name:ivan
title:open sesame
title:(open sesame) == title:open title:sesame
title:"open sesame"
[apple TO bear]
date:[20050101 TO 20090715]
{prefix TO suffix}
[0000 TO 0025}

[] = inclusive
{} = exclusive
[0025 TO]
{TO suffix}
ninja^2 cowboy bear^0.5
(open sesame)^2.5 roc






"""
S= dict(page=0, hitsPerPage=20, attributesToRetrieve="*", getRankingInfo = 1, facets = '*',
        distinct = 0)

#f = I.search('startups', {'facets': '*', 'advancedSyntax': 1, 'restrictHighlightAndSnippetArrays': True})

#attributesToRetrieve, attributes, settings search,
#sortFacetValuesBy:['count','alpha']
#searchableAttributes =attributesToIndex, list
#restrictSearchableAttributes = []
#attributesToRetrieve
#HEADERS = get(url=url, headers={'X-Requested-With': 'XMLHttpRequest'})
#attributesForFaceting: filterOnly,searchable,''
#unretrievableAttributes


class Object(object):
	def __init__(self, **kwargs):
		for k,v in kwargs.items():
			setattr(self, k,v)
		
	@property
	def tags(self):
		return '_tags', 'tagFilters'

class FacetFilters(object):
	def __init__(self, _data):
		self._data = _data
		
		
		
		



class SearchResult(object):
	KEYS = ['hits', 'nbHits', 'page', 'nbPages', 'hitsPerPage', 'processingTimeMS', 'exhaustiveNbHits', 'query',
	        'params', 'facets']
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
		self._facets = _data.get('facets', {})
		
	def clean_params(self):
		from urllib.parse import unquote
		params = [param.split('=',1) for param in unquote(self._params).split('&')]
		return params
		
		
	

class Hit(object):
	def __init__(self, _data):
		self._data = _data
		self.objectID = _data.get('objectID')
		if '_highlightResult' in _data:
			self._highlightResult = _data.pop('_highlightResult')
		if '_rankingInfo' in _data:
			self._rankingInfo = _data.pop('_rankingInfo')
		#_snippetResult
		#_tags,
		#sumOrFiltersScores = True
		ex = "(company:Google<score=3> OR company:Amazon<score=2> OR company:Facebook<score=1>)"
		_ex = 'attribute:value<score=X>'
		#'numericAttributesToIndex'
	#'customRanking'
	#'attributesToSnippet'
	#'attributesToRetrieve'
	#'attributesToIndex'
	#'attributesForFaceting'
	
	
	
	


class HighlightResult(object):
	def __init__(self, _data):
		self._data = _data
		
		
class Attribute(object):
	searchable = 'searchable\([^)]\)'
	filterOnly = 'filterOnly\([^)]\)'
	
	

class IndexSettings(object):
	def __init__(self, _data):
		self._data = _data
		for k,v in _data.items():
			try:
				setattr(self, k,v)
			except AttributeError:
				pass
		
	@property
	def attributes_for_faceting(self):
		"""
		searchable() and filterOnly()
		:return:
		
		
		Difference between filtering and faceting

		These 2 features are often confused because there is much overlap between them, but understanding the difference is important. In general, both are used for restricting search to a subset of results. There may be cases where this is done entirely hidden to the end user - this is done using filters. In contrast, faceting is generally used for building a UI, where users can select facets (as categories) to further refine their query.

		Practically speaking, facets need to be first set up as filters before they can be used later as facets. The difference begins there: facets go further than filters by offering features such as listing all values, facet counts, and search for facet values.
		
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


class Rule(object):
	def __init__(self, _data):
		self._data = _data
		self.objectid = _data.pop('objectID', '')
		self.description = _data.pop('description', '')
		if 'condition' in self._data:
			condition = self._data.pop('condition')
			self.condition = RuleCondition(condition)
			self.__dict__.update(self.condition.__dict__)
		
		if 'consequence' in self._data:
			consequence = self._data.pop('consequence')
			self.consequence = RuleConsequence(consequence)
			#self.__dict__.update(self.consequence.__dict__)
		#self.condition = RuleCondition(_data.pop('condition'))
		#self.consequence = RuleConsequence(_data.pop('consequence'))
		
		
class RuleCondition(object):
	def __init__(self, condition):
		self.condition = condition
		self.anchoring = condition.get('anchoring')
		self.pattern = condition.get('pattern')
		
		
class RuleConsequence(object):
	def __init__(self, consequence):
		self.consequence = consequence
		
	@property
	def query(self):
		return self.consequence.get('query')
		
	@property
	def promote(self):
		return self.consequence.get('promote')
	@property
	def params(self):
		return self.consequence.get('params')
	
	@property
	def userData(self):
		return self.consequences.get('userData')
	
	
	


class SearchStuff(object):
	filters = 'filters'
	facetFilters = 'negate facet filters using a minus sign (-)'
	attributesToSnippet = ''
	to_snippet = 'attribute:nbWords'
	
	
#formats.Format, analysis.Analyzer
#'whoosh.analysis.analyzers.StandardAnalyzer'

#schema = "whoosh.fields.Schema", #FieldWrapper, #MetaSchema, FieldType
#{'int', int, bool}

JS = """
https://community.algolia.com/instantsearch.js/v2/getting-started.html

appId, apiKey, indexName
const search = instantsearch({
  appId: 'latency',
  apiKey: '6be0576ff61c053d5f9a3225e2a90f76',
  indexName: 'instant_search',
  urlSync: true
});

search.start();"""


if __name__ == '__main__': print(__file__)