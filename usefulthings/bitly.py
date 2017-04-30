#!/usr/bin/env
# -*- coding: utf-8 -*-
# author=AutisticScreeching
# date = 3/8/17

import sys, os
import bitly_api
import bitly_api.bitly_api
import bitly_api.bitly_http
from requests import session
from requests.auth import _basic_auth_str
import webbrowser
import Foundation
import re
import time



class BitLink(dict):
	def __init__(self, **kwargs):
		super(BitLink, self).__init__(**kwargs)
		for k,v in kwargs.items():
			setattr(self, k,v)
			
	def __repr__(self):
		if self.link:
			return '{} ({!r})'.format(self.__class__.__name__, self.link)
		else:
			return '{}'.format(self.__class__.__name__)
		




INFO = 'http://dev.bitly.com/links.html#v3_expand'
HEADERS = {'X-Requested-With': 'XMLHttpRequest'}
ACCESS_TOKEN_URL ='https://api-ssl.bitly.com/oauth/access_token'

SCRIPTS = dict(
		SAFARI='tell application "Safari" to return URL of front document',
		CHROME='tell application "Google Chrome" to return URL of active tab of front window',
		OTHER='tell application "Finder" to set activePath to (POSIX path of (target of window 1 as alias))')

AS = Foundation.NSAppleScript.alloc().initWithSource_(
	'tell application "Google Chrome" to return URL of active tab of front window')
e = AS.executeAndReturnError_(None)[0].stringValue()


API_PATH = dict(
	referrers ='v3/referrers',
	clicks_day ="/v3/link/clicks?unit=day",
	link_lookup = 'user/link_lookup?url={url}')

api_key = 'R_3a106980300143279990c9f68cb5c27f'
client_id = 'ab33f473989024738fac8bd2d0010ee53a9377d8'
client_secret = '88c9307ee0cbc8918b28d1101fc49c923fa038ef'
redirect_uri = 'https://oursexploration.net/callbacks/'
access_token = 'defc7bd4dfe5b9173a6881c3d1bda396542c00ca'

token = 'dd78859808f525e3a1bf5256cef875053b9064c0'


__EX = 'access_token=defc7bd4dfe5b9173a6881c3d1bda396542c00ca&login=kgerring&apiKey=R_3a106980300143279990c9f68cb5c27f'


def get_authorize_url(client_id, client_secret, code, redirect_uri, state='state', grant_type='authorization_code'):
	Accept = 'application/json'
	params = dict(client_id=client_id, redirect_uri=redirect_uri, state=state)
	auth_url = prepare_url(root_url ='https://bitly.com/oauth/authorize', query_params=params)
	webbrowser.get('chrome').open(str(auth_url))
	
	CHROME = 'tell application "Google Chrome" to return URL of active tab of front window'
	AppleScript = Foundation.NSAppleScript.alloc().initWithSource_(CHROME)
	time.sleep(20)
	code_url = AppleScript.executeAndReturnError_(None)[0].stringValue()
	#cmd("""osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'""")
	code = re.search('code=(.+)&?', code_url)
	token_url = 'https://api-ssl.bitly.com/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}'
	result = post(token_url)
	return dict([t.split('=', 1) for t in result.text.split('&')])


def resource_owner_credential_grant(username, password, client_id,client_secret):
	grant_type = 'password'
	http_session = session()
	params = dict(username=username, password=password, grant_type='password')
	url = prepare_url(root_url='https://api-ssl.bitly.com/oauth/access_token', query_params=params)
	auth = _basic_auth_str(client_id, client_secret)
	http_session.headers['Authorization'] = auth
	data= http_session.post(str(url))
	if data.status_code == 200:
		return data.json().get('access_token')



def http_basic_authentication(username, password, client_id=None, client_secret=None):
	curl = 'curl -u "{username}:{password}" -X POST "https://api-ssl.bitly.com/oauth/access_token --silent"'
	return curl
	


def prepare_url(*args, **kwargs):
	from furl import furl
	root_url = kwargs.get('root_url', 'https://api-ssl.bitly.com/v3')
	url = furl()
	url = url.load(root_url)
	
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

def prepare_link(*args, **kwargs):
	from urlobject import URLObject
	root_url = kwargs.get('root_url', 'https://api-ssl.bitly.com/v3')
	url = URLObject(root_url)
	
	path = url.path
	query = url.query
	return dict(url=url, path=path, query=query)
	
	
link = 'https://api-ssl.bitly.com/v3/user/link_history?access_token='


