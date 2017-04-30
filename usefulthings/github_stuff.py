#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = github_stuff
# author=KGerring
# date = 4/3/17

import sys, os
import subprocess
from pathlib import Path
from github3.null import NullObject
from github3.repos.repo import Repository
from github3.repos.contents import Contents
from github3.github import GitHub
import github3.exceptions
from startups import get_keychain, get_github
from twisted.python.filepath import FilePath, Permissions, RWX
from twisted.python.reflect import qual, namedAny, getClass
from twisted.python.modules import walkModules, dirname, PythonPath, PythonAttribute, PathEntry
import fnmatch
from os.path import commonpath, relpath, abspath
from stat import filemode
import github3.git
from operator import itemgetter, attrgetter
import pip.vcs
from pip.vcs import git
from glob import _iglob, _glob1, _glob2, iglob, glob1
from fnmatch import translate, filter
import re, regex
import subprocess

_t = subprocess.Popen(['gfind', '.', '-type', 'd', '-path', './proj/mdls/[!.]*', '-regextype', 'posix-egrep', '-print'],
                      shell=0, stdout=-1, universal_newlines=True,
                      cwd='/Users/kristen/PycharmProjects').communicate()[0].splitlines()
_tt= subprocess.Popen(
		['gfind', '.', '-type', 'd', '-path', './proj/mdls/[!.]*', '-regextype', 'posix-egrep', '-printf', '%P\\0'],
		shell=0, stdout=-1, universal_newlines=True, cwd='/Users/kristen/PycharmProjects').communicate()[0]

#import mdls.mixins.base


re_null = re.compile("'\(null\)'")
re_mdimport = re.compile(r"'(?P<name>[^']+)'\s*'(?P<title>[^']+)'\s*'(?P<desc>[^']+)'\s*'(?P<short>[^']+)'")

go = subprocess.getoutput('''mdfind -0 -onlyin /Users/kristen/PycharmProjects/proj/mdls . \
| xargs -0 grep -lE "import (\S+)" --exclude-dir "__pycache__" --null ''').split(chr(0))

#list(glob.iglob('./**/mdls/**', recursive=True))
#list(_iglob('../**', recursive=True, dironly=False))

#_make_child_relpath


#events

#commits(sha='master',

#md.commit_activity()
#compare_commits



def iglob(pathname, recursive, dironly): pass

#commits(path='mdls')

#Git
todo = 'https://github.com/msabramo/setuptools-git'
hgtools ='https://github.com/jaraco/hgtools'
GitPython = 'https://github.com/gitpython-developers/GitPython'

#re.findall('^(\S+)\s*\(([\d\,]{7,})\)', g, re.M)






PYTHON  = ['twisted.python._oldstyle',
           'twisted.python._tzhelper',
           'twisted.python.compat',
           'twisted.python.components',
           'twisted.python.context',
           'twisted.python.deprecate', #
           'twisted.python.failure',
           'twisted.python.filepath',
           'twisted.python.log',
           'twisted.python.modules',
           'twisted.python.reflect',
           'twisted.python.runtime',
           'twisted.python.threadable',
           'twisted.python.util',
           'twisted.python.versions',
           'twisted.python.win32',
           'twisted.python.zippath']

ref = 'master'
#url = self._build_url('contents', directory_path, base_url=self._api)
#json = self._json(self._get(url, params={'ref': ref}), 200) or []
#['If-Modified-Since']

#return return_as((j.get('name'), Contents(j, self)) for j in json)
#base_url ='https://api.github.com/repos/KGerring/mdls'
#github3.repos.contents
#github3.gists.history
#'last_modified', 'sha', 'type', 'name', 'path'

