from datetime import datetime, date
from pytz import timezone
import os
import re
import sys

class RenameFile:
	'''Class for renaming files downloaded from Ekos in preperation for
	reformatting data using pandas and then importing data into Google
	Sheets'''

	def dtround(self, datetime):
		'''Rounds seconds of datetime object up if microseconds > 500000
		else returns datetime object'''
		print("Rounding %s" % str(datetime))
		if datetime.microsecond > 500000 and datetime.second == 59:
			datetime = datetime.replace(minute = datetime.minute + 1, 
				second = 0)
		elif datetime.microsecond > 500000:
			datetime = datetime.replace(second = datetime.second + 1)
		return datetime

	def tzconv(self, datetime):
		'''Takes datetime object, sets timezone as Pacific Time
		and the convents timezone to Eastern Time. Necessary because
		Ekos export names incorporate time of download in Eastern Time.
		DST = Daylight Savings Time'''
		print("Adjusting Timezones")
		datetime = timezone('UTC').localize(datetime)
		datetime = datetime.astimezone(timezone('US/Eastern'))
		return datetime

	def rename_file(self, new_filename, PATH):
		'''Searches for the downloaded csv file based on a regular expression
		and replaces that filename with a filename provided '''
		filename_regex = re.compile('Export_\d\d\d\d\d\d\d\d\d\d\d\d\d\d_\.csv')
		for l in os.listdir(PATH):
			if filename_regex.match(l) != None:
				filename = filename_regex.match(l).string
				os.rename(PATH + filename, PATH + new_filename)
			else:
				logger.info('No file matching regular expression')
		return
	