class Bitly(object):
	OAUTH_URL = 'https://bitly.com/oauth'
	ACCESS_TOKEN_PATH = 'https://api-ssl.bitly.com/oauth/access_token'
	VERSION = 'v3'
	
	def __init__(self, login='kgerring', api_key='R_3a106980300143279990c9f68cb5c27f',
	             access_token='b12412226129d740bf227aaeccd80b29a08d9262',
	             secret='88c9307ee0cbc8918b28d1101fc49c923fa038ef', **kwargs):
		self.host = 'api.bit.ly'
		self.ssl_host = 'api-ssl.bit.ly'
		self.login = login
		self.api_key = api_key
		self.access_token = access_token
		self.secret = secret
		self.session = session()
		if self.access_token:
			self.session.params['access_token'] = self.access_token
			
		self.units = ("minute", "hour", "day", "week", "mweek", "month")
		
		self.authorize = 'https://bitly.com/oauth/authorize?client_id=ab33f473989024738fac8bd2d0010ee53a9377d8&state=state&redirect_uri=https://oursexploration.net/callbacks/'

		if kwargs:
			for k,v in kwargs.items():
				self.__setattr__(k,v)
				print('attribute {} set'.format(k))
	
	@staticmethod
	def prepare_url(*args, **kwargs):
		from furl import furl
		root_url = kwargs.get('root_url', 'https://api-ssl.bitly.com/v3')
		url = furl()
		url = url.load(root_url)
		
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
	
	def prepare_session(self):
		self.session = session()
		self.session.params['access_token'] = self.access_token
		self.session.headers['Accept'] = 'application/json'
	
	def EX(self): return 'https://api-ssl.bitly.com/v3/user/info?access_token={access_token}'
	
	def get_access_token(self, code, redirect_uri):
		params = dict(code=code, redirect_uri=redirect_uri)
		url = self.prepare_url(root_url='https://api-ssl.bitly.com/oauth/access_token', query_params=params)
		return str(url)
	
	def _call(self, path, params=None, method='GET', secret=None, timeout=5000):
		if not params:
			params = dict()
		params['format'] = params.get('format', 'json')  # default to json
		if self.access_token:
			params['access_token'] = self.access_token
		else:
			scheme = 'http'
			params['login'] = self.login
			params['apiKey'] = self.api_key
		
		url = str(self.prepare_url(path=path, query_params=params))
		if method == 'GET':
			response = self.session.get(url)
			if response.status_code == 200:
				return response.json()
			
		elif method == 'POST':
			response = self.session.post(url)
			if response.status_code == 200:
				return response.json()
	
	def expand(self, shortUrl, hash=None):
		"""The maximum number of shortUrl and hash parameters is 15."""
		params = dict(shortUrl=shortUrl)
		data = self._call('expand', params=params)
		return data.get('data').get('expand')
	
	def info(self, hash=None, shortUrl=None, link=None):
		"""Get info about a short-link by hash, shortUrl (aka link)
		:param hash:
		:param shortUrl:
		:param link:
		:return: `created_at`, `global_hash`, `hash`, `title`, `user_hash` params
		"""
		if link and not shortUrl:
			shortUrl = link
		if not hash and not shortUrl:
			pass
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		data = self._call('info', params)
		return data['data']['info']
	
	def shorten(self, uri, x_login=None, x_apiKey=None, preferred_domain=None):
		""" creates a bitly link for a given long url
		        @parameter uri: long url to shorten
		        @parameter x_login: login of a user to shorten on behalf of
		        @parameter x_apiKey: apiKey of a user to shorten on behalf of
		        @parameter preferred_domain: bit.ly[default], bitly.com, or j.mp
		        """
		params = dict(uri=uri)
		if preferred_domain:
			params['domain'] = preferred_domain
		if x_login:
			params.update({
				'x_login':  x_login,
				'x_apiKey': x_apiKey})
		data = self._call('shorten', params, self.secret)
	
	def user_info(self, expand_client_id=True):
		params = dict()
		if expand_client_id:
			params = dict(expand_client_id='true')
		return self._call('user/info', params=params).get('data')
	
	
	def link_lookup(self, longUrl):
		"""Look up a previously-shortened link by the authenticated user
		:param longUrl: The url to look up
		:return: `aggregate_link` and `url`
		"""
		params = dict(url=longUrl)
		data = self._call('link/lookup', params=params)
		return data.get('data').get('link_lookup')

	
	def user_link_history(self, created_before=None, created_after=None,
	                      archived=None, limit=None, offset=None,
	                      private=None):
		params = dict()
		if created_before is not None:
			assert isinstance(limit, int)
			params["created_before"] = created_before
		if created_after is not None:
			assert isinstance(limit, int)
			params["created_after"] = created_after
		if archived is not None:
			assert isinstance(archived, str)
			archived = archived.lower()
			assert archived is "on" or "off" or "both"
			params["archived"] = archived
		if private is not None:
			assert isinstance(private, str)
			private = private.lower()
			assert private is "on" or "off" or "both"
			params["private"] = private
		if limit is not None:
			assert isinstance(limit, int)
			params["limit"] = str(limit)
		if offset is not None:
			assert isinstance(offset, int)
			params["offset"] = str(offset)
			
		url = self.prepare_url('user/link_history', params)
		response = self.session.get(str(url))
		if response.status_code == 200:
			return response.json().get('data').get('link_history')
			
	
	def link_info(self, link='http://bit.ly/2lyUsex'):
		params = dict(link=link)
		url = self.prepare_url('link/info', {'link': l})
		response =self.session.get(str(url))
		if response.status_code == 200:
			return response.json().get('data')

	def shorten_counts(self, **kwargs):
		params= dict()
		if kwargs:
			params.update(kwargs)
		
		data = self._call('user/shorten_counts', params=params)
		return data.get('data')
	
	
	def referrers(self):
		data = self._call('user/referrers')
		return data.get('data').get('referrers')
	
	def popular_links(self):
		return self._call('user/popular_links')
	
	def countries(self):
		data= self._call('user/countries')
		return data.get('data').get('countries')
	
	def user_clicks(self):
		data= self._call('user/clicks')
		return data.get('data').get('clicks')
	
	def link_countries(self, link):
		params = dict(link=link)
		return self._call('link/countries', params=params)['data']['countries']
		
	def link_referrers(self, link):
		params = dict(link=link)
		data = self._call('link/referrers', params=params)
		return data.get('data').get('referrers')
	
	def link_referrers_by_domain(self, link):
		params = dict(link=link)
		data = self._call('link/referrers_by_domain', params=params)
		return data.get('data').get('referrers')
		
	def link_clicks(self, link, unit='day'):
		params = dict(link=link, unit=unit)
		data = self._call('link/clicks', params=params)
		return data.get('data').get('link_clicks')
		
	def popular_links(self):
		return self._call('user/popular_links')['data']['popular_links']

	

	def _call_oauth2(self, endpoint, params):
		assert self.access_token, "This %s endpoint requires OAuth" % endpoint
		return self._call(endpoint, params)["data"]
	
	def _call_oauth2_metrics(self, endpoint, params, unit=None, units=None,
	                         tz_offset=None, rollup=None, limit=None,
	                         unit_reference_ts=None):
		if unit is not None:
			assert unit in ("minute", "hour", "day", "week", "mweek", "month")
			params["unit"] = unit
		if units is not None:
			assert isinstance(units, int), "Unit (%r) must be integer" % units
			params["units"] = units
		if tz_offset is not None:
			# tz_offset can either be a hour offset, or a timezone like
			# North_America/New_York
			if isinstance(tz_offset, int):
				msg = "integer tz_offset must be between -12 and 12"
				assert -12 <= tz_offset <= 12, msg
			else:
				assert isinstance(tz_offset, str)
			params["tz_offset"] = tz_offset
		if rollup is not None:
			assert isinstance(rollup, bool)
			params["rollup"] = "true" if rollup else "false"
		if limit is not None:
			assert isinstance(limit, int)
			params["limit"] = limit
		if unit_reference_ts is not None:
			assert (unit_reference_ts == 'now' or
			        isinstance(unit_reference_ts, int))
			params["unit_reference_ts"] = unit_reference_ts
		
		return self._call_oauth2(endpoint, params)
	
	def search(self, query, offset=None, cities=None, domain=None, fields=None,
	           limit=10, lang='en'):
		params = dict(query=query, lang=lang)
		if offset:
			assert isinstance(offset, int)
			params["offset"] = str(offset)
		if cities:  # TODO: check format
			assert isinstance(cities, str)
			params["cities"] = cities
		if domain:
			assert isinstance(domain, str)
			params["domain"] = domain
		if fields:
			assert isinstance(fields, str)
			params["fields"] = fields
		data = self._call_oauth2_metrics("search", params, limit=limit)
		return data['results']
	
	
	def user_link_edit(self, link, edit, title=None, note=None, private=None,
	                   user_ts=None, archived=None):
		params = dict()
		params['link'] = link
		params['edit'] = edit
		if title is not None:
			params['title'] = str(title)
		if note is not None:
			params['note'] = str(note)
		if private is not None:
			params['private'] = bool(private)
		if user_ts is not None:
			params['user_ts'] = user_ts
		if archived is not None:
			params['archived'] = archived
		data = self._call("user/link_edit", params)
		
		return data['link_edit']
	
	def user_link_save(self, longUrl=None, long_url=None, title=None,
	                   note=None, private=None, user_ts=None):
		params = dict()
		if not longUrl and not long_url:
			pass
		params['longUrl'] = longUrl or long_url
		if title is not None:
			params['title'] = str(title)
		if note is not None:
			params['note'] = str(note)
		if private is not None:
			params['private'] = bool(private)
		if user_ts is not None:
			params['user_ts'] = user_ts
		data = self._call("user/link_save", params)
		return data['link_save']
	
	
	def user_link_lookup(self, url=None, link=None):
		"""
		:param url: one or more long URLs to lookup.
		:param link: one or more Bitlinks to lookup.
		:return:
		"""
		if url and not link:
			params = dict(link=link)
		else:
			params = dict(url=url)
			
		data = self._call('user/link_lookup', params)
		return data.get('data').get('link_lookup')
	
	def app(self, client_id=None):
		if not client_id:
			params = dict(client_id=self.client_id)
		else:
			params = dict(client_id=client_id)
		data = self._call('oauth/app', params)
		return data.get('data')
	
	def __repr__(self):
		return '{} for {!r}'.format(self.__class__.__name__, self.login)
		