class GitHubRepository(Repository):
	_create_file ='(path, message, content, branch=None, committer=None, author=None)'
	_contents = dict()
	
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
		contents = path_contents(self=self, path=initial_path, ref=ref, return_as=dict)
		__docs__ = contents.get('__docs__')
		while len(__docs__) > 0:
			path = __docs__.pop()
			new_contents = path_contents(self, path=path, ref=ref)
			contents = merge(new_contents, contents)
		
		contents.pop('__docs__')
		self._contents = contents.copy()
		return contents
	

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
	contents= path_contents(self=self, path=initial_path, ref=ref, return_as = dict)
	__docs__ = contents.get('__docs__')
	while len(__docs__) > 0:
		path = __docs__.pop()
		new_contents = path_contents(self, path=path, ref=ref)
		contents = merge(new_contents, contents)
		
	contents.pop('__docs__')
	return contents




cr = create_file#'(self, path, message, content, branch=None,  committer=None, author=None)'
	#json = self._json(self._put(url, data=dumps(data)), 201)
#'%a, %d %b %Y %T %Z'
TIMEFMT = '%a, %d %b %Y %H:%M:%S %Z'
#from pathlib import _PreciseSelector, _RecursiveWildcardSelector, _Selector, _TerminatingSelector, _WildcardSelector

#p = subprocess.Popen(['ls', '/Users/kristen/PycharmProjects/proj/mdls'], stdout=-1)
#substitutions, 0 insertions, 1 deletions

topdown=True
followlinks=True

from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

with NamedTemporaryFile() as f:
	check_call(['ls', '-l'], stdout=f, stderr=STDOUT)
	f.seek(0)
	output = f.read()


	
	

def walk(top='.', topdown=True, onerror=None, followlinks=True):
	for root, dirs, files in os.walk(top=top, topdown=topdown, followlinks=followlinks):
		if '__pycache__' in dirs:
			dirs.remove('__pycache__')
		
		if dirs:
			for filedir in dirs:
				#do stuff
				if filedir.__contains__('.'):
					print('HIDDEN', join(root, filedir))
				else:
					print('DIR', join(root, filedir))
		if files:
			for file in files:
				if file.endswith('plist'):
					print('PLIST', join(root, file))
				else:
					print('FILE', join(root, file))
				
				
	

def _select_from(self, parent_path, is_dir, exists, scandir):
	try:
		yielded = set()
		try:
			successor_select = self.successor._select_from
			for starting_point in self._iterate_directories(parent_path, is_dir, scandir):
				for p in successor_select(starting_point, is_dir, exists, scandir):
					if p not in yielded:
						yield p
						yielded.add(p)
		finally:
			yielded.clear()
	except PermissionError:
		return


popen = subprocess.Popen

ACK = '/usr/local/bin/ack'
#drv, root, pattern_parts = self._flavour.parse_parts((pattern,))
#file -s /dev/wd0{b,d}
#selector = _make_selector(("**",) + tuple(pattern_parts))
#for p in selector.select_from(self): yield p
#_make_child
#_make_child_relpath
' --match PATTERN --sort-files --show-types'
output="--output='$&'"
'shell=False, cwd=None, env=None'

#url = self._build_url('repos', owner, repository)
#url = self._build_url('repositories', str(number))

#require_module
#qual
#namedAny
#get_bundle_id_for_app
#get_build_platform
#getClass
#fullyQualifiedName
#filenameToModuleName
#by_extension
#METADATA_OPTIONS
#DirectoryLocator
#DATESTR
#CONFIG_FILE

key = get_keychain()
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


__PRIVATE = 'https://github.com/KGerring.private.atom?token=AKUqm8H1XbIz-Awrgiu_DZyEF8mjZv3iks627pR0wA=='
__ACTOR = 'https://github.com/KGerring.private.actor.atom?token=AKUqm5ROwW4W1q8fC1778xlv07y2Q3MIks627pbYwA=='

#logins = key.get_values('github', ('login', 'password', 'token', 'client_id', 'client_secret'))
#os.path.join(dirpath, name)
#dirpath, dirnames, filenames
#walk(top, topdown=True, onerror=None, followlinks=False)
#version_control = vcs.get_backend_from_location(location)
#return version_control().get_src_requirement(dist,location)
#return dist.as_requirement()




