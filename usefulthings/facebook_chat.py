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
from fbchat.models import User as OldUser, Message as OldMessage
from usefulthings import datetime_stuff
from fbchat.client import graphql_to_message, graphql_response_to_json
from isodate import parse_datetime
FMTSTR = '%b %d,%l:%M%p'



PRIVATE_KEY_FILE= '/Users/kristen/.ssh/kgerring_rsa'
PUBLIC_KEY_FILE = '/Users/kristen/.ssh/kgerring_rsa.pub'

def load_rsa_keys(public='/Users/kristen/.ssh/kgerring_rsa.pub', private=PRIVATE_KEY_FILE):
	import rsa
	
	PUBLIC_KEY_FILE = os.path.expanduser('~/.ssh/kgerring_rsa.pub')
	PRIVATE_KEY_FILE = os.path.expanduser('~/.ssh/kgerring_rsa')
	PublicKey = rsa.PublicKey._load_pkcs1_pem(open(PUBLIC_KEY_FILE, 'rb').read())
	PrivateKey = rsa.PrivateKey._load_pkcs1_pem(open(PRIVATE_KEY_FILE, 'rb').read())
	return PublicKey, PrivateKey




def rsa_encrypt(message, public_key):
	from startups.core import encode, decode
	if not isinstance(message, bytes):
		message = encode(message)
		return rsa.encrypt(message, public_key)
	
def rsa_decrypt(encrypted, private_key):
	from startups.core import encode, decode
	decrypted = rsa.decrypt(encrypted, private_key)
	if isinstance(decrypted, bytes):
		return decode(decrypted)
	return decrypted


def rsa_sign(message, private_key, hash='MD5'):
	if not isinstance(message, bytes):
		message = encode(message)
	return rsa.sign(message, private_key, hash=hash)


def rsa_verify(message, signature, public_key):
	if not isinstance(message, bytes):
		message = encode(message)
	try:
		return rsa.verify(message, signature, public_key)
	except rsa.pkcs1.VerificationError:
		return False




#todo uploadImage
#todo sendLocalImage, sendRemoteImage
#todo list_mimetypes common

def to_datetime(timestamp, TS_FACTOR=1000):
	from datetime import datetime
	if isinstance(timestamp, str):
		ts = int(timestamp)
		ts = ts / TS_FACTOR
		return datetime.fromtimestamp(ts)
	elif isinstance(timestamp, int):
		ts = timestamp
		ts = ts / TS_FACTOR
		return datetime.fromtimestamp(ts)
	return None


params = {
	'id': '7202549',
	'message_limit': 20,
	'load_messages': True,
	'load_read_receipts': False,
	'before': None
}

def get_message_type(message):
	try_attach = message.attachments
	if message.attachments:
		return message.attachments[0].get('__typename')
	else: return 'Text'
		
		
#graphql_requests
#fetchThreadMessages
#fetchThreadInfo
#fb_h
#_getThread


def get_message_from(self, uid, limit=100, before=None):
	from fbchat.client import GraphQL
	params = dict()
	params['load_read_receipts'] = True
	params['before'] = before
	params['load_messages'] = True
	params['message_limit'] = limit
	params['id'] = uid
	j = self.graphql_request(GraphQL(doc_id='1386147188135407', params=params))
	return j



REACTIONS = dict(LOVE='😍', SMILE='😆',
                 WOW='😮',
                 SAD='😢',
                 ANGRY='😠',
                 YES='👍',
                 NO='👎')


