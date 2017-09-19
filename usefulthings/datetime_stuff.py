
import sys, os
from string import ascii_letters
import datetime
import isodate
import time
from functools import partial
dt = datetime.datetime
from datetime import date, timedelta
import re
from isodate.isotzinfo import tz_isoformat
from pytz import timezone, UTC
from isodate.duration import Duration
from isodate.isoduration import ISO8601_PERIOD_REGEX, parse_duration
from decimal import Decimal


import dateutil
import dateutil._common
import dateutil.easter
import dateutil.parser
from dateutil.parser import DEFAULTPARSER, DEFAULTTZPARSER
import dateutil.relativedelta
import dateutil.rrule
import dateutil.tz
import dateutil.tz._common
import dateutil.tz.tz
# import dateutil.tz.win
# import dateutil.tzwin
import dateutil.zoneinfo
import dateutil.zoneinfo.rebuild
from dateutil.zoneinfo import (get_data, getzoneinfofile_stream, get_zonefile_instance, gettz, gettz_db_metadata, ZONEFILENAME,
	tzfile, tar_open, TarFile, ZoneInfoFile)

def get_local_tzfile():
	tz = dateutil.tz.gettz()
	posix = tz._read_tzfile(open('/usr/share/zoneinfo/posixrules', 'rb'))
	return tz, posix




zoneinfo = dateutil.zoneinfo

from dateutil.rrule import rrule, FREQNAMES

FREQUENCIES = {k: getattr(dateutil.rrule, k) for k in FREQNAMES}

def get_rrule(start, count, cache=True):
	return rrule(dtstart=start, count=count, cache=True)

rule = dateutil.rrule

ZONEINFO = os.path.dirname(dateutil.zoneinfo.__file__)
ZONEFILE = os.path.join(ZONEINFO, dateutil.zoneinfo.ZONEFILENAME)

def copysign(x, y):
	return dateutil.relativedelta.copysign(x=x,y=y)

ISO8601 = isodate.isoduration.ISO8601_PERIOD_REGEX

ISO8601_RE = re.compile(
	r'^(?P<sign>[+-])?P'
	r'(?!\\b)'
	r'(?P<years>[0-9]+([,.][0-9]+)?Y)?'
	r'(?P<months>[0-9]+([,.][0-9]+)?M)?'
	r'(?P<weeks>[0-9]+([,.][0-9]+)?W)?'
	r'(?P<days>[0-9]+([,.][0-9]+)?D)?'
	r'('
	r'(?P<separator>T)'
	r'(?P<hours>[0-9]+([,.][0-9]+)?H)?'
	r'(?P<minutes>[0-9]+([,.][0-9]+)?M)?'
	r'(?P<seconds>[0-9]+([,.][0-9]+)?S)?'
		r')?$'
	, re.X)

def _parse_duration(datestring):
	"""
	Parses an ISO 8601 durations into datetime.timedelta or Duration objects.
	If the ISO date string does not contain years or months, a timedelta
	instance is returned, else a Duration instance is returned.
	The following duration formats are supported:
	  -PnnW                  duration in weeks
	  -PnnYnnMnnDTnnHnnMnnS  complete duration specification
	  -PYYYYMMDDThhmmss      basic alternative complete date format
	  -PYYYY-MM-DDThh:mm:ss  extended alternative complete date format
	  -PYYYYDDDThhmmss       basic alternative ordinal date format
	  -PYYYY-DDDThh:mm:ss    extended alternative ordinal date format
	The '-' is optional.
	Limitations:  ISO standard defines some restrictions about where to use
	  fractional numbers and which component and format combinations are
	  allowed. This _base implementation ignores all those restrictions and
	  returns something when it is able to find all necessary components.
	  In detail:
		it does not check, whether only the last component has fractions.
		it allows weeks specified with all other combinations
	  The alternative format does not support durations with years, months or
	  days set to 0.
	"""
	if not isinstance(datestring, str):
		raise TypeError("Expecting a string %r" % datestring)
	match = isodate.isoduration.ISO8601_PERIOD_REGEX.match(datestring)
	if not match:
		# try alternative format:
		if datestring.startswith("P"):
			durdt = isodate.isoduration.parse_datetime(datestring[1:])
			if durdt.year != 0 or durdt.month != 0:
				# create Duration
				ret = Duration(days=durdt.day, seconds=durdt.second,
				               microseconds=durdt.microsecond,
				               minutes=durdt.minute, hours=durdt.hour,
				               months=durdt.month, years=durdt.year)
			else:  # FIXME: currently not possible in alternative format
				# create timedelta
				ret = timedelta(days=durdt.day, seconds=durdt.second,
				                microseconds=durdt.microsecond,
				                minutes=durdt.minute, hours=durdt.hour)
			return ret
		raise ISO8601Error("Unable to parse duration string %r" % datestring)
	groups = match.groupdict()
	for key, val in list(groups.items()):
		if key not in ('separator', 'sign'):
			if val is None:
				groups[key] = "0n"
			# print groups[key]
			if key in ('years', 'months'):
				groups[key] = Decimal(groups[key][:-1].replace(',', '.'))
			else:
				# these values are passed into a timedelta object,
				# which works with floats.
				groups[key] = float(groups[key][:-1].replace(',', '.'))
	if groups["years"] == 0 and groups["months"] == 0:
		ret = timedelta(days=groups["days"], hours=groups["hours"],
		                minutes=groups["minutes"], seconds=groups["seconds"],
		                weeks=groups["weeks"])
		if groups["sign"] == '-':
			ret = timedelta(0) - ret
	else:
		ret = Duration(years=groups["years"], months=groups["months"],
		               days=groups["days"], hours=groups["hours"],
		               minutes=groups["minutes"], seconds=groups["seconds"],
		               weeks=groups["weeks"])
		if groups["sign"] == '-':
			ret = Duration(0) - ret
	return ret