####
label ={'id':                    'Label_14',
 'labelListVisibility':   'labelShow',
 'messageListVisibility': 'show',
 'name':                  'Will',
 'type':                  'user'}
labels = 'STARRED', 'UNREAD', 'SENT', 'CHAT', 'IMPORTANT'

auth = 'https://bitly.com/oauth/authorize?client_id=ab33f473989024738fac8bd2d0010ee53a9377d8&state=state&redirect_uri=https://oursexploration.net/callbacks/'



token = 'https://api-ssl.bitly.com/oauth/access_token?grant_type=password&d&username=kgerring&password=ekalb4393'

tok = 'https://api-ssl.bitly.com/oauth/access_token?client_id=ab33f473989024738fac8bd2d0010ee53a9377d8&client_secret=88c9307ee0cbc8918b28d1101fc49c923fa038ef&code={}9&redirect_uri=https://oursexploration.net/callbacks/'



curl = 'curl -u "ab33f473989024738fac8bd2d0010ee53a9377d8:88c9307ee0cbc8918b28d1101fc49c923fa038ef" -d "grant_type=password" -d "username=kgerring" -d "password=ekalb4393" https://api-ssl.bitly.com/oauth/access_token --silent'



ini = '/Users/kristen/.config/pythonista'
INI = '/Users/kristen/.config/revealme.ini'

#api_key = 'R_3a106980300143279990c9f68cb5c27f'
#client_id = 'ab33f473989024738fac8bd2d0010ee53a9377d8'
#client_secret = '88c9307ee0cbc8918b28d1101fc49c923fa038ef'
#redirect_uri = 'https://oursexploration.net/callbacks/'
#access_token = 'defc7bd4dfe5b9173a6881c3d1bda396542c00ca'
#access_token = 'b12412226129d740bf227aaeccd80b29a08d9262'
#token = 'dd78859808f525e3a1bf5256cef875053b9064c0'




user_info = 'https://api-ssl.bitly.com/v3/user/info?access_token={access_token}'

link_history = 'https://api-ssl.bitly.com/v3/user/link_history?access_token=b12412226129d740bf227aaeccd80b29a08d9262'
expand = 'https://api-ssl.bitly.com/v3/expand?access_token=b12412226129d740bf227aaeccd80b29a08d9262&shortUrl=http://bit.ly/2lyE0uQ'
hist = 'https://api-ssl.bitly.com/v3/user/link_history?access_token=b12412226129d740bf227aaeccd80b29a08d9262&expand_client_id=true'

