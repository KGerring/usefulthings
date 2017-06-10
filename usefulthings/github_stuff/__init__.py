#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = __init__.py
# author=AutisticScreeching
# date = 4/25/17
import sys, os

from pathlib import Path
from github3.repos.repo import Repository
from github3.repos.contents import Contents
from github3.github import GitHub
from github3.session import GitHubSession
from github3.null import NullObject
import github3.exceptions
import github3.git
import github3.repos.comparison
import github3.auths
import github3.pulls
import github3.repos.commit
import github3.repos.deployment
import github3.repos.hook
import github3.repos.stats
import github3.repos.status
import github3.structs
import github3.users
import github3.utils
import github3.repos.branch
from github3.models import BaseCommit
from send2trash import send2trash as remove
safe_delete = remove
try:
	from startups import *
except ImportError:
	pass

from github3.git import Blob, Commit, GitData, Hash, Reference, Tag, Tree
from github3.pulls import PullRequest, PullFile, PullDestination, ReviewComment

GH_Thread = github3.github.Thread
GH_Comparison = github3.repos.comparison.Comparison
Asset = github3.repos.release.Asset
Release = github3.repos.release.Release
Branch = github3.repos.branch.Branch
#github3.events

#93428287
#git_commit
#git_commits_urlt
#git_url

#'X-OAuth-Scopes'
#'X-Accepted-OAuth-Scopes'

#VARS = vars(M)
#create_comment
#from inspect import KEYWORD_ONLY, POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_KEYWORD, VAR_POSITIONAL, _empty
#ENTERPRISE = github3.api.GitHubEnterprise
#enterprise = github3.api.enterprise_login

#http://developer.github.com/v3/repos/commits/#compare-two-commits


response_to_file= github3.utils.stream_response_to_file
gh_Plan = github3.users.Plan
GH_Status = github3.repos.status.Status #http://developer.github.com/v3/repos/statuses/
GH_Hook = github3.repos.hook.Hook

SCOPES = ['admin:gpg_key',
          'admin:org',
          'admin:org_hook',
          'admin:public_key',
          'admin:repo_hook',
          'gist',
          'notifications',
          'public_repo',
          'read:org',
          'repo',
          'repo:status',
          'repo_deployment',
          'user',
          'user:email',
          'user:follow',
          'write:repo_hook']


#username, password, client_id, client_secret



def diff_from_commit(self):
	headers = {'Accept': 'application/vnd.github.diff'}
	resp = self._get(self._api, headers={'Accept': 'application/vnd.github.diff'})
	return resp.content if self._boolean(resp, 200, 404) else b''

def patch_from_commit(self):
	resp = self._get(self._api, headers={'Accept': 'application/vnd.github.patch'})
	return resp.content if self._boolean(resp, 200, 404) else b''

def get_raw(self):
	resp = self._get(url, headers={"Accept": 'application/vnd.github.VERSION.raw+json'})
	return resp




#'github.v3; param=VERSION.raw; format=json'

http = 'com.apple.web-internet-location'
furl= 'public.file-url'
url= 'public.url'
zip = 'public.zip-archive'
arch = 'public.archive'
data = 'public.archive'
#'public.tar-archive'
disk_image = 'public.disk-image'
resolvable = 'com.apple.resolvable'
symlink = 'public.symlink'
log= 'public.log'
direc = 'text/directory'
DB = 'public.database'


from startups import get_keychain, get_github, unmask, mask, encode, decode
from os.path import commonpath, relpath, abspath
from stat import filemode
from fnmatch import translate, filter as fn_filter
import re, regex
from operator import itemgetter, attrgetter, methodcaller
from shlex import split as split_command
from mimetypes import knownfiles, types_map
import filecmp, shlex, pyclbr, pty, pipes
from pyclbr import _readmodule, readmodule_ex
from inspect import modulesbyfile, getsourcefile, getfile, getclosurevars, getargs, getabsfile, getblock, findsource
from mimetypes import MimeTypes, read_mime_types
from difflib import Differ, HtmlDiff

#fspath #__fspath__
#fdopen
#PathLike


	

#STAT =sh('stat -s ./schema.pkl')

#class Matcher: pass