def from_duration(years=0, months=0, weeks=0, days=0, hours=0, minutes=0,
             seconds=0, microseconds=0, milliseconds=0):
	return Duration(years=years, months=months, weeks=weeks, days=days, hours=hours, minutes=minutes,
	                seconds=seconds, milliseconds=milliseconds, microseconds=microseconds)


def _get_now(**kwargs):
	"""Flexible, locale-specific way to return the correct `now` time.
	Possible parameters and examples:
	:param fallback: a specific timezone to fall-back on. Default is UTC.
	:param name: A typical timezone in pytz name, like `US/Eastern`, UTC,
	or an instance of ``<DstTzInfo 'US/Eastern' LMT-1 day, 19:04:00 STD>``
	"""
	from pytz import timezone, UTC
	from pytz.exceptions import UnknownTimeZoneError
	from datetime import datetime as dt
	if not kwargs:
		return dt.utcnow()
	fallback = kwargs.get('fallback') if 'fallback' in kwargs else UTC
	tz = kwargs.get('tz') if 'tz' in kwargs else UTC
	name = kwargs.get('name', 'US/Eastern')
	if name:
		try:
			zone = timezone(name)
		except UnknownTimeZoneError:
			zone = fallback
	else:
		zone = UTC
	return dt.now(zone)

	

get_now = partial(_get_now, name ='America/New_York')
from operator import methodcaller

def get_timetz():
	timetz = methodcaller('timetz')
	return timetz(get_now())

def get_date():
	date = methodcaller('date')
	return date(get_now())


get_utcnow = partial(_get_now, name='UTC')


from datetime import timedelta

DELTADICT = {'days':         0,
             'hours':        0,
             'microseconds': 0,
             'milliseconds': 0,
             'minutes':      0,
             'seconds':      0,
             'weeks':        0}


class TimeUnit(object):
	__slots__ = ('single', 'plural')

	def __init__(self, single, plural):
		self.single = single
		self.plural = plural
		
	
		
		
	
		
	
days,hours = 1,1

def datedict(): return dict(
years = 365 * days,
weeks =     7 * days,
days =      24 * hours,
hours =     60 * minutes,
minutes =   60 * seconds,
seconds = 1000 * milliseconds,
milliseconds = 1000 * microseconds,
)

TIMEDELTA_UNITS = (('year', 31536000), ('month', 2592000), ('week', 604800), ('day', 86400), ('hour', 3600), ('minute', 60), ('second', 1))

def _strips(direction, text, remove):
	if (direction == 'l'):
		if text.startswith(remove):
			return text[len(remove):]
	elif (direction == 'r'):
		if text.endswith(remove):
			return text[:(- len(remove))]
	else:
		raise ValueError('Direction needs to be r or l.')
	return text

def rstrips(text, remove):
	return _strips('r', text, remove)

def lstripts(text, remove):
	return _strips('l', text, remove)

