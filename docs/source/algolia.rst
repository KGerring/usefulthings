.. author KGerring
.. filename algolia
.. date = 11/27/17

=======
algolia
=======


search
------
  - analytics
  - analyticsTags
  - aroundLatLng
  - aroundLatLngViaIP
  - aroundPrecision
  - aroundRadius
  - clickAnalytics
  - enableRules_
  - facetFilters_
  - facetingAfterDistinct
  - facets
  - filters_
  - getRankingInfo
  - insideBoundingBox
  - insidePolygon
  - length
  - minimumAroundRadius
  - numericFilters_
  - offset
  - optionalFilters_
  - page
  - percentileComputation
  - query
  - queryType
  - restrictSearchableAttributes_
  - ruleContexts_
  - setting
  - settings
  - sumOrFiltersScores_
  - synonyms

settings
--------
  - allowCompressionOfIntegerArray_
  - attributeForDistinct
  - attributesForFaceting_
  - camelCaseAttributes
  - customRanking
  - decompoundedAttributes
  - disablePrefixOnAttributes
  - disableTypoToleranceOnWords
  - numericAttributesForFiltering_
  - paginationLimitedTo
  - ranking_
  - replicas
  - search
  - searchableAttributes_
  - separatorsToIndex
  - unretrievableAttributes_

search & settings
-----------------
  - advancedSyntax_
  - allowTyposOnNumericTokens
  - attributesToHighlight
  - attributesToRetrieve_
  - attributesToSnippet
  - disableExactOnAttributes
  - disableTypoToleranceOnAttributes
  - distinct
  - exactOnSingleWordQuery
  - highlightPostTag
  - highlightPreTag
  - hitsPerPage
  - ignorePlurals
  - maxFacetHits
  - maxValuesPerFacet
  - minProximity
  - minWordSizefor1Typo
  - minWordSizefor2Typos
  - optionalWords
  - removeStopWords
  - removeWordsIfNoResults
  - replaceSynonymsInHighlight
  - responseFields
  - restrictHighlightAndSnippetArrays
  - snippetEllipsisText
  - sortFacetValuesBy
  - typoTolerance


Attributes
^^^^^^^^^^

.. _searchableAttributes:

searchableAttributes
++++++++++++++++++++
:scope: settings
:type: array of strings
:default: []
:formerly: attributesToIndex

To assign the same priority to several attributes, pass them within the same string, separated by commas
`'a,b', 'c'`
Within a given attribute, matches near the beginning of the text are considered more important than matches near the end. use `unordered`


.. _attributesForFaceting:

attributesForFaceting
+++++++++++++++++++++
:scope: settings
:type: array of strings
:default: []
:description: List of attributes you want to use for faceting.



.. _unretrievableAttributes:

unretrievableAttributes
+++++++++++++++++++++++
:scope: settings
:type: array of strings
:default: []
:description: List of attributes that cannot be retrieved at query time.



.. _attributesToRetrieve:

attributesToRetrieve
++++++++++++++++++++
:scope: settings search
:type: array of strings
:default: "*"
:formerly: attributes
:description: List of object attributes you want to retrieve


.. _restrictSearchableAttributes:

restrictSearchableAttributes
++++++++++++++++++++++++++++
:scope: search
:type: array of strings
:default: all attributes in searchableAttributes_

It must be a subset of the searchableAttributes index setting
`restrictSearchableAttributes` is a search time parameter, it will only affect the current query.
It will not override your index settings.


Ranking
^^^^^^^

.. _ranking:

ranking
+++++++
:scope: settings
:type: array of strings
:default: ["typo", "geo", "words", "filters", "proximity", "attribute", "exact", "custom"]
:description: Controls the way results are sorted.

The following ranking criteria are available:

typo
    Sort by increasing number of typos.
geo
    Sort by decreasing geo distance when performing a geo search; ignored when not performing a geo search.