def get_attachment(message):
	uris = []
	for attachment in message.attachments:
		if attachment.get('__typename').__contains__('Image'):
			uri = attachment.get('large_preview').get('uri')
			uris.append(uri)
	return uris

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
		
		

		
class Message(OldMessage):
	DATESTR = '%Y-%m-%dT%H:%M:%S'
	D = '%b %d,%l:%M%p'
	
	@property
	def _ts(self):
		return to_datetime(self.timestamp).strftime('%Y-%m-%dT%H:%M:%S')
	
	@property
	def name(self):
		if self.author == '7202549':
			return "Kristen"
		return "Michael"
	
	@property
	def ts(self):
		return to_datetime(self.timestamp).strftime('%b %d,%l:%M%p')
	
	def format(self, fmtstr='{} ({}):{}'):
		return fmtstr.format(self.name, self.ts, self.text)
	
	def __str__(self):
		return '{} ({}): {}'.format(self.name, self.ts, self.text)
	
	
	
	#@property
	#def attachment(self):
	#	uris = []
	#	for attachment in self.attachments:
	#		if attachment.get('__typename').__contains__('Image'):
	#			uri = attachment.get('large_preview').get('uri')
	#			uris.append(uri)
	#	return uris
	
	#def update_text(self):
	#	try:
	#		if self.text == '':
	#			self.text = self.attachment[0]
	#	except (AttributeError, IndexError, TypeError):
	#		pass
	
def safe_pickler(file, private_key):
	import rsa
	import json
	PRIVATE_KEY_FILE = '/Users/kristen/.ssh/kgerring_rsa'
	PrivateKey = rsa.PrivateKey._load_pkcs1_pem(open(PRIVATE_KEY_FILE, 'rb').read())
	
	if not private_key == PrivateKey:
		return
	else:
		return json.loads(unpickler(file))


def flatten(lst, out=None):
	"""
	Return a flattened version of C{lst}.
	"""
	if out is None: out = []
	for elt in lst:
		if isinstance(elt, (list, tuple)):
			flatten(elt, out)
		else:
			out.append(elt)
	return out


class Conversation(object):
	selfuser = '7202549'
	CHAD = '100000669061191'
	def __init__(self, data, nodes = []):
		self.data = data
		if self.data:
			self.thread = data.get('message_thread')
			self.message_count = self.thread.get('messages_count', 0)
			self.participants = set([u.get('messaging_actor').get('id') for u in self.thread.get('all_participants').get('nodes')])
			self.participants.remove(self.selfuser)
			self.thread_key = self.thread.get('thread_key')
			self.messages = self.thread.get('messages').get('nodes')
			self.node_length = len(self.messages)
			self.updated_time = self.thread.get('updated_time_precise')
			self.page_info = self.thread.get('messages').get('page_info')
		self.nodes = nodes
	
	def get_prior(self):
		pass
		
	@property
	def get_last_message(self):
		return self.thread.get('last_message').get('nodes')[0]
	
	@property
	def last_read_receipt(self):
		return to_datetime(self.thread.get('last_read_receipt').get('nodes')[0].get('timestamp_precise'))
	
	def convert(self, message):
		timestamp = message.get('timestamp_precise')
		text = message.get('snippet')
		author = message.get('message_sender').get('id')
		uid = message.get('message_id')
		if author is '7202549':
			name = 'Kristen'
		else:
			name = 'Michael'
		return Message(uid, author =author, timestamp =timestamp, text=text)
	
	def to_string(self):
		self.nodes = list(map(self.convert, self.messages))
		messages = list(map(str, self.nodes))
		from textwrap import wrap
		WRAPS = []
		for message in messages:
			wp = wrap(message, 100)
			WRAPS.extend(wp)
			#if len(wp) > 3:
			#	WRAPS.append('\n')
		return '\n'.join(WRAPS)
	
	
	
	
	#####
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

#fetchThreadMessages
#fetchThreadInfo

#fetchThreadList
#fetchUnread



def process_all_users(self):
	users = [(pythonize(user.name), user) for user in self.fetchAllUsers()]
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
	ext = message.get('extensible_attachment')
	if ext is not None:
		attachment = message.get('extensible_attachment').get('story_attachment')
		ex = attachment.get('url')
		durl = furl(ex).args
		url= durl.get('u', durl)
		if with_title:
			title = attachment.get('title_with_entities').get('text')
			return (url, title)
		else:
			return url
	

	

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
CHAD = '100000669061191'
TS_FACTOR = 1000

#GraphQL

	
	
	#


#['message_thread']['messages']['nodes']





#strftime('%s')


def get_messages(self, uid, limit=100, before=None):
	return self.fetchThreadMessages(uid, limit=limit, before=before)

	




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