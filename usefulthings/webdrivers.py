#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = webdrivers
# author=SluttyScience
# date = 7/8/17
from startups import *
import sys, os

DRIVERS = ("""/Users/kristen/Downloads/geckodriver
/Users/kristen/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs
/Users/kristen/Downloads/selenium-server-standalone-3.1.0.jar""")

SELENIUM = '/Users/kristen/anaconda/selenium'
STANDALONE = '/Users/kristen/Downloads/selenium-server-standalone-3.1.0.jar'
GECKO = '/Users/kristen/Downloads/geckodriver'
JQUERY ='/Users/kristen/Downloads/jquery-3.1.1.js'
PHANTOMJS ='/Users/kristen/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
CHROME = '/Users/kristen/Downloads/chromedriver'
FIREFOX_PROFILE_DIR = '/Users/kristen/Library/Application Support/Firefox/Profiles'
profile = join(FIREFOX_PROFILE_DIR, 'lsvbvalb.dev-edition-default')
APP ='/Applications/FirefoxDeveloperEdition.app'
BINARY = '/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox-bin'
from selenium.webdriver import phantomjs, chrome, common, firefox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#chrome_options = webdriver.ChromeOptions()

Binary = firefox.firefox_binary.FirefoxBinary
Profile = firefox.firefox_profile.FirefoxProfile


def get_chrome():
	Chrome = webdriver.Chrome('/Users/kristen/Downloads/chromedriver')
	#Chrome.get('https://www.literotica.com/stories/')
	return Chrome

def get_phantomjs():
	JS = webdriver.PhantomJS('/Users/kristen/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
	return JS

def get_firefox():
	prof = firefox.firefox_profile.FirefoxProfile(profile)
	executable_path = '/Users/kristen/Downloads/geckodriver'
	binary = firefox.firefox_binary.FirefoxBinary('/Applications/FirefoxDeveloperEdition.app')
	Firefox = webdriver.Firefox(prof, binary, executable_path='/Users/kristen/Downloads/geckodriver')
	return Firefox
	
	
	if __name__ == '__main__': print(__file__)