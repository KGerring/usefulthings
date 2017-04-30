#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = github
# author=AutisticScreeching
# date = 4/28/17
import sys, os
from github3.repos.repo import Repository
from github3.repos.contents import Contents
from github3.github import GitHub
from github3.session import GitHubSession
from send2trash import send2trash as remove
from uritemplate import URITemplate
try:
	from startups import *
except ImportError:
	pass
from operator import methodcaller
from urllib.parse import unquote
from usefulthings.github_stuff import GitRepository

import re, regex


def now_time_commit():
	return get_now(name='US/Eastern').strftime('%Y-%m-%dT%H:%M:%SZ')

RSS_GIT ='http://127.0.0.1:1234/?p=.git;a=rss'
ATOM_GIT ='http://127.0.0.1:1234/?p=.git;a=atom;f=mdls/base.py'
RAW='http://127.0.0.1:1234/?p=.git;a=blob_plain;f=mdls/metadata/utt.py;hb=fdc7318744f2b87ae1c92c9fbc83f4233dce6cb0'
__url_cache__ = dict()



#cmd('gfind /Users/kristen/PycharmProjects/proj/mdls -type f -name "*"|grep -v ".git"')
RH = '/Users/kristen/Library/Application Support/Gitbox/git-1.7.7.2.3.g19dee/git.bundle/lib/python2.7/site-packages/git_remote_helpers'

ACCEPT_HEADERS = dict(json=     'application/vnd.github.v3+json',
                      raw=      'application/vnd.github.v3.raw',
                      diff=     'application/vnd.github.v3.diff',
                      patch=    'application/vnd.github.v3.patch',
                      sha=      'application/vnd.github.v3.sha',
                      base64=   'application/vnd.github.v3.base64',
                      full=     'application/vnd.github.v3.full')
                      

CONF ='''
# --- Example file ---
# this is a comment
url ="https://api.github.com/repos/KGerring/mdls/git/blobs/fc6e67a1c51cbfdd1a10cea8d288374b8ba60ff0"
header= "Authorization: token b2e768397367c7b46c4de3d73ad78b41c6d01faa"
header="Accept: application/vnd.github.v3.raw"
'''
T= '%Y-%m-%dT%H:%M:%SZ'

#{'Accept': 'application/vnd.github.v3.base64'}


#dt = datetime.strptime(time_str, __timeformat__)
#datetime.datetime.strptime('Tue, 11 Apr 2017 21:32:02 GMT', '%a, %d %b %Y %H:%M:%S %Z')

#m.join('mdls','_data').listdir()[0].relto(m)

def ensure_make(repo, path):
	if repo.file_contents(path).is_null():
		file =repo.create_file(
			path =path,
			message=path,
			content= PathEntry(path).read_binary())
	return file

#'(?<=-)\w+'         # will match a word following a hyphen. Matches 'egg' in 'spam-egg'
#Isaac(?=Asimov)  # will match 'Isaac ' only if it’s followed by 'Asimov'
#Isaac(?!Asimov)  # will match 'Isaac ' only if it’s not followed by 'Asimov'
#(?<=abc)def  # will find a match in abcdef (will match def)
#	(?<!a)b  # matches a "b" that is not preceded by an "a", using negative lookbehind.


# It doesn't match cab, but matches the b (and only the b) in bed or debt
#(? <= a)b  # (positive lookbehind) matches the b (and only the b) in cab,
# but does not match bed or debt
def re_show(regexp, string, left="{", right="}", color="blue"):
	import re, regex
	import termcolor
	if color:
		#func = getattr(colors, color)
		left, right = ['\x1b[35m', '\x1b[0m']
	# print('Using REGEXP {0!s} on STRING {1!s}'.format(colors.negative(regexp, 'red'), colors.negative(string, 'green')))
	result = re.compile(regexp, re.M).sub(left + r"\g<0>" + right, string.rstrip())
	result = regex.compile(regexp, regex.V1).sub(left + r"\g<0>" + right, string.rstrip())
	print('re.match({!r}, {!r}) => {!s}'.format(regexp, string, result))

re_show('purebasename(?=.ext)', 'purebasename.ext')
re_show('(?<=purebasename).ext', 'purebasename.ext')
re_show('(?<!__pycache__)\.py', '__pycache__.py')
re_show('Isaac(?!Asimov)', 'IsaacAsimov')
re_show('Isaac(?!Asimov)', 'IsaacAsimo')

LOOK = '\(\?[!<=]{,3}'

# (?P=...: a named group reference.
# (?=... or (?!...: lookahead.
# (?P>...: a call to a group.
# (?P...: a Python extension.
# (?#...: a comment.
# (?(...: a conditional subpattern.
# (?>...: an atomic subpattern
# (?|...: a common/reset groups branch
# (?R...: probably a call to a group
# (?&...: a call to a named group.
# (...: an unnamed capture group
# (?(?...
# (?(?=... or (?(?!...: lookahead conditional
# (?(?<=... or (?(?<!...: lookbehind conditional.
#"Parses a set union ([x||y])
#"Parses a set symmetric difference ([x~~y])."
#"Parses a set intersection ([x&&y])."
#"Parses a set difference ([x--y])."
#"Parses a set implicit union ([xy])."
#PROPERTIES = _regex.get_properties()
#CHARSET_ESCAPES
#POSITION_ESCAPES

