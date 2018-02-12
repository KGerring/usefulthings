.. author KGerring
.. name algolia_search
.. filename 
.. date = 2/10/18

=====
Title
=====

search_for_facet_values
+++++++++++++++++++++++

  - facet_name: name of the facet to search. It must have been
    declared in the index's `attributesForFacetting` setting with the
    `searchable()` modifier.
  - facet_query: text to search for in the facet's values.
  - query: an optional query to take extra search parameters into


search_disjunctive_faceting
+++++++++++++++++++++++++++
  - query: the query
  - disjunctive_facets: the array of disjunctive facets
  - params: a hash representing the regular query parameters

search
++++++

args
----
if set, contains an associative array with query parameters

=====================  ======  =========  ======================================================
query                  type    default    desc
=====================  ======  =========  ======================================================
page                   int     0          the page to retrieve (zero-based)
hitsPerPage            int     20         number of hits per page
attributesToRetrieve   str     "*"        list of object attributes you want in result
attributesToHighlight  str     "*"        Attributes are separated by a comma
attributesToSnippet    str     None       ex:(attributesToSnippet=name:10,content:10)
minWordSizefor1Typo    int     3          the min char # in a query-word to accept one typo
minWordSizefor2Typos   int     7          the minimum char # in a query-word to accept two typos
getRankingInfo         int     0          if set to 1, will contain _rankingInfo attribute.
tagFilters             str                filter the query by a set of tags.
facetFilters           str     ''         filter query by csv facets like attributeName:value
optionalWords          str     ''         comma-sep list of optional words in query
distinct               int     0          If set to 1, enable the distinct feature
=====================  ======  =========  ======================================================



tagFilters
----------
filter the query by a set of tags.
You can AND tags by separating them by commas.
To OR tags, you must add parentheses.
For example, tags=tag1,(tag2,tag3) means tag1 AND (tag2 OR tag3).
You can also use a string array encoding,
    for example tagFilters: ['tag1',['tag2','tag3']] means tag1 AND (tag2 OR tag3).

At indexing, tags should be added in the _tags** attribute of objects (for example {'_tags':['tag1','tag2']}).



numericFilters;str;


A `matchLevel` is returned for each highlighted attribute and can contain:
full: if all the query terms were found in the attribute,
partial: if only some of the query terms were found,
none: if none of the query terms were found.





SETTINGS
________

queryType
    Select how the query words are interpreted, it can be any of
prefixAll
    all query words are interpreted as prefixes
prefixLast #default
    only the last word is interpreted as a prefix
prefixNone
    no query word is interpreted as a prefix. Not recommended

optionalWords

customRanking
    ['typo', 'geo', 'proximity', 'attribute', 'exact', 'custom']

attributesToRetrieve
    default list of attributes to retrieve in objects. If set to null, all attributes are retrieved

attributesToHighlight
    default list of attributes to highlight. If set to null, all indexed attributes are highlighted

attributesToSnippet
    default list of attributes to snippet alongside the number of words to return (attributeName:nbWords); null or default is None computed

attributesToIndex
    line ``['title', 'unordered(text)']``

attributesForFaceting
    All strings in the attribute selected for faceting are extracted and added as a facet

attributeForDistinct
    The attribute name used for the `distinct` feature. when enabled in query with the distinct=1 parameter, all hits containing a duplicate value for this attribute are removed from results. For example, if the chosen attribute is `show_name` and several hits have the same value for show_name, then only the best one is kept and others are removed

ranking
    controls the way results are sorted
    typo, geo,

    - proximity
        sort according to the proximity of query words in hits,
    - attribute
        sort according to the order of attributes defined by attributesToIndex
    - exact
        ['typo', 'geo', 'proximity', 'attribute', 'exact', 'custom']

customRanking
    lets you specify part of the ranking. The syntax of this condition is an array of strings containing attributes prefixed by asc (ascending order) or desc (descending order) operator.
    For example `'customRanking' =>", ['desc(population)', 'asc(name)']`

hitsPerPage #default = 10
attributesToRetrieve
highlightPostTag #'</em>'
highlightPreTag #'<em>'







.. |date| date:: %Y-%m-%dT%H:%M:%S

.. [#] This document was generated |date| .
