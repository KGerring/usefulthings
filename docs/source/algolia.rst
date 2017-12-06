.. author KGerring
.. filename algolia
.. date = 11/27/17

=======
algolia
=======


a
-
'''
code          code object
 |          callcount     how many times this was called
 |          reccallcount  how many times called recursively
 |          totaltime     total time in this entry
 |          inlinetime    inline time in this entry (not in subcalls)
 |          calls         details of the calls


			code          called code object
 |          callcount     how many times this is called
 |          reccallcount  how many times this is called recursively
 |          totaltime     total time spent in this call
 |          inlinetime    inline time (not in further subcalls)


def func_to_id(code):
	func = cProfile.label(code)
	i = id(code)

def snapshot_stats(self):
        entries = self.getstats()
        self.stats = {}
        callersdicts = {}
        # call information
        for entry in entries:
            func = cProfile.label(entry.code)
            nc = entry.callcount         # ncalls column of pstats (before '/')
            cc = nc - entry.reccallcount # ncalls column of pstats (after '/')
            tt = entry.inlinetime        # tottime column of pstats
            ct = entry.totaltime         # cumtime column of pstats
            callers = {}
            callersdicts[id(entry.code)] = callers
            self.stats[func] = cc, nc, tt, ct, callers
        # subcall information
        for entry in entries:
            if entry.calls:
                func = cProfile.label(entry.code)
                for subentry in entry.calls:
                    try:
                        callers = callersdicts[id(subentry.code)]
                    except KeyError:
                        continue
                    nc = subentry.callcount
                    cc = nc - subentry.reccallcount
                    tt = subentry.inlinetime
                    ct = subentry.totaltime
                    if func in callers:
                        prev = callers[func]
                        nc += prev[0]
                        cc += prev[1]
                        tt += prev[2]
                        ct += prev[3]
                    callers[func] = nc, cc, tt, ct
    # The following two methods can be called by clients to use
    # a profiler to profile a statement, given as a string.



'''




settings
--------

- searchableAttributes
- paginationLimitedTo
- maxValuesPerFacet
- hitsPerPage
- highlightPostTag
- highlightPreTag
- attributesToSnippet
- attributesToRetrieve
- attributesToHighlight
- attributesForFaceting
	searchable(attributeName)
	If you only need the filtering features, you can take advantage of filterOnly(attribute)

- attributeForDistinct
- advancedSyntax True/False
-restrictSearchableAttributes
- sortFacetValuesBy (alpha/count)


search
------

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
