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
		# Class for reformatting Delivery Hour Report data from Ekos

		def data_reformat(self, PATH, filename):
			# Reformats data from Delivery Hour reports from Ekos
			
			logger.info('Reformatting %s data' % filename)

			# Import and read csv file located in PATH
			logger.debug('Importing file %s' % filename)
			targetFile = PATH + filename
			df = pd.read_csv(targetFile)

			# Rename Columns
			logger.debug('Renaming columns')
			df = df.rename(columns={element: re.sub(r'.* Delivery Start', 'Delivery Start', element, flags=re.MULTILINE)
			           for element in df.columns.tolist()})
			df = df.rename(columns={element: re.sub(r'.* Delivery End', 'Delivery End', element, flags=re.MULTILINE)
			           for element in df.columns.tolist()})
			df = df.rename(columns={'Delivery Company': 'Required Vehicle'})

			# Add Service Time Column
			logger.debug('Adding Service Time column')
			df['Service Time'] = 10

			# Convert Start Time and End Time to datetimes
			logger.debug('Converting start and end times to datetimes')
			df['Delivery Start'] = pd.to_datetime(df['Delivery Start'])
			df['Delivery End'] = pd.to_datetime(df['Delivery End'])
			# Convert datetimes to times
			df['Delivery Start'] = df['Delivery Start'].dt.time
			df['Delivery End'] = df['Delivery End'].dt.time

			# Collect Errors
			logger.debug('Collecing errors')
			errors = []
			for index, row in df.iterrows():
			    if pd.isna(row['Delivery Start']) == True or pd.isna(row['Delivery End']) == True:
			        errors.append('%s is missing a delivery time'%row['Name'])
			    elif row['Delivery Start'] >= row['Delivery End']:
			        errors.append('%s\'s delivery window is entered incorrectly'%row['Name'])
			    elif pd.isna(row['Address']) == True or pd.isna(row['City']) == True or \
			        pd.isna(row['State']) == True or pd.isna(row['Zip Code']) == True:
			        errors.append('%s is missing a valid address'%row['Name'])

			# Deal with NaNs
			logger.debug('dealing with NaNs')
			df['Delivery Start'] = df['Delivery Start'].fillna(value=pd.datetime(2019,1,1,9,0).time())
			df['Delivery End'] = df['Delivery End'].fillna(value=pd.datetime(2019,1,1,17,0).time())
			df[['Keg &#8209; 13.2 gal', 'Keg &#8209; Sixtel']] = df[['Keg &#8209; 13.2 gal', 'Keg &#8209; Sixtel']].fillna(value=0)
			df['Note'] = df['Note'].fillna(value='')


			#write info to csv file
			logger.debug('Writing updated %s to csv' % filename)
			df.to_csv(path_or_buf=targetFile, columns=df.columns, index=False)

			return errors
except Exception as e:
	logger.error(e, exc_info=True)

if __name__ == '__main__':
	reformat = DataReformat()

	PATH = '/PATH/TO/FILES/'
	filename = 'FILENAME'
	new_filename = 'NEW_FILENAME'

	errors = reformat.datareformat(PATH, filename, new_filename)
	print errors

