#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = webdrivers
# author=SluttyScience
# date = 7/8/17
from startups import *
import sys, os
join = os.path.join
WEBDRIVERS = os.path.expanduser('~/webdrivers')

SELENIUM = '/Users/kristen/anaconda/selenium'
STANDALONE = join(WEBDRIVERS, 'selenium-server-standalone-3.1.0.jar')
GECKO = join(WEBDRIVERS,'geckodriver')
JQUERY = join(WEBDRIVERS,'jquery-3.1.1.js')
PHANTOMJS = join(WEBDRIVERS,'phantomjs')
CHROME = join(WEBDRIVERS,'chromedriver')
FIREFOX_PROFILE_DIR = '/Users/kristen/Library/Application Support/Firefox/Profiles'
FIREFOX_PROFILE = join(FIREFOX_PROFILE_DIR, 'lsvbvalb.dev-edition-default')
#APP ='/Applications/FirefoxDeveloperEdition.app'
BINARY = '/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox-bin'
from selenium.webdriver import phantomjs, chrome, common, firefox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#chrome_options = webdriver.ChromeOptions()

Binary = firefox.firefox_binary.FirefoxBinary
Profile = firefox.firefox_profile.FirefoxProfile


def get_chrome():
	Chrome = webdriver.Chrome(CHROME)
	#Chrome.get('chrome://bookmarks/')
	return Chrome

def get_phantomjs():
	from selenium import webdriver
	from selenium.webdriver import phantomjs
	service = phantomjs.webdriver.Service(PHANTOMJS)
	JS = webdriver.PhantomJS(PHANTOMJS)
	return JS

def get_firefox():
	prof = firefox.firefox_profile.FirefoxProfile(FIREFOX_PROFILE)
	executable_path = GECKO
	binary = firefox.firefox_binary.FirefoxBinary('/Applications/FirefoxDeveloperEdition.app')
	Firefox = webdriver.Firefox(prof, binary, executable_path=GECKO)
	return Firefox

bookmarks = dict(
BK_C = '/Users/kristen/Library/Mobile Documents/com~apple~CloudDocs/bookmarks_3_16_17.html',
DOCUMENTS ='/Users/kristen/Documents',
BK = join(DOCUMENTS, 'bookmarks_3_22_17.html'),
BK4 = join(DOCUMENTS, 'bookmarks_3_22_174.html'),
SAFARI ='/Users/kristen/Library/Caches/Metadata/Safari/Bookmarks',
CB = '/Users/kristen/Downloads/Takeout/Chrome/Bookmarks.html')

def log_in(uname, password):
	c = get_chrome()
	i= '//*[@id="gb_70"]'
	c.get('https://www.google.com')
	ii = c.find_element_by_xpath(i)
	ii.click()
	ID = c.find_element_by_id('identifierId')
	ID.send_keys(uname)
	button = c.find_element_by_id("identifierNext")
	button.click()
	
	pass_inp = '//*[@id="password"]/div[1]/div/div[1]/input'
	passwd = c.find_element_by_xpath(pass_inp)
	passwd.send_keys(password)
	pass_next = '//*[@id="passwordNext"]/content/span'
	
	pin = c.find_element_by_id("idvPin")
	pin.send_keys('')
	pin_next = '//*[@id="idvPreregisteredPhoneNext"]/content/span'
	button_next = c.find_element_by_xpath(pin_next)
	button_next.click()


if __name__ == '__main__': print(__file__)