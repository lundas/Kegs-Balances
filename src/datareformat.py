import csv
import numpy as np
import pandas as pd
import re
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create file handler
fh = logging.FileHandler('Kegs-Balances/kegsbalances.log') # PATH to file on local machine
fh.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to fh
fh.setFormatter(formatter)
# Add fh to logger
logger.addHandler(fh)

try:
	class DataReformat:
		# Class for reformatting Empty Keg and Outstanding Balance data from Ekos

		def data_reformat_empties(self, PATH, filename):
			# Reformats data from "Kegs At Customers - Pivoted by Keg 
			# Type/Quantity [Script Report]"" report from Ekos
			
			logger.info('Reformatting %s data' % filename)

			# Import and read csv file located in PATH
			logger.debug('Importing file %s' % filename)
			targetFile = PATH + filename
			df = pd.read_csv(targetFile)

			# Convert Most Recent Delivery to datetime objects
			# First drop NaNs in Most Recent Delivery column
			df = df[df['Most Recent Delivery'].isna() == False]
			# Convert Most Recent Delivery column to datetimes
			df['Most Recent Delivery'] = pd.to_datetime(df['Most Recent Delivery'])

			# Limit date range in data frame - 30 days ago to 6 months ago
			logger.debug('Limiting Delivery Date Range')
			# Ditch dates after 30 days before today
			last_month = pd.datetime.today() - pd.Timedelta(days=30)
			df = df[df['Most Recent Delivery'] <= last_month]
			# Ditch accounts that haven't ordered in the last 6 months
			six_months_ago = pd.datetime.today() - pd.Timedelta(days=180)
			df = df[df['Most Recent Delivery'] >= six_months_ago]

			# Fill NaNs
			logger.debug('Filling NaNs')
			# Quantity Columns with 0s
			df[['Keg Shell - 13.2 Gal', 'Keg Shell - Sixtel']] = df[['Keg Shell - 13.2 Gal', 'Keg Shell - Sixtel']].fillna(0)
			#df.info()
			# Salesperson Column with None
			df['Salesperson'] = df['Salesperson'].fillna('None')

			# Split data by Sales Rep and write to csvs
			logger.debug('Writing updated %s to Sales Rep csvs' % filename)
			sales_reps = df['Salesperson'].unique()
			for rep in sales_reps:
				df[df['Salesperson'] == rep].to_csv(path_or_buf=PATH+'%s_Empties.csv' % rep.replace(' ', '_'), 
			                                        columns=df.columns, 
			                                        index=False)
			return

		def data_reformat_overdue(self, PATH, filename):
			# Reformats data from "Invoice - Overdue Balances Summed by Company" report

			logger.info('Reformatting %s data' % filename)

			#Import and read csv file located in PATH
			logger.debug('Importing file %s' % filename)
			targetFile = PATH + filename
			df = pd.read_csv(targetFile)
			
			# Fill Salesperson NaNs with None
			logger.debug('Filling Salesperson NaNs')
			df['Salesperson'] = df['Salesperson'].fillna('None')

			# Convert Due Date Column to datetime objects
			logger.debug('Converting Due Date Column to datetime objects')
			df['Due Date'] = pd.to_datetime(df['Due Date'])

			# Add conditional Status column
			# "Credit Hold Next Week" for future due dates
			# "Balance Overdue" for past due dates
			logger.debug('Creating Status Column')
			df['Balance Status'] = ['Overdue Next Week' if x > pd.datetime.today() \
									else 'Balance Overdue' for x in df['Due Date']]

			# Split data by Sales Rep and write to csvs
			logger.debug('Writing updated %s to Sales Rep csvs' % filename)
			sales_reps = df['Salesperson'].unique()
			for rep in sales_reps:
				df[df['Salesperson'] == rep].to_csv(path_or_buf=PATH+'%s_Balances.csv' % rep.replace(' ', '_'), 
			                                        columns=df.columns, 
			                                        index=False)

			return


except Exception as e:
	logger.error(e, exc_info=True)


if __name__ == '__main__':
	reformat = DataReformat()

	PATH = '/PATH/TO/FILES/'
	filename = 'FILENAME'
	new_filename = 'NEW_FILENAME'

	errors = reformat.datareformat(PATH, filename, new_filename)
	print errors

