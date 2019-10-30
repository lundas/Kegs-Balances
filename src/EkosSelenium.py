#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import ElementClickInterceptedException
from datetime import datetime
import time

class EkosSelenium:
	'''Class for accessing and downloading items from Ekos using 
	Selenium Webdriver'''
	# Firefox Settings. Need to import from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
	gPATH = '/home/lund/downloads/geckodriver'

	# FIREFOX PROFILE - PREVENTS DOWNLOAD DIALOGS
	profile = FirefoxProfile()
	profile.set_preference("browser.download.folderList", 2)  #set download location as custom dir
	profile.set_preference("browser.download.dir", '/home/lund/downloads/')  #sets custom dir - NEED PATH ON LOCAL MACHINE
	profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")

	# Firefox Options - Allows Firefox to run in headless mode
	options = Options()
	options.add_argument('-headless')
	options.set_headless(headless=True)

	browser = webdriver.Firefox(firefox_profile = profile, executable_path = gPATH, firefox_options = options)

	# chrome_options = Options()
	# chrome_options.add_argument('--headless')
	# chrome_options.add_argument('--window-size=1920x1080')

	# browser = webdriver.Chrome()

	def login(self, username, password):
		'''logs in to Ekos using credentials provided by user
			handle any alerts that may occur during log in'''
		#open webdriver, go to Ekos login page
		print("Logging in to Ekos")
		browser = EkosSelenium.browser
		browser.get('https://login.goekos.com/default.aspx')
		assert "Ekos" in browser.title

		#enter login credentials and log in
		elem = browser.find_element_by_id('txtUsername')
		elem.send_keys(username)
		elem = browser.find_element_by_id('txtPassword')
		elem.send_keys(password)
		elem.send_keys(Keys.RETURN)

		#handle alert that might occur upon login
		try:
			WebDriverWait(browser, 3).until(
				EC.alert_is_present()
				)
			alert = browser.switch_to.alert()
			alert.accept()
			print("Alert Accepted")
		except TimeoutException:
			print("No Alert")

		print("Login Successful")

		return

	def download_report(self, reportname):
		'''Clicks Report link and downloads report provided
		by user'''
		browser = EkosSelenium.browser
		try:
			WebDriverWait(browser, 3).until(
				EC.alert_is_present()
				)
			alert = browser.switch_to.alert()
			alert.accept()
			print("Alert Accepted")
		except TimeoutException:
			print("No Alert")
		#Get and click on Reports Tab
		elem = WebDriverWait(browser, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, 'Reports'))
			)
		elem.click()

		#Click reportname link
		while True:
			try:
				print("Downloading %s as csv" % str(reportname))
				elem = WebDriverWait(browser, 10).until(
					EC.element_to_be_clickable((By.LINK_TEXT, reportname))
					)
				elem.click()
				#download csv
				browser.implicitly_wait(10)
				# time.sleep(5)	# time.sleeps useful with Chrome
				browser.switch_to.frame('formFrame_0')
				# time.sleep(5)
				elem = WebDriverWait(browser, 10).until(
					EC.element_to_be_clickable((By.CLASS_NAME, 'buttonGroupInner'))
					)
				elem.click()
				dltime = datetime.today()		#capture time of download
				elem = WebDriverWait(browser, 10).until(
					EC.element_to_be_clickable((By.ID, 'csv_export'))
					)
				# time.sleep(5)
				elem.click()
				# time.sleep(5)
				#close iframe
				browser.switch_to.default_content()
				elem = browser.find_element_by_class_name('formClose')
				elem.click()
			except NoSuchFrameException:
				print('NoSuchFrameException: Restarting DL process')
			except ElementClickInterceptedException:
				print('ElementClickInterceptedException: Closing iframe')
				browser.switch_to.default_content()
				elem = browser.find_element_by_class_name('formClose')
				elem.click()
			else:
				break

		return dltime

	def quit(self):
		'''quits webdriver'''
		EkosSelenium.browser.quit()
		return