LH = '[{"archived": false, "user_ts": 1488490889, "title": "Untitled", "created_at": 1488490889, "tags": [], "modified_at": 1488490889, "campaign_ids": [], "private": true, "aggregate_link": "http://bit.ly/2lyUsex", "long_url": "https://oursexploration.net/callbacks/", "client_id": {"app_link": "http://oursexploration.net/bitwhores/", "app_name": "bitwhores", "client_id": "ab33f473989024738fac8bd2d0010ee53a9377d8", "app_description": "Basic utilities, with a touch of sass..."}, "link": "http://bit.ly/2lyE0uQ"}, {"archived": false, "user_ts": 1465557112, "title": "Bitly. The power of the link.", "created_at": 1465557112, "tags": [], "modified_at": 1465557112, "campaign_ids": [], "private": true, "aggregate_link": "http://bit.ly/28pEcky", "long_url": "https://app.bitly.com/bitlinks/1qHW7Rr?actions=create", "client_id": {"app_name": "Bitly", "client_id": "ece654beaf35f9c29f610ffd4fb128702b4bad15", "app_link": "http://bitly.com/", "app_description": ""}, "link": "https://bitly.is/28pEckq"}, {"keyword_link": "http://bit.ly/pee_mark", "archived": false, "user_ts": 1464130728, "title": "Marking me with his pee | XTube Porn Video from Mystic86", "created_at": 1464130728, "tags": [], "modified_at": 1465557352, "campaign_ids": [], "private": true, "aggregate_link": "http://bit.ly/1qHVTK6", "long_url": "http://www.xtube.com/video-watch/Marking-me-with-his-pee-28316961", "shares": [{"remote_share_id": "17da45a635050a6161e5b1f376d9b5bed8be4b75", "share_id": "8c5de342-d199-40e4-884a-4e9aa95352fb", "ts": 1465557352000, "share_type": "email", "email": "easyeinstein@sluttyscience.com"}, {"remote_share_id": "7fc9770ab338ec54bf8caebcdc56206429a72c99", "share_id": "8c5de342-d199-40e4-884a-4e9aa95352fb", "ts": 1465557352000, "share_type": "email", "email": "kgerring@gmail.com"}], "client_id": {"app_link": "https://bitly.com/", "app_name": "Bitly API", "client_id": "a5e8cebb233c5d07e5c553e917dffb92fec5264d", "app_description": "Generic Bitly API Access Token for Developers"}, "link": "http://bit.ly/1qHW7Rr"}]'

lookup ='https://api-ssl.bitly.com/v3/link/lookup?url={url}&access_token={access_token}'


l = 'http://bit.ly/2lyE0uQ'
keyword = 'http://bit.ly/pee_mark'
link = 'http://bit.ly/1qHW7Rr'
user_hash = '1qHW7Rr'
long_url = 'http://www.xtube.com/video-watch/Marking-me-with-his-pee-28316961'


shorten = 'v3/shorten'
params = dict(uri='http://www.xtube.com/video-watch/Marking-me-with-his-pee-28316961')

shares0 = {'email':           'easyeinstein@sluttyscience.com',
           'remote_share_id': '17da45a635050a6161e5b1f376d9b5bed8be4b75',
           'share_id':        '8c5de342-d199-40e4-884a-4e9aa95352fb',
           'share_type':      'email',
           'ts':              1465557352000}

shares1 = {'email':           'kgerring@gmail.com',
           'remote_share_id': '7fc9770ab338ec54bf8caebcdc56206429a72c99',
           'share_id':        '8c5de342-d199-40e4-884a-4e9aa95352fb',
           'share_type':      'email',
           'ts':              1465557352000}

URL = 'https://raw.githubusercontent.com/bitly/bitly-api-python/master/bitly_api/bitly_api.py'


import hashlib
import json
import sys
import time
import types
import warnings

try:
	from urllib.request import build_opener, HTTPRedirectHandler
	from urllib.parse import urlencode
	from urllib.error import URLError, HTTPError
	
	string_types = str,
	integer_types = int,
	numeric_types = (int, float)
	text_type = str
	binary_type = bytes
except ImportError as e:
	from urllib.request import build_opener, HTTPRedirectHandler, URLError, HTTPError
	from urllib.parse import urlencode
	
	string_types = str,
	integer_types = (int)
	numeric_types = (int, float)
	text_type = str
	binary_type = str


class DontRedirect(HTTPRedirectHandler):
	def redirect_response(self, req, fp, code, msg, headers, newurl):
		if code in (301, 302, 303, 307):
			raise HTTPError(req.get_full_url(), code, msg, headers, fp)


class Error(Exception):
	pass


class BitlyError(Error):
	def __init__(self, code, message):
		Error.__init__(self, message)
		self.code = code


def _utf8(s):
	if isinstance(s, text_type):
		s = s.encode('utf-8')
	assert isinstance(s, binary_type)
	return s


def _utf8_params(params):
	"""encode a dictionary of URL parameters (including iterables) as utf-8"""
	assert isinstance(params, dict)
	encoded_params = []
	for k, v in list(params.items()):
		if v is None:
			continue
		if isinstance(v, numeric_types):
			v = str(v)
		if isinstance(v, (list, tuple)):
			v = [_utf8(x) for x in v]
		else:
			v = _utf8(v)
		encoded_params.append((k, v))
	return dict(encoded_params)


