import pandas as pd
import re
from datetime import datetime

def normalize(df: pd.DataFrame):
	# Strip leading and trailing space all columns
	df[df.columns] = df[df.columns].apply(lambda x: x.str.strip())
	# Remove consecutive spaces
	df[df.columns] = df[df.columns].apply(
		lambda x: x.str.replace(r'\s+', ' ', regex=True)
	)

	# Set TitleCase on merchant_name and region
	title_column = ['merchant_name', 'region']
	df[title_column] = df[title_column].apply(lambda x: x.str.title())

	# Set Lowercase on contact_email
	lower_column = ['contact_email', 'business_category_freetext']
	df[lower_column] = df[lower_column].apply(lambda x: x.str.lower())

	# Only retain valid (+ and digits) characters from contact_phone
	phone_column = ['contact_phone']
	df[phone_column] = df[phone_column].apply(
		lambda x: x.str.replace(r'[^\+\d]+', '', regex=True)
	)
	# Convert +60 or 60 to 0
	df[phone_column] = df[phone_column].apply(
		lambda x: x.str.replace(r'^\+*60', '0', regex=True)
	)

	# Convert dates to YYYY-MM-DD
	date_columns = 'registration_date'
	df[date_columns] = df[date_columns].apply(lambda x: normalize_date(x))

	return df

def normalize_date(date_str):
	try:
		if re.match(r'\d{4}-\d{1,2}-\d{1,2}', date_str):
			return datetime.strptime(date_str, '%Y-%m-%d').date()
		if re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
			return datetime.strptime(date_str, '%d/%m/%Y').date()
	except:
		return None