def timeinterval_fromstr(interval):
	parts = interval.strip().split(' ')
	if (len(parts) == 1):
		num = 1
		period = parts[0]
	elif (len(parts) == 2):
		(num, period) = parts
		num = int(num)
	else:
		raise ValueError('format should be ([num] second|minute|etc)')
	period = rstrips(period, 's')
	d = timeinterval.get(period, 0)
	delta = (num * d)
	return timedelta(0, delta)

def timedelta_by_name(interval='day'):
	return timeinterval_fromstr(('1 ' + interval))

timeinterval = dict(second=1, minute=60, hour=(60 * 60), day=((60 * 60) * 24), week=(((60 * 60) * 24) * 7), month=(((60 * 60) * 24) * 30), year=(((60 * 60) * 24) * 365))


class TimeText(object):
	__slots__ = ('single', 'plural')

	def __init__(self, single, plural):
		self.single = single
		self.plural = plural
		

timechunks = (((((60 * 60) * 24) * 365), TimeText('year', 'years')),
			  ((((60 * 60) * 24) * 30), TimeText('month', 'months')),
			  (((60 * 60) * 24), TimeText('day', 'days')),
			  ((60 * 60), TimeText('hour', 'hours')),
			  (60, TimeText('minute', 'minutes')),
			  (1, TimeText('second', 'seconds')))