words
    Sort by decreasing number of matched query words. This parameter is useful when you use the optionalWords_ query parameter to rank hits with the most matched words first.
filters
  The filter criteria is the sum of scores for filters matched by one hit. In case of OR filters, only one score is taken in account even if the two filters match.
proximity
    Sort by increasing proximity of query words in hits.
attribute
    Sort according to the order of attributes defined by searchableAttributes_
`exact`
    If the query contains only one word: The behavior depends on the value of exactOnSingleWordQuery_. If the query contains multiple words: Sort by decreasing number of words that matched exactly. What is considered to be an exact match depends on the value of alternativesAsExact_


customRanking
+++++++++++++

replicas
++++++++





Filtering
^^^^^^^^^

.. _tagFilters:
.. _filters:
.. _numericFilters:

filters
+++++++
:scope: search

  - Numeric *comparison* `${attributeName} ${operator} ${operand}`
  - Numeric *range* `${attributeName}:${lowerBound} TO ${upperBound}`
  - Facet facetFilter `${facetName}:${facetValue}` case-sensitive
  - tags Tag `_tags:${value}` case-sensitive.
  - If no attribute name is specified, the filter applies to \_tags
  - For performance reasons, filter expressions are limited to a conjunction (ANDs) of disjunctions (ORs).

.. code:: python

    results = index.search('query', {'filters': '(category:Book OR category:Ebook) AND _tags:published'})


.. _facetFilters:

facetFilters
++++++++++++
:scope: search

`{'facetFilters': ['category:Book', 'author:John Doe']}`
  - in form `${attributeName}:${value}`
  - if regular list it is with *AND*
  - for *OR* nest the list.
    + [["category:Book", "category:Movie"], "author:John Doe"]  is `(category:Book OR category:Movie) AND author:"John Doe"`
  - Negation is with \- before the value
    + `["category:Book", "category:-Movie"]` is `category:Book AND NOT category:Movie`
  - see also filters_



.. _optionalFilters:

optionalFilters
+++++++++++++++
:scope: search
:default: []

Optional filters behave much like regular filters, except that results not matching the filter are not excluded altogether; they’re simply ranked lower in the result set.

.. _sumOrFiltersScores:

sumOrFiltersScores
++++++++++++++++++
:scope: search
:type: bool
:default: False

Determines how to calculate the total score for filtering
When `sumOrFiltersScores` is `false`, max score will be kept.
When `sumOrFiltersScores` is `true`, score will be summed.

Faceting
^^^^^^^^
facets
++++++

maxValuesPerFacet
+++++++++++++++++

facetingAfterDistinct
+++++++++++++++++++++

sortFacetValuesBy
+++++++++++++++++




Highlight/Snippet
^^^^^^^^^^^^^^^^^

attributesToHighlight
+++++++++++++++++++++

attributesToSnippet
+++++++++++++++++++

highlightPreTag
+++++++++++++++

highlightPostTag
++++++++++++++++

snippetEllipsisText
+++++++++++++++++++

restrictHighlightAndSnippetArrays
+++++++++++++++++++++++++++++++++



Pagination
^^^^^^^^^^

page
++++

hitsPerPage
+++++++++++

offset
++++++

length
++++++

paginationLimitedTo
+++++++++++++++++++




Typos
^^^^^

minWordSizefor1Typo
+++++++++++++++++++

minWordSizefor2Typos
++++++++++++++++++++

typoTolerance
+++++++++++++

allowTyposOnNumericTokens
+++++++++++++++++++++++++

ignorePlurals
+++++++++++++

disableTypoToleranceOnAttributes
++++++++++++++++++++++++++++++++

disableTypoToleranceOnWords
+++++++++++++++++++++++++++

separatorsToIndex
+++++++++++++++++


Query Strategy
^^^^^^^^^^^^^^

queryType
+++++++++

removeWordsIfNoResults
++++++++++++++++++++++