def get_relative_path(): pass



class GitHelper(object):
	def __init__(self, github=None, keychain=None):
		self.keychain = keychain or get_keychain()
		self.github = github or get_github()
		self.gists =[]
		self.repositories = dict()
		self.repo_names = set([])
	
	def iter_repos(self):
		for repository in self.github.repositories(sort='updated',number=-1):
			fullname = repository.full_name
			self.repo_names.add(fullname)
			user, name = repository.full_name.rsplit('/',1)
			self.repositories.update({name: repository})
			
	def ensure_repository(self, **kwargs):
		repository = kwargs.get('repository', None)
		if not repository or not isinstance(repository, Repository):
			repository = self.github.create_repository(**kwargs)
			assert isinstance(repository, Repository)
			name = kwargs.get('name', repository.name)
			self.repositories.update({name: repository})
			self.repo_names.add(repository.fullname)
		return repository
	
	def ensure_file(self, repository, filename, **kwargs):
		ADDED_TEMPLATE = 'added file: {!s}'
		UPDATED_TEMPLATE = '{}'
		try:
			contents = repository.directory_contents(filename)
		except AttributeError:
			contents = repository.file_contents(filename)
			if isinstance(contents, NullObject):
				return 'file {!r}'.format(str(contents)) ##todo
			
	def update_file(self, repository, filename, localfilename, localdir=None):
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
				createfile = repository.create_file(path=localfilename, message=message, content=content)
				print(message)
			


			
			
			
			
			#file = repository.create_file(path=filename, message=message, content=content)
		
		
		
		#if not isinstance(repository, Repository):
		#	repo_name = DirPath.name
		#	repository = self.github.create_repository(name=repo_name)
		#	self.repositories.update({repo_name: repository})
		#	assert isinstance(repository, Repository)
		
	def add_new_files_to_repository(self, repository=None, local_dir=os.getcwd()):
		from pathlib import Path
		from github3.null import NullObject
		from github3.repos.repo import Repository
		TEMPLATE = 'added file: {!s}'
		contents = []
		DirPath = Path(local_dir[:])
		repository = self.ensure_repository(repository=repository, name=DirPath.name)
		
		# children = DirPath.rglob('*.py')
		for child in DirPath.rglob('*.py'):
			relative = child.relative_to(DirPath).as_posix()
			###Check if recent or exists
			content = child.read_bytes()
			message = TEMPLATE.format(relative)
			file = repository.create_file(path=relative, message=message, content=content)
			if file:
				contents.append(file)
				print(message)
		return contents
	
	#@staticmethod
				
	def iter_files(self, repository):
		FILEPATHS = set([])
		for commit in repository.commits():
			freshened = commit.refresh()
			for file in freshened.files:
				if file.get('status') in ('added', 'modified'):
					FILEPATHS.add(file.get('filename'))
		return FILEPATHS
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					#contents = repo.directory_contents('path/to/dir/', return_as=dict)

#set_client_id


#GH.create_repository('startups', 'A collection of scripts to run that simplify development and usage (mainly convenience functions).',#homepage= 'http://pypi.python.org/pypi/mdls', private=False, gitignore_template='python')



def add_new_files_to_repository(github, repository=None, local_dir=os.getcwd()):
	from pathlib import Path
	from github3.null import NullObject
	from github3.repos.repo import Repository
	TEMPLATE = 'added file: {!s}'
	contents = []
	DirPath = Path(local_dir[:])
	if not isinstance(repository, Repository):
		repo_name = DirPath.name
		repository = github.create_repository(name=repo_name)
		assert isinstance(repository, Repository)
		
	#children = DirPath.rglob('*.py')
	for child in DirPath.rglob('*.py'):
		relative = child.relative_to(DirPath).as_posix()
		content = child.read_bytes()
		message = TEMPLATE.format(relative)
		file = repository.create_file(path=relative, message=message, content=content)
		if file:
			contents.append(file)
			print(message)
	return contents
		
		

	#path, message, content