_a = '''gfind /Users/kristen/PycharmProjects/proj/mdls -type d -name "*" -printf "%f\t%p\t%P\t%d\t%A@\t%C@\t%T@
\n"|sort'''
_0 = str(chr(0))

_a ="""xargs -0 egrep --exclude "*/__pycache__/*" "kMD" -l | cut -d "\t" -f 2"""

KEYCHAIN = get_keychain()

BASIC_AUTH_TEMPLATE = {'Authorization': 'Basic {}'}
TOKEN_AUTH_TEMPLATE = {"Authorization": 'token {}'}

TIME_FMT='%a, %d %b %Y %H:%M:%S %Z'
TEMPLATE_NEW_FILE = 'added file {!s}'
TEMPLATE_UPDATED_FILE = 'updated file {!r}'

#patch_url
#parent
#network_events
#merge #todo
#ignore
#forks
#diff_url
#create_tree
#create_release
#create_pull
#create_issue
#create_fork
#create_deployment
#compare_urlt
#compare_commits
#commit_activity
#code_frequency
#branches
#archive_urlt



def prepare_url(*args, **kwargs):
	from furl import furl
	url = furl()
	url = url.load('https://api.github.com')
	if args:
		for arg in args:
			if '=' in arg:
				kv = url.copy().query._extract_items_from_querystr(arg)
				url = url.copy().add(kv)
			elif isinstance(arg, (dict, list, tuple)):
				kv = url.copy().query._items(arg)
				url = url.copy().add(kv)
			else:
				path = url.path._path_from_segments(arg)
				url = url.copy().add(path=arg)
	if kwargs:
		if 'query' in kwargs:
			query = kwargs.get('query')
			kv = url.copy().query._extract_items_from_querystr(query)
		# pass
		if 'query_params' in kwargs:
			query_params = kwargs.get('query_params')
			url = url.copy().add(query_params=query_params)
		if 'params' in kwargs:
			params = kwargs.get('params')
			url = url.copy().add(query_params=params)
		if 'path' in kwargs:
			path = kwargs.get('path')
			url = url.copy().add(path=path)
		if 'args' in kwargs:
			args = kwargs.get('args')
			url = url.copy().add(args=args)
		if 'fragment' or 'fragment_path' in kwargs:
			fragment = kwargs.get('fragment')
			url = url.copy().add(fragment_path=fragment)
	# if args:
	#	path = url.path._path_from_segments(args)
	# else:
	#	path = ''
	# url = url.copy().add(path=path)
	return url


COMPARE_URL = "https://api.github.com/repos/{user}/{repo}/compare/{base}...{head}"
ARCHIVE_URL = 'https://api.github.com/repos/KGerring/mdls/{zipball}/{master}' #path
#resp = self._get(url, allow_redirects=True, stream=True)




gitignore ='public.data'
rst='dyn.ah62d4rv4ge81e65y'
ini='dyn.ah62d4rv4ge80w5xm'
pkl='dyn.ah62d4rv4ge81a45q'
yml = 'dyn.ah62d4rv4ge81w5pq'
cfg ='dyn.ah62d4rv4ge80g3xh'
py='public.python-script'

all_repositories = methodcaller('repositories', type='all', sort='pushed')




def make_basic_auth(username=None, password=None, keychain=None):
	if keychain:
		username =keychain.get('github', 'username')
		password = keychain.get('github', 'password')
	else:
		username=username
		password=password
	
	basic = '{}:{}'.format(username,password)
	hidden = mask(hidden)
	header= BASIC_AUTH_TEMPLATE['Authorization'].format(hidden)
	return header


def make_token_auth(token = None, keychain=None):
	if keychain:
		token = keychain.get('github', 'gitmore_token')
	else:
		token = token
	header= TOKEN_AUTH_TEMPLATE['Authorization'].format(token)
	return header
	
class NullObjectException(Exception):
	pass



#-fls
#-fstype
#-ilname pattern

_gfind='''gfind . -type d -regex "^.*" -printf "%AY-%Am-%AdT%AH:%AM:00\t%P\t%sb\t%Y\n"'''
_findthing ='''gfind $HOME -type d -iname mdls -regex ".*/PycharmProjects/.*"'''
_findthing = '''gfind $PWD -type d -iname mdls -regex ".*/PycharmProjects/.*"'''