#/Users/kristen/anaconda/lib/python3.6/inspect.py:796:        pat = re.compile(r'^(\s*def\s)|(\s*async\s+def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')

#``(?:...)++`` is equivalent to ``(?>(?:...)+)``
##/Users/kristen/anaconda/lib/python3.6/site-packages/regex-2017.4.5.dist-info/METADATA
##/Users/kristen/anaconda/lib/python3.6/site-packages/regex-2017.4.5.dist-info/DESCRIPTION.rst
from stuf import patterns

import  pygments.lexers.markup

def test_qualified_re_sub(self):
	self.assertEqual(regex.sub('a', 'b', 'aaaaa'), 'bbbbb')
	self.assertEqual(regex.sub('a', 'b', 'aaaaa', 1), 'baaaa')

rr = regex.findall(r"(a|(b))", "aba")

#self.assertEqual(regex.search(r"^abc$", "\nabc\n", regex.M)[0], 'abc')
#self.assertEqual(regex.search(r"^\Aabc\Z$", "abc", regex.M)[0], 'abc')
#self.assertEqual(regex.search(r"^\Aabc\Z$", "\nabc\n", regex.M), None)

ACCEPT =dict(
		any=['application/vnd.github.v3+json', 'application/vnd.github.v3.raw+json'],
		comment=[
	             'application/vnd.github.v3.raw+json',
	             'application/vnd.github.v3.text+json',
	             'application/vnd.github.v3.html+json',
	             'application/vnd.github.v3.full+json'],
		gist=[
	             'application/vnd.github.v3+json',
	             'application/json',
	             'application/vnd.github.v3.raw'],
		comparison=[
	             'application/vnd.github.v3.diff',
	             'application/vnd.github.v3.patch',
	             'application/vnd.github.v3.sha'],
		commit=[
	             'application/vnd.github.v3.diff',
	             'application/vnd.github.v3.patch',
	             'application/vnd.github.v3.sha'],
		pull=[
	             'application/vnd.github.v3.diff',
	             'application/vnd.github.v3.patch',
	             'application/vnd.github.v3.sha'],
		contents=['application/vnd.github.v3.raw',
                       'application/vnd.github.v3.html'],
		gists=['application/vnd.github.v3.raw',
	             'application/vnd.github.v3.base64'])
             
class Headers(object):
	re_url = '<(?P<url>[^>]+)>'
	COMPARE_URL =       URITemplate("https://api.github.com/repos{/user}{/repo}compare{/contents}")
	ARCHIVE_URL =       URITemplate('https://api.github.com/repos{/user}{/repo}{/type}{/ref}')
	SUBSCRIPTIONS =     URITemplate('https://api.github.com/users{/user}/subscriptions')
	USER =              URITemplate('https://api.github.com/users{/user}')
	REPOS =             URITemplate('https://api.github.com/users{/user}/repos')
	RECIEVED_EVENTS =   URITemplate('https://api.github.com/users{/user}/received_events')
	ORGS =              URITemplate('https://api.github.com/users{/user}/orgs')
	GISTS =             URITemplate('https://api.github.com/users{/user}/gists{/gist_id}')
	FOLLOWING=          URITemplate('https://api.github.com/users{/user}/following{/other_user}')
	FOLLOWERS=          URITemplate('https://api.github.com/users{/user}/followers')
	EVENTS =            URITemplate('https://api.github.com/users{/user}/events{/privacy}')
	STARRED =           URITemplate('https://api.github.com/users{/user}/starred{/owner}{/repo}')
	USER =              URITemplate('https://api.github.com/users{/user}')
	ME =                URITemplate('https://api.github.com/users{/user}')
	
	# path




class Link(object):
	__timeformat__ = '%a, %d %b %Y %H:%M:%S %Z'
	__date__ = "Date"
	
	EXPOSE = 'ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval'
	
	p2='https://api.github.com/user/10824347/received_events?page=2'
	
	

class GitMore(GitHub):
	def __init__(self, username=None, password=None, token=None, keychain=None):
		if keychain:
			username = keychain.get('github', 'username')
			password = keychain.get('github', 'password')
			token = keychain.get('github', 'token')
		super(GitMore, self).__init__(username=username, password=password, token=token)
		self.session.token_auth(token)
		
	def my_repos(self):
		#return methodcaller('repositories', type='all', sort='pushed')(self)
		params = {'sort': 'pushed', 'type': 'all'}#rep
		return self._iter(int(-1), url='https://api.github.com/user/repos', cls=GitRepository, params=params, etag=None)

#parts
#ensure

if __name__ == '__main__': print(__file__)