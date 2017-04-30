#!/usr/bin/env
# -*- coding: utf-8 -*-
# author=KGerring
# date = 3/4/17

import sys, os

import sys, os
import zlib, zipfile
from datetime import date
from send2trash import send2trash
from shutil import move



def backup_to_zip(folder, use_date=True, move_to=None):
	folder = os.path.abspath(folder)
	date_slot = (date.today().isoformat().replace('-', '_') if use_date else '')
	number = 1
	while True:
		if use_date:
			zip_filename = '{}_{}.zip'.format(os.path.basename(folder), date_slot)
			if os.path.exists(zip_filename):
				zip_filename = (((os.path.basename(folder) + '_') + str(number)) + '.zip')
		else:
			zip_filename = (((os.path.basename(folder) + '_') + str(number)) + '.zip')
			if (not os.path.exists(zip_filename)):
				break
			number = (number + 1)
	print(('Creating %s...' % zip_filename))
	backup_zip = zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED)
	for (foldername, subfolders, filenames) in os.walk(folder):
		print(('Adding files in %s...' % foldername))
		backup_zip.write(foldername)
		for filename in filenames:
			newBase = (os.path.basename(folder) + '_')
			if (filename.startswith(newBase) and filename.endswith('.zip')):
				continue
			backup_zip.write(os.path.join(foldername, filename))
	backup_zip.close()
	print('Done.')


def conditional_backup_to_zip(folder):
	folder = os.path.abspath(folder)
	number = 1
	while True:
		zip_filename = (((os.path.basename(folder) + '_') + str(number)) + '.zip')
		if (not os.path.exists(zip_filename)):
			break
		number = (number + 1)
	print(('Creating %s...' % zip_filename))
	backup_zip = zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED)
	for (foldername, subfolders, filenames) in os.walk(folder):
		print(('Adding files in %s...' % foldername))
		backup_zip.write(foldername)
		for filename in filenames:
			newBase = (os.path.basename(folder) + '_')
			if (filename.startswith(newBase) and filename.endswith('.zip')):
				continue
			backup_zip.write(os.path.join(foldername, filename))
	backup_zip.close()
	print('Done.')