#subprocess.Popen(['gfind','$PWD', '-mtime','0'],shell=True)

#g = self._iter(int(-1), url, GitRepository, params, None)

def iterate_url(*args, **kwargs):

	headers= {'Accept':        'application/vnd.github.v3.full+json',
	          'Authorization': 'token b2e768397367c7b46c4de3d73ad78b41c6d01faa'}
	if 'url' in kwargs:
		url = kwargs.pop('url')
	else:
		url = str(prepare_url(*args, **kwargs))
		print(url)
		
	get(url, headers=headers).json()
	#return
	#	#parts = ['repos', 'KGerring', 'startups', 'contents']
	#	if args:
	#		parts.extend(args)
	#		url = str(prepare_url(*parts, **kwargs))
	#		dic = get(url, params=kwargs, headers = headers).json()
	#return dic
		


def iterate(json_data):
	urls = []
	for item in json_data:
		if item.get('type') == 'file':
			urls.append(item)
		elif item.get('type') == 'dir':
			url = item.get('url')
			urls.extend(iterate_url(url=url, recursive='1'))
	return urls
			



class GitRepository(Repository):
	
	
	def path_contents(self, path='', ref='master', return_as=dict):
		from github3.repos.contents import Contents
		contents = dict(__docs__=set([]))
		url = self._build_url('contents', path, base_url=self._api)
		json = self._json(self._get(url, params={'ref': ref}), 200) or []
		for j in json:
			type = j.get('type', '')
			path = j.get('path', '')
			contents.update({path: Contents(j, self)})
			if type == 'dir':
				contents['__docs__'].add(path)
		return contents
	
	def iterate_all_files(self, initial_path='', ref='master'):
		from toolz import merge
		from github3.repos.contents import Contents
		contents = self.path_contents(path=initial_path, ref=ref, return_as=dict)
		__docs__ = contents.get('__docs__')
		while len(__docs__) > 0:
			path = __docs__.pop()
			new_contents = self.path_contents(path=path, ref=ref)
			contents = merge(new_contents, contents)
		
		contents.pop('__docs__')
		self._contents = contents.copy()
		return contents
	
	def ensure_file(self, filename, **kwargs):
		try:
			contents = self.directory_contents(filename)
		except AttributeError:
			contents = self.file_contents(filename)
			if isinstance(contents, NullObject):
				return False
			else:
				return True
		return None
				#return 'file NOT THERE {!r}'.format(str(contents))  ##todo
	
	def add_new_file(self, name, fromfile, branch = 'master', local_dir=os.getcwd()):
		
		message= TEMPLATE_NEW_FILE.format(name)
		with open(fromfile, 'rb') as reader:
			content = reader.read()
		newfile = self.create_file(path=name, message = message,
		                           branch=branch, content=content)
		
		return newfile
		
			
	def update_file(self, filename, localfilename, localdir=None):
		file_contents = repository.file_contents(filename)
		if localdir:
			file = os.path.join(localdir, localfilename)
		else:
			file = localfilename
		
		if file_contents.__class__.__name__ != 'NullObject':
			with open(file, 'rb') as reader:
				content = reader.read()
				message = '{!r} updated'.format(filename)
				file_contents(filename).update(message, content)
				print(message)
		else:
			with open(file, 'rb') as reader:
				content = reader.read()
				message = '{!r} created'.format(localfilename)
				file_contents = self.create_file(path=localfilename, message=message, content=content)
				print(message)
				
		return file_contents



META = {'ETag':                               'W/"4940686ba09e6edd8397805967132d33"',
        'Last-Modified':                      '',
        'git':                                ['192.30.252.0/22'],
        'github_services_sha':                '749995b7a788ea5070c900866007c448e04afd8f',
        'hooks':                              ['192.30.252.0/22'],
        'importer':                           ['54.158.161.132', '54.226.70.38', '54.87.5.173', '54.166.52.62'],
        'pages':                              ['192.30.252.153/32', '192.30.252.154/32'],
        'verifiable_password_authentication': True}



class GitHelper(github3.github.GitHub):
	
	gists = []
	repositories = dict()
	
	
	




if __name__ == '__main__': print(__file__)