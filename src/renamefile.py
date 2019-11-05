from datetime import datetime, date
from pytz import timezone
import os
import re
import sys
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create file handler
fh = logging.FileHandler('Kegs-Balances/kegsbalances.log') # PATH to file on local machine
fh.setLevel(logging.INFO)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to fh
fh.setFormatter(formatter)
# Add fh to logger
logger.addHandler(fh)

class RenameFile:
	'''Class for renaming files downloaded from Ekos in preperation for
	reformatting data using pandas and then importing data into Google
	Sheets'''

	def dtround(self, datetime):
		'''Rounds seconds of datetime object up if microseconds > 500000
		else returns datetime object'''
		logger.info("Rounding %s" % str(datetime))
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
		logger.info("Adjusting Timezones")
		datetime = timezone('UTC').localize(datetime)
		datetime = datetime.astimezone(timezone('US/Eastern'))
		logger.debug('Adjusted Timezone is %s' % str(datetime))
		return datetime

	def rename_file(self, new_filename, PATH):
		'''Searches for the downloaded csv file based on a regular expression
		and replaces that filename with a filename provided '''
		filename_regex = re.compile('Export_\d{14}_\.csv')
		for l in os.listdir(PATH):
			if filename_regex.match(l) != None:
				logger.info('File found!')
				filename = filename_regex.match(l).string
				os.rename(PATH + filename, PATH + new_filename)
				break
			else:
				logger.info('File does not match regex. Checking next file')
		return