def timetext(delta, precision=None, bare=True):
	delta = max(delta, timedelta(0))
	since = ((((delta.days * 24) * 60) * 60) + delta.seconds)
	for (i, (seconds, name)) in enumerate(timechunks):
		count = (since // seconds)
		if (count != 0):
			break
		if ((count == 0) and (delta.seconds == 0) and (delta != timedelta(0))):
			n = (delta.microseconds // 1000)
			time_label = '%(num)d %(time)s'
			s = (time_label % dict(num=n, time='milliseconds'))
		else:
			time_label = '%(num)d %(time)s'
			s = (time_label % dict(num=count, time=str(int(count))))
			if precision:
				j = 0
				while True:
					j += 1
					since -= (seconds * count)
					if ((i + j) >= len(timechunks)):
						break
					if (timechunks[(i + j)][0] < precision):
						break
					(seconds, name) = timechunks[(i + j)]
					count = (since // seconds)
					if (count != 0):
						s += (', %d %s' % (count, str(count)))
		if (not bare):
			s += (' ' + 'ago')
	return s

def timesince(d, precision=None):
	from datetime import datetime as dt
	return timetext((dt.now() - d), precision)

def timeuntil(d, precision=None):
	from datetime import datetime as dt
	return timetext((d - dt.now()), precision)

def timefromnow(interval):
	'The opposite of timeago'
	from datetime import datetime as dt
	return (dt.now() + timeinterval_fromstr(interval))

def timeago(interval):
	from datetime import datetime as dt
	return (dt.now() - timeinterval_fromstr(interval))
from datetime import datetime as dt
import time

def _process_carryover(deltas, carry_over):
	'A helper function to process negative deltas based on the deltas\n\tand the list of tuples that contain the carry over values'
	for (smaller, larger, amount) in carry_over:
		if (deltas[smaller] < 0):
			deltas[larger] -= 1
			deltas[smaller] += amount

def _pluralize_granularity(granularity):
	'Pluralize the given granularity'
	if ('century' == granularity):
		return 'centuries'
	return (granularity + 's')

def _delta_string(delta, granularity):
	'Return the string to use for the given delta and ordinality'
	if (1 == delta):
		return ('1 ' + granularity)
	elif (delta > 1):
		return ((str(delta) + ' ') + _pluralize_granularity(granularity))

def _is_leap_year(year):
	if (((year % 4) == 0) and ((year % 400) != 0)):
		return True
	return False

def distance_of_time_in_words(from_time, to_time=0, granularity='second', round=False):
	"\n\tReturn the absolute time-distance string for two datetime objects,\n\tints or any combination you can dream of.\n\n\tIf times are integers, they are interpreted as seconds from now.\n\n\t``granularity`` dictates where the string calculation is stopped.\n\tIf set to seconds (default) you will receive the full string. If\n\tanother accuracy is supplied you will receive an approximation.\n\tAvailable granularities are:\n\t'century', 'decade', 'year', 'month', 'day', 'hour', 'minute',\n\t'second'\n\n\tSetting ``round`` to true will increase the result by 1 if the fractional\n\tvalue is greater than 50% of the granularity unit.\n\n\tExamples:\n\n\t>>> distance_of_time_in_words(86399, round=True, granularity='day')\n\t'1 day'\n\t>>> distance_of_time_in_words(86399, granularity='day')\n\t'less than 1 day'\n\t>>> distance_of_time_in_words(86399)\n\t'23 hours, 59 minutes and 59 seconds'\n\t>>> distance_of_time_in_words(datetime(2008,3,21, 16,34),\n\t... datetime(2008,2,6,9,45))\n\t'1 month, 15 days, 6 hours and 49 minutes'\n\t>>> distance_of_time_in_words(datetime(2008,3,21, 16,34),\n\t... datetime(2008,2,6,9,45), granularity='decade')\n\t'less than 1 decade'\n\t>>> distance_of_time_in_words(datetime(2008,3,21, 16,34),\n\t... datetime(2008,2,6,9,45), granularity='second')\n\t'1 month, 15 days, 6 hours and 49 minutes'\n\t"
	granularities = ['century', 'decade', 'year', 'month', 'day', 'hour', 'minute', 'second']
	granularity_size = {'century': 10, 'decade': 10, 'year': 10, 'month': 12, 'day': 15, 'hour': 24, 'minute': 60, 'second': 60}
	if (granularity not in granularities):
		raise ValueError(('Please provide a valid granularity: %s' % granularities))
	if isinstance(from_time, int):
		from_time = dt.fromtimestamp((time.time() + from_time))
	if isinstance(to_time, int):
		to_time = dt.fromtimestamp((time.time() + to_time))
	if (from_time > to_time):
		s = from_time
		from_time = to_time
		to_time = s
	elif (from_time == to_time):
		return ('0 ' + _pluralize_granularity(granularity))
	deltas = {'century': 0, 'decade': 0, 'year': 0, 'month': 0, 'day': 0, 'hour': 0, 'minute': 0, 'second': 0}
	for field in ['month', 'hour', 'day', 'minute', 'second']:
		deltas[field] = (getattr(to_time, field) - getattr(from_time, field))
	delta_year = (to_time.year - from_time.year)
	if (delta_year >= 100):
		deltas['century'] = (delta_year // 100)
	if ((delta_year % 100) >= 10):
		deltas['decade'] = ((delta_year // 10) - (deltas['century'] * 10))
	if (delta_year % 10):
		deltas['year'] = (delta_year % 10)
	carry_over = [('second', 'minute', granularity_size['second']), ('minute', 'hour', granularity_size['minute']), ('hour', 'day', granularity_size['hour'])]
	_process_carryover(deltas, carry_over)
	month_carry = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if (deltas['day'] < 0):
		deltas['month'] -= 1
		if ((from_time.month == 2) and _is_leap_year(from_time.year)):
			deltas['day'] += 29
		else:
			deltas['day'] += month_carry[from_time.month]
	carry_over = [('month', 'year', granularity_size['month']), ('year', 'decade', granularity_size['year']), ('decade', 'century', granularity_size['decade'])]
	_process_carryover(deltas, carry_over)
	print(deltas)
	return_strings = []
	for g in granularities:
		delta = deltas[g]
		if (g == granularity):
			if (round and (g != 'second')):
				i = granularities.index(g)
				g_p = granularities[(i + 1)]
				delta_p = deltas[g_p]
				if (delta_p > (granularity_size[g_p] / 2)):
					delta += 1
				if (delta != 0):
					return_strings.append(_delta_string(delta, g))
				if (not return_strings):
					return ('less than 1 ' + granularity)
				break
			else:
				if (delta != 0):
					return_strings.append(_delta_string(delta, g))
				if (not return_strings):
					return ('less than 1 ' + granularity)
				break
		elif (delta != 0):
			return_strings.append(_delta_string(delta, g))
	if (len(return_strings) == 1):
		return return_strings[0]
	print(return_strings)
	return ((', '.join(return_strings[:(- 1)]) + ' and ') + return_strings[(- 1)])

def time_ago_in_words(from_time, granularity='second', round=False):
	'\n\tReturn approximate-time-distance string for ``from_time`` till now.\n\n\tSame as ``distance_of_time_in_words`` but the endpoint is now.\n\t'
	return distance_of_time_in_words(from_time, dt.now(), granularity, round)
DATE_BAS_COMPLETE = '%Y%m%d'
DATE_EXT_COMPLETE = '%Y-%m-%d'
DATE_BAS_WEEK_COMPLETE = '%YW%W%w'
DATE_EXT_WEEK_COMPLETE = '%Y-W%W-%w'
DATE_BAS_ORD_COMPLETE = '%Y%j'
DATE_EXT_ORD_COMPLETE = '%Y-%j'
DATE_BAS_WEEK = '%YW%W'
DATE_EXT_WEEK = '%Y-W%W'
DATE_MONTH = '%Y-%m'
DATE_YEAR = '%Y'
DATE_CENTURY = '%C'
TIME_BAS_COMPLETE = '%H%M%S'
TIME_EXT_COMPLETE = '%H:%M:%S'
TIME_BAS_MINUTE = '%H%M'
TIME_EXT_MINUTE = '%H:%M'
TIME_HOUR = '%H'
TIME_AMPM = '%I %p'
TZ_BAS = '%z'
TZ_EXT = '%Z'
TZ_HOUR = '%h'
DT_EXT_COMPLETE = (((DATE_EXT_COMPLETE + 'T') + TIME_EXT_COMPLETE) + TZ_EXT)
DT_BAS_COMPLETE = (((DATE_BAS_COMPLETE + 'T') + TIME_BAS_COMPLETE) + TZ_BAS)
DT_EXT_ORD_COMPLETE = (((DATE_EXT_ORD_COMPLETE + 'T') + TIME_EXT_COMPLETE) + TZ_EXT)
DT_BAS_ORD_COMPLETE = (((DATE_BAS_ORD_COMPLETE + 'T') + TIME_BAS_COMPLETE) + TZ_BAS)
DT_EXT_WEEK_COMPLETE = (((DATE_EXT_WEEK_COMPLETE + 'T') + TIME_EXT_COMPLETE) + TZ_EXT)
DT_BAS_WEEK_COMPLETE = (((DATE_BAS_WEEK_COMPLETE + 'T') + TIME_BAS_COMPLETE) + TZ_BAS)
D_DEFAULT = 'P%P'
D_WEEK = 'P%p'
D_ALT_EXT = ((('P' + DATE_EXT_COMPLETE) + 'T') + TIME_EXT_COMPLETE)
D_ALT_BAS = ((('P' + DATE_BAS_COMPLETE) + 'T') + TIME_BAS_COMPLETE)
D_ALT_EXT_ORD = ((('P' + DATE_EXT_ORD_COMPLETE) + 'T') + TIME_EXT_COMPLETE)
D_ALT_BAS_ORD = ((('P' + DATE_BAS_ORD_COMPLETE) + 'T') + TIME_BAS_COMPLETE)
days = (lambda d: ('%02d' % d.day))
DAYS = '{:2d}'
FULL_DAYS = '{:02d}'
MICROSECOND = '{:06d}'
STRF_DT_MAP = {'%d': (lambda tdt, yds: ('%02d' % tdt.day)), '%f': (lambda tdt, yds: ('%06d' % tdt.microsecond)), '%H': (lambda tdt, yds: ('%02d' % tdt.hour)), '%j': (lambda tdt, yds: ('%03d' % ((tdt.toordinal() - date(tdt.year, 1, 1).toordinal()) + 1))), '%m': (lambda tdt, yds: ('%02d' % tdt.month)), '%M': (lambda tdt, yds: ('%02d' % tdt.minute)), '%S': (lambda tdt, yds: ('%02d' % tdt.second)), '%w': (lambda tdt, yds: ('%1d' % tdt.isoweekday())), '%W': (lambda tdt, yds: ('%02d' % tdt.isocalendar()[1])), '%Y': (lambda tdt, yds: ((((yds != 4) and '+') or '') + (('%%0%dd' % yds) % tdt.year))), '%C': (lambda tdt, yds: ((((yds != 4) and '+') or '') + (('%%0%dd' % (yds - 2)) % (tdt.year / 100)))), '%h': (lambda tdt, yds: tz_isoformat(tdt, '%h')), '%Z': (lambda tdt, yds: tz_isoformat(tdt, '%Z')), '%z': (lambda tdt, yds: tz_isoformat(tdt, '%z')), '%%': (lambda tdt, yds: '%')}
strings = [('DATE_BAS_COMPLETE', '%Y%m%d'),
           ('DATE_BAS_ORD_COMPLETE', '%Y%j'),
           ('DATE_BAS_WEEK', '%YW%W'),
           ('DATE_BAS_WEEK_COMPLETE', '%YW%W%w'),
           ('DATE_CENTURY', '%C'), ('DATE_EXT_COMPLETE', '%Y-%m-%d'),
           ('DATE_EXT_ORD_COMPLETE', '%Y-%j'), ('DATE_EXT_WEEK', '%Y-W%W'),
           ('DATE_EXT_WEEK_COMPLETE', '%Y-W%W-%w'), ('DATE_MONTH', '%Y-%m'),
           ('DATE_YEAR', '%Y'), ('DT_BAS_COMPLETE', '%Y%m%dT%H%M%S%z'),
           ('DT_BAS_ORD_COMPLETE', '%Y%jT%H%M%S%z'), ('DT_BAS_WEEK_COMPLETE', '%YW%W%wT%H%M%S%z'),
           ('DT_EXT_COMPLETE', '%Y-%m-%dT%H:%M:%S%Z'), ('DT_EXT_ORD_COMPLETE', '%Y-%jT%H:%M:%S%Z'),
           ('DT_EXT_WEEK_COMPLETE', '%Y-W%W-%wT%H:%M:%S%Z'), ('D_ALT_BAS', 'P%Y%m%dT%H%M%S'),
           ('D_ALT_BAS_ORD', 'P%Y%jT%H%M%S'), ('D_ALT_EXT', 'P%Y-%m-%dT%H:%M:%S'),
           ('D_ALT_EXT_ORD', 'P%Y-%jT%H:%M:%S'), ('D_DEFAULT', 'P%P'), ('D_WEEK', 'P%p'), ('TIME_BAS_COMPLETE', '%H%M%S'),
           ('TIME_BAS_MINUTE', '%H%M'), ('TIME_EXT_COMPLETE', '%H:%M:%S'), ('TIME_EXT_MINUTE', '%H:%M'),
           ('TIME_HOUR', '%H'), ('TZ_BAS', '%z'), ('TZ_EXT', '%Z'), ('TZ_HOUR', '%h')]
DATES = [re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})-W(?P<week>[0-9]{2})-(?P<day>[0-9]{1})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})W(?P<week>[0-9]{2})(?P<day>[0-9]{1})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})-(?P<day>[0-9]{3})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})(?P<day>[0-9]{3})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})-W(?P<week>[0-9]{2})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})W(?P<week>[0-9]{2})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})-(?P<month>[0-9]{2})'), re.compile('(?P<sign>[+-]){0}(?P<year>[0-9]{4})'), re.compile('(?P<sign>[+-]){0}(?P<century>[0-9]{2})')]
TIMES = [re.compile('T?(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2}([,.][0-9]+)?)(?P<tzname>(Z|(?P<tzsign>[+-])(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)'), re.compile('T?(?P<hour>[0-9]{2})(?P<minute>[0-9]{2})(?P<second>[0-9]{2}([,.][0-9]+)?)(?P<tzname>(Z|(?P<tzsign>[+-])(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)'), re.compile('T?(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}([,.][0-9]+)?)(?P<tzname>(Z|(?P<tzsign>[+-])(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)'), re.compile('T?(?P<hour>[0-9]{2})(?P<minute>[0-9]{2}([,.][0-9]+)?)(?P<tzname>(Z|(?P<tzsign>[+-])(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)'), re.compile('T?(?P<hour>[0-9]{2}([,.][0-9]+)?)(?P<tzname>(Z|(?P<tzsign>[+-])(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)')]

def fmt(s, pattern='%{0}', date_time=None):
	if (date_time is None):
		formatted = dt.now().strftime(pattern.format(s))
	else:
		try:
			formatted = dt(date_time).strftime(pattern.format(s))
		except TypeError:
			formatted = None
	return formatted
lookup_fmt = partial(fmt, pattern='{0}    %{0}')

def fmt_timestamp(s):
	try:
		return datetime.datetime.fromtimestamp(int(float(s)))
	except (AttributeError, ValueError):
		return datetime.fromtimestamp(int(float(s)))
	except (AttributeError, ValueError):
		return None

def get_datetime(s):
	try:
		return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
	except AttributeError:
		return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def simple_fmt(obj):
	return obj.strftime('%x %l:%M %p')
