#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = facebook_chat
# author=SluttyScience
# date = 6/23/17
from startups import *
import sys, os
import fbchat
import fbchat.client
import fbchat.models
#import fbchat.stickers
import fbchat.utils
from startups.core import pythonize
from inflection import underscore, camelize
from six.moves.http_cookiejar import CookieJar
from grab.cookie import CookieManager
import re
from fbchat.utils import now, get_json
from fbchat.models import User as OldUser
#todo uploadImage
#todo sendLocalImage, sendRemoteImage
#todo list_mimetypes common

class User(OldUser):
	@property
	def deep_data(self):
		_data = getattr(self, 'data').get('data')
		if not hasattr(self, '_data'):
			setattr(self, '_data', _data)
			return getattr(self, '_data', _data)
		else:
			return self._data
		
	def is_friend(self):
		deep = getattr(self, '_data', self.deep_data)
		return deep.get('is_friend', False)

	@property
	def nickname(self):
		return getattr(self, '_nickname', None)
	
	@nickname.setter
	def nickname(self, name):
		if not hasattr(self, '_nickname'):
			setattr(self, '_nickname', name)
		else:
			self._nickname = name
			
	def __repr__(self):
		if not self.nickname:
			shortname = pythonize(self.name)
		else:
			shortname = self.nickname
		if self.is_friend():
			clsname = 'Friend'
		else:
			clsname = self.__class__.__name__
			
		return '<{!s} {!r} ({!r})>'.format(clsname, shortname, self.uid)
	def __str__(self):
		shortname = self.url
		if self.is_friend():
			clsname = 'Friend'
		else:
			clsname = self.__class__.__name__
		
		return '<{!s} {!r} ({!r})>'.format(clsname, shortname, self.uid)
		




URLS={'AllUsersURL': 'https://www.facebook.com/chat/user_info_all',
 'BaseURL': 'https://www.facebook.com',
 'CheckpointURL': 'https://m.facebook.com/login/checkpoint/',
 'ConnectURL': 'https://www.facebook.com/ajax/add_friend/action.php?dpr=1',
 'DeliveredURL': 'https://www.facebook.com/ajax/mercury/delivery_receipts.php',
 'LoginURL': 'https://m.facebook.com/login.php?login_attempt=1',
 'LogoutURL': 'https://www.facebook.com/logout.php',
 'MarkSeenURL': 'https://www.facebook.com/ajax/mercury/mark_seen.php',
 'MessagesURL': 'https://www.facebook.com/ajax/mercury/thread_info.php',
 'MobileURL': 'https://m.facebook.com/',
 'PingURL': 'https://0-channel-proxy-06-ash2.facebook.com/active_ping',
 'ReadStatusURL': 'https://www.facebook.com/ajax/mercury/change_read_status.php',
 'RemoveUserURL': 'https://www.facebook.com/chat/remove_participants/',
 'SaveDeviceURL': 'https://m.facebook.com/login/save-device/cancel/',
 'SearchURL': 'https://www.facebook.com/ajax/typeahead/search.php',
 'SendURL': 'https://www.facebook.com/messaging/send/',
 'StickyURL': 'https://0-edge-chat.facebook.com/pull',
 'ThreadSyncURL': 'https://www.facebook.com/ajax/mercury/thread_sync.php',
 'ThreadsURL': 'https://www.facebook.com/ajax/mercury/threadlist_info.php',
 'UploadURL': 'https://upload.facebook.com/ajax/mercury/upload.php',
 'UserInfoURL': 'https://www.facebook.com/chat/user_info/'}

#url_sub = re.compile(r'^(?P<word>[A-Za-z]+)(URL)$')
def shorten_url(word):
	import re
	url_sub = re.compile(r'^(?P<word>[A-Za-z]+)(URL)$')
	short = url_sub.sub('\g<word>', word)
	return underscore(short)
	
def lengthen_url(word):
	camel = camelize(word)
	return camel + 'URL'

SHORT_URLS = {shorten_url(k): v for k, v in URLS.items()}
URLS.update(SHORT_URLS)


COOKIE_ATTRS = ('name', 'value', 'version', 'port', 'domain',
				'path', 'secure', 'expires', 'discard', 'comment',
				'comment_url', 'rfc2109')

KEYS=['getAllUsers',
		'getSession',
		'getThreadInfo',
		'getThreadList',
		'getUnread',
		'getUserInfo',
		'getUsers']


def process_all_users(self):
	users = [(pythonize(user.name), user) for user in self.getAllUsers()]
	return AttrDict(users)

def get_facebook():
	key = get_keychain()
	email = key.get('facebook', 'email')
	password = key.get('facebook', 'password')
	client = fbchat.client.Client(email, password)
	if client.password:
		client.password = '******'
	return client

def get_self_sent_messages(client, limit = 50):
	ID = client.uid
	messages = client.fetchThreadMessages(thread_id=ID, limit = 50)
	return messages

def get_attached_url(message, with_title = False):
	from furl import furl
	ext = message.extensible_attachment
	if ext is not None:
		attachment = message.extensible_attachment.get('story_attachment')
		ex = attachment.get('url')
		durl = furl(ex).args
		url= durl.get('u', durl)
		if with_title:
			title = attachment.get('title_with_entities').get('text')
			return (url, title)
		else:
			return url
	
def get_attachment(message):
	uris = []
	for attachment in  message.attachments:
		if attachment.get('__typename').__contains__('Image'):
			uri =attachment.get('large_preview').get('uri')
			uris.append(uri)
	return uris
	

def get_main():
	from tabulate import tabulate
	FB = get_facebook()
	messages = get_self_sent_messages(FB, limit=50)
	URLS = []
	for message in messages:
		url = get_attached_url(message, with_title=True)
		if url:
			URLS.append(url)
	print(tabulate(URLS, tablefmt='grid', headers=['URL', 'TITLE']))
	return URLS
	

##
if __name__ == '__main__':
	from tabulate import tabulate
	FB = get_facebook()
	messages = get_self_sent_messages(FB, limit=50)
	URLS = []
	for message in messages:
		url = get_attached_url(message, with_title=True)
		if url:
			URLS.append(url)
	print(tabulate(URLS, tablefmt='grid', headers=['URL', 'TITLE']))