def search_repositories(self, lanuage='Python', _in='name,description,readme', size=None, forks=None, fork=None,
	created=None, user=None,topic=None, topics=None): pass

def search_code(self, _in='file,path', filename=None, extension=None,user=None, repo=None):
	"""filename:.vimrc commands
	"""
	

code_help='''
minitest filename:test_helper path:test language:ruby Finds Ruby files containing the word "minitest" named *test_helper* within the *test* directory.

icon size:>200000 extension:css Finds files larger than 200 KB that end in .css and have the word "icon" in them.
console path:app/public language:javascript Finds JavaScript files with the word "console" in an app/public directory (even if they reside in app/public/js/form-validators).'''





def repositories(self, type='all', sort='created',direction='desc',number=-1):
	"""
	:param type: ('all', 'owner', 'public', 'private', 'member')
	:param sort: ('created', 'updated', 'pushed', 'full_name')
	:param direction:('asc', 'desc'), API default: 'asc' when using 'full_name', 'desc' otherwise
	:param number: -1 if all
	:return:
	"""
	return list(self.repositories(type=type, sort=sort, direction=direction, number=number))
	

#
def issues(filter='assigned', state='open', number=-1, since='', sort='created'): #labels='bug,ui,@high'
	"""
	:param filter: ('assigned', 'created', 'mentioned', 'subscribed')
	:param state: ('all', 'open', 'closed')
	:param str labels: comma-separated list of label names, e.g., 'bug,ui,@high'
	:param number:
	:param since:
	:param sort: ('created', 'updated', 'comments')
	:return:
	"""

def starred(self, sort='created', number=-1, direction='desc'):
	"""
	:param self: GitHub instance
	:param sort: either 'created' or 'updated'
	:param number: -1 for all, or limit total stars returned
	:param direction: either 'asc' or 'desc'
	:return: starred repositories
	"""
	return list(self.starred(sort=sort, number=number, direction=direction))





def subscriptions(self, number=-1):
	return list(self.subscriptions())

def teams(self):pass

def authorizations(self, number=-1):
	return list(self.authorizations(number=number))

def feeds(self):
	feeds =self.feeds()
	current_user_url = feeds['current_user_url'].expand()
	current_user_actor_url = feeds['current_user_actor_url'].expand()
	current_user_organization_urls = []
	for url in feeds['current_user_organization_urls']:
		current_user_organization_urls.append(url.expand())
	return dict(current_user_url=current_user_url, current_user_actor_url=current_user_actor_url,
	            current_user_organization_urls=current_user_organization_urls)



def get_github():
	from github3 import login
	from keyring.core import get_keyring
	key = get_keyring()
	token = key.get_password('github', 'token')
	password = key.get_password('github', 'password')
	username = key.get_password('github', 'login')
	client_id = key.get_password('github', 'client_id')
	client_secret = key.get_password('github', 'client_secret')
	GitHub = login(username=username, password=password, token=token)
	if client_id and client_secret:
		GitHub.set_client_id(id=client_id, secret=client_secret)
	me = GitHub.me()
	if me.type == 'User':
		return GitHub
	return None

def search_users(self, followers=None, sort='followers', created=None, language=None, location=None,repos=None,type='user'):

	"""in:email,login,fullname
	type:org,user
	repos>2000, repos:10..30
	 location:iceland
	 """
#IT.directory_contents
#IT.file_contents
#'frontpage-GET_canvasse'
#"wss://ws-04bea3c67e5f5289c.wss.redditmedia.com/place?m=AQAA-grjWG5ifSyTPAaDjiTPDZiKlPb_WywxQ_O3-XybT5voZZ1Y"


if __name__ == '__main__': print(__file__)