advancedSyntax
++++++++++++++

optionalWords
+++++++++++++

removeStopWords
+++++++++++++++

disablePrefixOnAttributes
+++++++++++++++++++++++++

disableExactOnAttributes
++++++++++++++++++++++++

.. _exactOnSingleWordQuery:

exactOnSingleWordQuery
++++++++++++++++++++++
:scope: settings search
:type: str
:default: attribute
:description: deals with how the `exact` criterion is decided in ranking_


The following values are allowed:
  - attribute: if the query string exactly matches an entire attribute value
  - none: ignored on single word queries
  - word: set to 1 if the query word is found in the record. Must be > 3 and not stop-word





.. _alternativesAsExact:

alternativesAsExact
+++++++++++++++++++
:scope: setting search
:type: array of strings
:default: ["ignorePlurals", "singleWordSynonym"]
:description: List of alternatives that should be considered an exact match by the exact ranking criterion.

The following values are allowed:
  - ignorePlurals : alternative words added by the ignorePlurals_ feature;
  - multiWordsSynonym: multiple-words synonyms (example: "NY" = "New York").
  - singleWordSynonym: single-word synonyms (example: "NY" = "NYC");


Query Rules
^^^^^^^^^^^

.. _enableRules:

enableRules
+++++++++++
:scope: search settings
:type: bool
:default: True

.. _ruleContexts:

ruleContexts
++++++++++++
:scope: search
:type: array of strings
:default: []

Enables contextual rules.




Performance
^^^^^^^^^^^

.. _numericAttributesForFiltering:

numericAttributesForFiltering
+++++++++++++++++++++++++++++
:scope: settings
:default: all numeric attributes
:type: array of strings
:formerly: **numericAttributesToIndex**
:description: List of numeric attributes that can be used as numerical filters.


If not specified, all numeric attributes are automatically indexed and available as numerical filters
If specified, only attributes explicitly listed are available as numerical filters.
If empty, no numerical filters are allowed.
If you don’t need filtering on some of your numerical attributes, you can use `numericAttributesForFiltering` to speed up the indexing.
If you only need to filter on a numeric value based on equality (i.e. with the operators `=` or `!=`), you can speed up the indexing by specifying `equalOnly(${attributeName})`. Other operators will be disabled.


.. _allowCompressionOfIntegerArray:

allowCompressionOfIntegerArray
++++++++++++++++++++++++++++++
:scope: settings
:type: bool
:default: False

Enables compression of large integer arrays.

Advanced
^^^^^^^^

.. _advancedSyntax:

advancedSyntax
++++++++++++++
:scope: settings search
:type: bool
:default: False
:description: Enables the advanced-syntax stuff

attributeForDistinct
++++++++++++++++++++

placeholders
++++++++++++

minProximity
++++++++++++

responseFields
++++++++++++++

maxFacetHits
++++++++++++

percentileComputation
+++++++++++++++++++++

camelCaseAttributes
+++++++++++++++++++

decompoundedAttributes
++++++++++++++++++++++

distinct
++++++++

getRankingInfo
++++++++++++++

clickAnalytics
++++++++++++++

analytics
+++++++++

analyticsTags
+++++++++++++

synonyms
++++++++

replaceSynonymsInHighlight
++++++++++++++++++++++++++




search-info
-----------

- page: Number of the page to retrieve.
- hitsPerPage: Maximum number of hits per page
- offset:Offset of the first hit to return (zero-based)
- length: Maximum number of hits to return. (1000 is the maximum)
- paginationLimitedTo: Maximum number of hits accessible via pagination.


client
------

.. code:: python

    from algoliasearch import algoliasearch
    client = algoliasearch.Client("YourApplicationID", 'YourAPIKey')
    index.set_settings({"customRanking": ["desc(followers)"]})



.. |date| date:: %Y-%m-%dT%H:%M:%S

.. [#] This document was generated |date| .