class Connection(object):
	"""
	This is a python library for accessing the bitly api
	http://github.com/bitly/bitly-api-python

	Usage:
		import bitly_api
		c = bitly_api.Connection('bitlyapidemo','R_{{apikey}}')
		# or to use oauth2 endpoints
		c = bitly_api.Connection(access_token='...')
		c.shorten('http://www.google.com/')
	"""
	
	def __init__(self, login=None, api_key=None, access_token=None,
	             secret=None):
		self.host = 'api.bit.ly'
		self.ssl_host = 'api-ssl.bit.ly'
		self.login = login
		self.api_key = api_key
		self.access_token = access_token
		self.secret = secret
		(major, minor, micro, releaselevel, serial) = sys.version_info
		parts = (major, minor, micro, '?')
		self.user_agent = "Python/%d.%d.%d bitly_api/%s" % parts
	
	def shorten(self, uri, x_login=None, x_apiKey=None, preferred_domain=None):
		""" creates a bitly link for a given long url
		@parameter uri: long url to shorten
		@parameter x_login: login of a user to shorten on behalf of
		@parameter x_apiKey: apiKey of a user to shorten on behalf of
		@parameter preferred_domain: bit.ly[default], bitly.com, or j.mp
		"""
		params = dict(uri=uri)
		if preferred_domain:
			params['domain'] = preferred_domain
		if x_login:
			params.update({
				'x_login':  x_login,
				'x_apiKey': x_apiKey})
		data = self._call(self.host, 'v3/shorten', params, self.secret)
		return data['data']
	
	def expand(self, hash=None, shortUrl=None, link=None):
		""" given a bitly url or hash, decode it and return the target url
		@parameter hash: one or more bitly hashes
		@parameter shortUrl: one or more bitly short urls
		@parameter link: one or more bitly short urls (preferred vocabulary)
		"""
		if link and not shortUrl:
			shortUrl = link
		
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/expand', params, self.secret)
		return data['data']['expand']
	
	def clicks(self, hash=None, shortUrl=None):
		"""
		given a bitly url or hash, get statistics about the clicks on that link
		"""
		warnings.warn("/v3/clicks is depricated in favor of /v3/link/clicks",
		              DeprecationWarning)
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/clicks', params, self.secret)
		return data['data']['clicks']
	
	def referrers(self, hash=None, shortUrl=None):
		"""
		given a bitly url or hash, get statistics about the referrers of that
		link
		"""
		warnings.warn("/v3/referrers is depricated in favor of "
		              "/v3/link/referrers", DeprecationWarning)
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/referrers', params, self.secret)
		return data['data']['referrers']
	
	def clicks_by_day(self, hash=None, shortUrl=None):
		""" given a bitly url or hash, get a time series of clicks
		per day for the last 30 days in reverse chronological order
		(most recent to least recent) """
		warnings.warn("/v3/clicks_by_day is depricated in favor of "
		              "/v3/link/clicks?unit=day", DeprecationWarning)
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/clicks_by_day', params, self.secret)
		return data['data']['clicks_by_day']
	
	def clicks_by_minute(self, hash=None, shortUrl=None):
		""" given a bitly url or hash, get a time series of clicks
		per minute for the last 30 minutes in reverse chronological
		order (most recent to least recent)"""
		warnings.warn("/v3/clicks_by_minute is depricated in favor of "
		              "/v3/link/clicks?unit=minute", DeprecationWarning)
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/clicks_by_minute', params,
		                  self.secret)
		return data['data']['clicks_by_minute']
	
	def link_clicks(self, link, **kwargs):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/clicks", params, **kwargs)
		return data["link_clicks"]
	
	def link_encoders(self, link, **kwargs):
		"""return the bitly encoders who have saved this link"""
		params = dict(link=link)
		data = self._call(self.host, 'v3/link/encoders', params, **kwargs)
		return data['data']
	
	def link_encoders_count(self, link, **kwargs):
		"""return the count of bitly encoders who have saved this link"""
		params = dict(link=link)
		data = self._call(self.host, 'v3/link/encoders_count', params,
		                  **kwargs)
		return data['data']
	
	def link_referring_domains(self, link, **kwargs):
		"""
		returns the domains that are referring traffic to a single bitly link
		"""
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/referring_domains", params,
		                                 **kwargs)
		return data["referring_domains"]
	
	def link_referrers_by_domain(self, link, **kwargs):
		"""
		returns the pages that are referring traffic to a single bitly link,
		grouped by domain
		"""
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/referrers_by_domain", params,
		                                 **kwargs)
		return data["referrers"]
	
	def link_referrers(self, link, **kwargs):
		"""
		returns the pages are are referring traffic to a single bitly link
		"""
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/referrers", params, **kwargs)
		return data["referrers"]
	
	def link_shares(self, link, **kwargs):
		"""return number of shares of a bitly link"""
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/shares", params, **kwargs)
		return data
	
	def link_countries(self, link, **kwargs):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/countries", params, **kwargs)
		return data["countries"]
	
	def user_clicks(self, **kwargs):
		"""aggregate number of clicks on all of this user's bitly links"""
		data = self._call_oauth2_metrics('v3/user/clicks', dict(), **kwargs)
		return data
	
	def user_countries(self, **kwargs):
		"""
		aggregate metrics about countries from which people are clicking on all
		of a user's bitly links
		"""
		data = self._call_oauth2_metrics('v3/user/countries', dict(), **kwargs)
		return data["countries"]
	
	def user_popular_links(self, **kwargs):
		data = self._call_oauth2_metrics("v3/user/popular_links", dict(),
		                                 **kwargs)
		return data["popular_links"]
	
	def user_referrers(self, **kwargs):
		"""
		aggregate metrics about the referrers for all of the authed user's
		bitly links
		"""
		data = self._call_oauth2_metrics("v3/user/referrers", dict(), **kwargs)
		return data["referrers"]
	
	def user_referring_domains(self, **kwargs):
		"""
		aggregate metrics about the domains referring traffic to all of the
		authed user's bitly links
		"""
		data = self._call_oauth2_metrics("v3/user/referring_domains", dict(),
		                                 **kwargs)
		return data["referring_domains"]
	
	def user_share_counts(self, **kwargs):
		"""number of shares by authed user in given time period"""
		data = self._call_oauth2_metrics("v3/user/share_counts", dict(),
		                                 **kwargs)
		return data["share_counts"]
	
	def user_share_counts_by_share_type(self, **kwargs):
		"""
		number of shares by authed user broken down by type (facebook, twitter,
		email) in a give time period
		"""
		data = self._call_oauth2_metrics("v3/user/share_counts_by_share_type",
		                                 dict(), **kwargs)
		return data["share_counts_by_share_type"]
	
	def user_shorten_counts(self, **kwargs):
		data = self._call_oauth2_metrics("v3/user/shorten_counts", dict(),
		                                 **kwargs)
		return data["user_shorten_counts"]
	
	def user_tracking_domain_list(self):
		data = self._call_oauth2("v3/user/tracking_domain_list", dict())
		return data["tracking_domains"]
	
	def user_tracking_domain_clicks(self, domain, **kwargs):
		params = dict(domain=domain)
		data = self._call_oauth2_metrics("v3/user/tracking_domain_clicks",
		                                 params, **kwargs)
		return data["tracking_domain_clicks"]
	
	def user_tracking_domain_shorten_counts(self, domain, **kwargs):
		params = dict(domain=domain)
		data = self._call_oauth2_metrics(
			"v3/user/tracking_domain_shorten_counts", params, **kwargs)
		return data["tracking_domain_shorten_counts"]
	
	def user_info(self, **kwargs):
		"""return or update info about a user"""
		data = self._call_oauth2("v3/user/info", kwargs)
		return data
	
	def user_link_history(self, created_before=None, created_after=None,
	                      archived=None, limit=None, offset=None,
	                      private=None):
		params = dict()
		if created_before is not None:
			assert isinstance(limit, integer_types)
			params["created_before"] = created_before
		if created_after is not None:
			assert isinstance(limit, integer_types)
			params["created_after"] = created_after
		if archived is not None:
			assert isinstance(archived, string_types)
			archived = archived.lower()
			assert archived is "on" or "off" or "both"
			params["archived"] = archived
		if private is not None:
			assert isinstance(private, string_types)
			private = private.lower()
			assert private is "on" or "off" or "both"
			params["private"] = private
		if limit is not None:
			assert isinstance(limit, integer_types)
			params["limit"] = str(limit)
		if offset is not None:
			assert isinstance(offset, integer_types)
			params["offset"] = str(offset)
		data = self._call_oauth2("v3/user/link_history", params)
		return data["link_history"]
	
	def user_network_history(self, offset=None, expand_client_id=False,
	                         limit=None, expand_user=False):
		params = dict()
		if expand_client_id is True:
			params["expand_client_id"] = "true"
		if expand_user is True:
			params["expand_user"] = "true"
		if offset is not None:
			assert isinstance(offset, integer_types)
			params["offset"] = str(offset)
		if limit is not None:
			assert isinstance(limit, integer_types)
			params["limit"] = str(limit)
		data = self._call_oauth2("v3/user/network_history", params)
		return data
	
	def info(self, hash=None, shortUrl=None, link=None):
		""" return the page title for a given bitly link """
		if link and not shortUrl:
			shortUrl = link
		
		if not hash and not shortUrl:
			raise BitlyError(500, 'MISSING_ARG_SHORTURL')
		params = dict()
		if hash:
			params['hash'] = hash
		if shortUrl:
			params['shortUrl'] = shortUrl
		
		data = self._call(self.host, 'v3/info', params, self.secret)
		return data['data']['info']
	
	def link_lookup(self, url):
		"""query for a bitly link based on a long url (or list of long urls)"""
		params = dict(url=url)
		data = self._call(self.host, 'v3/link/lookup', params, self.secret)
		return data['data']['link_lookup']
	
	def lookup(self, url):
		""" query for a bitly link based on a long url """
		warnings.warn("/v3/lookup is depricated in favor of /v3/link/lookup",
		              DeprecationWarning)
		
		params = dict(url=url)
		
		data = self._call(self.host, 'v3/lookup', params, self.secret)
		return data['data']['lookup']
	
	def user_link_edit(self, link, edit, title=None, note=None, private=None,
	                   user_ts=None, archived=None):
		"""edit a link in a user's history"""
		params = dict()
		
		if not link:
			raise BitlyError(500, 'MISSING_ARG_LINK')
		
		if not edit:
			raise BitlyError(500, 'MISSING_ARG_EDIT')
		
		params['link'] = link
		params['edit'] = edit
		if title is not None:
			params['title'] = str(title)
		if note is not None:
			params['note'] = str(note)
		if private is not None:
			params['private'] = bool(private)
		if user_ts is not None:
			params['user_ts'] = user_ts
		if archived is not None:
			params['archived'] = archived
		
		data = self._call_oauth2("v3/user/link_edit", params)
		return data['link_edit']
	
	def user_link_lookup(self, url):
		"""
		query for whether a user has shortened a particular long URL. don't
		confuse with v3/link/lookup.
		"""
		params = dict(url=url)
		data = self._call(self.host, 'v3/user/link_lookup', params,
		                  self.secret)
		return data['data']['link_lookup']
	
	def user_link_save(self, longUrl=None, long_url=None, title=None,
	                   note=None, private=None, user_ts=None):
		"""save a link into the user's history"""
		params = dict()
		if not longUrl and not long_url:
			raise BitlyError('500', 'MISSING_ARG_LONG_URL')
		params['longUrl'] = longUrl or long_url
		if title is not None:
			params['title'] = str(title)
		if note is not None:
			params['note'] = str(note)
		if private is not None:
			params['private'] = bool(private)
		if user_ts is not None:
			params['user_ts'] = user_ts
		
		data = self._call_oauth2("v3/user/link_save", params)
		return data['link_save']
	
	def pro_domain(self, domain):
		""" is the domain assigned for bitly.pro? """
		end_point = 'v3/bitly_pro_domain'
		
		if not domain:
			raise BitlyError(500, 'MISSING_ARG_DOMAIN')
		
		protocol_prefix = ('http://', 'https://')
		if domain.lower().startswith(protocol_prefix):
			raise BitlyError(500, 'INVALID_BARE_DOMAIN')
		params = dict(domain=domain)
		data = self._call(self.host, end_point, params, self.secret)
		return data['data']['bitly_pro_domain']
	
	def bundle_archive(self, bundle_link):
		"""archive a bundle for the authenticated user"""
		params = dict(bundle_link=bundle_link)
		data = self._call_oauth2_metrics("v3/bundle/archive", params)
		return data
	
	def bundle_bundles_by_user(self, user=None, expand_user=False):
		"""list bundles by user (defaults to authed user)"""
		params = dict()
		if user is not None:
			params["user"] = user
		if expand_user is True:
			params["expand_user"] = "true"
		data = self._call_oauth2_metrics("v3/bundle/bundles_by_user", params)
		return data
	
	def bundle_clone(self, bundle_link):  # TODO: 500s
		"""clone a bundle for the authenticated user"""
		params = dict(bundle_link=bundle_link)
		data = self._call_oauth2_metrics("v3/bundle/clone", params)
		return data
	
	def bundle_collaborator_add(self, bundle_link, collaborator=None):
		"""add a collaborator a bundle"""
		params = dict(bundle_link=bundle_link)
		if collaborator is not None:
			params["collaborator"] = collaborator
		data = self._call_oauth2_metrics("v3/bundle/collaborator_add", params)
		return data
	
	def bundle_collaborator_remove(self, bundle_link, collaborator):
		"""remove a collaborator from a bundle"""
		params = dict(bundle_link=bundle_link)
		params["collaborator"] = collaborator
		data = self._call_oauth2_metrics("v3/bundle/collaborator_remove",
		                                 params)
		return data
	
	def bundle_contents(self, bundle_link, expand_user=False):
		"""list the contents of a bundle"""
		params = dict(bundle_link=bundle_link)
		if expand_user:
			params["expand_user"] = "true"
		data = self._call_oauth2_metrics("v3/bundle/contents", params)
		return data
	
	def bundle_create(self, private=False, title=None, description=None):
		"""create a bundle"""
		params = dict()
		if private:
			params["private"] = "true"
		if title is not None:
			assert isinstance(title, string_types)
			params["title"] = title
		if description is not None:
			assert isinstance(description, string_types)
			params["description"] = description
		data = self._call_oauth2_metrics("v3/bundle/create", params)
		return data
	
	def bundle_edit(self, bundle_link, edit=None, title=None, description=None,
	                private=None, preview=None, og_image=None):
		"""edit a bundle for the authenticated user"""
		params = dict(bundle_link=bundle_link)
		if edit:
			assert isinstance(edit, string_types)
			params["edit"] = edit
		if title:
			assert isinstance(title, string_types)
			params["title"] = title
		if description:
			assert isinstance(description, string_types)
			params["description"] = description
		if private is not None:
			if private:
				params["private"] = "true"
			else:
				params["private"] = "false"
		if preview is not None:
			if preview:
				params["preview"] = "true"
			else:
				params["preview"] = "false"
		if og_image:
			assert isinstance(og_image, string_types)
			params["og_image"] = og_image
		data = self._call_oauth2_metrics("v3/bundle/edit", params)
		return data
	
	def bundle_link_add(self, bundle_link, link, title=None):
		"""add a link to a bundle"""
		params = dict(bundle_link=bundle_link, link=link)
		if title:
			assert isinstance(title, string_types)
			params["title"] = title
		data = self._call_oauth2_metrics("v3/bundle/link_add", params)
		return data
	
	def bundle_link_comment_add(self, bundle_link, link, comment):
		"""add a comment to a link in a bundle"""
		params = dict(bundle_link=bundle_link, link=link, comment=comment)
		data = self._call_oauth2_metrics("v3/bundle/link_comment_add", params)
		return data
	
	def bundle_link_comment_edit(self, bundle_link, link, comment_id, comment):
		"""edit a comment on a link in a bundle"""
		params = dict(bundle_link=bundle_link, link=link,
		              comment_id=comment_id, comment=comment)
		data = self._call_oauth2_metrics("v3/bundle/link_comment_edit", params)
		return data
	
	def bundle_link_comment_remove(self, bundle_link, link, comment_id):
		""" remove a comment on a link in a bundle"""
		params = dict(bundle_link=bundle_link, link=link,
		              comment_id=comment_id)
		data = self._call_oauth2_metrics("v3/bundle/link_comment_remove",
		                                 params)
		return data
	
	def bundle_link_edit(self, bundle_link, link, edit, title=None,
	                     preview=None):
		""" edit the title for a link """
		params = dict(bundle_link=bundle_link, link=link)
		if edit == "title":
			params["edit"] = edit
			assert isinstance(title, string_types)
			params["title"] = title
		elif edit == "preview":
			params["edit"] = edit
			assert isinstance(preview, bool)
			if preview:
				params["preview"] = "true"
			else:
				params["preview"] = "false"
		else:
			raise BitlyError(500,
			                 "PARAM EDIT MUST HAVE VALUE TITLE OR PREVIEW")
		data = self._call_oauth2_metrics("v3/bundle/link_edit", params)
		return data
	
	def bundle_link_remove(self, bundle_link, link):
		""" remove a link from a bundle """
		params = dict(bundle_link=bundle_link, link=link)
		data = self._call_oauth2_metrics("v3/bundle/link_remove", params)
		return data
	
	def bundle_link_reorder(self, bundle_link, link, display_order):
		""" reorder the links in a bundle"""
		params = dict(bundle_link=bundle_link, link=link,
		              display_order=display_order)
		data = self._call_oauth2_metrics("v3/bundle/link_reorder", params)
		return data
	
	def bundle_pending_collaborator_remove(self, bundle_link, collaborator):
		"""remove a pending collaborator from a bundle"""
		params = dict(bundle_link=bundle_link)
		params["collaborator"] = collaborator
		data = self._call_oauth2_metrics(
			"v3/bundle/pending_collaborator_remove", params)
		return data
	
	def bundle_view_count(self, bundle_link):
		""" get the number of views on a bundle """
		params = dict(bundle_link=bundle_link)
		data = self._call_oauth2_metrics("v3/bundle/view_count", params)
		return data
	
	def user_bundle_history(self):
		""" return the bundles that this user has access to """
		data = self._call_oauth2_metrics("v3/user/bundle_history", dict())
		return data
	
	def highvalue(self, limit=10, lang='en'):
		params = dict(lang=lang)
		data = self._call_oauth2_metrics("v3/highvalue", params, limit=limit)
		return data
	
	def realtime_bursting_phrases(self):
		data = self._call_oauth2_metrics("v3/realtime/bursting_phrases",
		                                 dict())
		return data["phrases"]
	
	def realtime_hot_phrases(self):
		data = self._call_oauth2_metrics("v3/realtime/hot_phrases", dict())
		return data["phrases"]
	
	def realtime_clickrate(self, phrase):
		params = dict(phrase=phrase)
		data = self._call_oauth2_metrics("v3/realtime/clickrate", params)
		return data["rate"]
	
	def link_info(self, link):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/info", params)
		return data
	
	def link_content(self, link, content_type="html"):
		params = dict(link=link, content_type=content_type)
		data = self._call_oauth2_metrics("v3/link/content", params)
		return data["content"]
	
	def link_category(self, link):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/category", params)
		return data["categories"]
	
	def link_social(self, link):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/social", params)
		return data["social_scores"]
	
	def link_location(self, link):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/location", params)
		return data["locations"]
	
	def link_language(self, link):
		params = dict(link=link)
		data = self._call_oauth2_metrics("v3/link/language", params)
		return data["languages"]
	
	def search(self, query, offset=None, cities=None, domain=None, fields=None,
	           limit=10, lang='en'):
		params = dict(query=query, lang=lang)
		if offset:
			assert isinstance(offset, integer_types)
			params["offset"] = str(offset)
		if cities:  # TODO: check format
			assert isinstance(cities, string_types)
			params["cities"] = cities
		if domain:
			assert isinstance(domain, string_types)
			params["domain"] = domain
		if fields:
			assert isinstance(fields, string_types)
			params["fields"] = fields
		data = self._call_oauth2_metrics("v3/search", params, limit=limit)
		return data['results']
	
	@classmethod
	def _generateSignature(self, params, secret):
		if not params or not secret:
			return ""
		hash_string = ""
		if not params.get('t'):
			# note, this uses a utc timestamp not a local timestamp
			params['t'] = str(int(time.mktime(time.gmtime())))
		
		keys = list(params.keys())
		keys.sort()
		for k in keys:
			if type(params[k]) in [list, tuple]:
				for v in params[k]:
					hash_string += v
			else:
				hash_string += params[k]
		hash_string += secret
		signature = hashlib.md5(hash_string).hexdigest()[:10]
		return signature
	
	def _call_oauth2_metrics(self, endpoint, params, unit=None, units=None,
	                         tz_offset=None, rollup=None, limit=None,
	                         unit_reference_ts=None):
		if unit is not None:
			assert unit in ("minute", "hour", "day", "week", "mweek", "month")
			params["unit"] = unit
		if units is not None:
			assert isinstance(units, integer_types), \
				"Unit (%r) must be integer" % units
			params["units"] = units
		if tz_offset is not None:
			# tz_offset can either be a hour offset, or a timezone like
			# North_America/New_York
			if isinstance(tz_offset, integer_types):
				msg = "integer tz_offset must be between -12 and 12"
				assert -12 <= tz_offset <= 12, msg
			else:
				assert isinstance(tz_offset, string_types)
			params["tz_offset"] = tz_offset
		if rollup is not None:
			assert isinstance(rollup, bool)
			params["rollup"] = "true" if rollup else "false"
		if limit is not None:
			assert isinstance(limit, integer_types)
			params["limit"] = limit
		if unit_reference_ts is not None:
			assert (unit_reference_ts == 'now' or
			        isinstance(unit_reference_ts, integer_types))
			params["unit_reference_ts"] = unit_reference_ts
		
		return self._call_oauth2(endpoint, params)
	
	def _call_oauth2(self, endpoint, params):
		assert self.access_token, "This %s endpoint requires OAuth" % endpoint
		return self._call(self.ssl_host, endpoint, params)["data"]
	
	def _call(self, host, method, params, secret=None, timeout=5000):
		params['format'] = params.get('format', 'json')  # default to json
		
		if self.access_token:
			scheme = 'https'
			params['access_token'] = self.access_token
			host = self.ssl_host
		else:
			scheme = 'http'
			params['login'] = self.login
			params['apiKey'] = self.api_key
		
		if secret:
			params['signature'] = self._generateSignature(params, secret)
		
		# force to utf8 to fix ascii codec errors
		params = _utf8_params(params)
		
		request = "%(scheme)s://%(host)s/%(method)s?%(params)s" % {
			'scheme': scheme,
			'host':   host,
			'method': method,
			'params': urlencode(params, doseq=1)
		}
		
		try:
			opener = build_opener(DontRedirect())
			opener.addheaders = [('User-agent', self.user_agent + ' urllib')]
			response = opener.open(request)
			code = response.code
			result = response.read().decode('utf-8')
			if code != 200:
				raise BitlyError(500, result)
			if not result.startswith('{'):
				raise BitlyError(500, result)
			data = json.loads(result)
			if data.get('status_code', 500) != 200:
				raise BitlyError(data.get('status_code', 500),
				                 data.get('status_txt', 'UNKNOWN_ERROR'))
			return data
		except URLError as e:
			raise BitlyError(500, str(e))
		except HTTPError as e:
			raise BitlyError(e.code, e.read())
		except BitlyError:
			raise
		except Exception:
			raise BitlyError(None, sys.exc_info()[1])

#
		
		