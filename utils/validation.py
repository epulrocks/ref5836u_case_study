import pandas as pd
import re
from datetime import date

def validate_existing_merchant(df, db):
	df['rejection_reasons'] = ""
	db_merchant_list = db.query("SELECT * FROM existing_merchants")
	existing_name = pd.merge(
		df,
		db_merchant_list,
		how='left',
		on='merchant_name',
		indicator='ind'
	).query("ind == 'both'").loc[:, 'merchant_id']
	existing_id = pd.merge(
		df,
		db_merchant_list,
		how='left',
		left_on='existing_merchant_id',
		right_on='merchant_id',
		indicator='ind'
	).query("ind == 'both'").loc[:, 'merchant_id']
	merged_id = pd.concat([existing_name, existing_id])
	unique_list = ~merged_id.index.duplicated(keep='first')
	df["found_id"] = merged_id.loc[unique_list]
	df[df.columns] = df[df.columns].apply(lambda x: write_existing_id(x), axis=1)
	df.drop("found_id", axis = 1, inplace=True)

def write_existing_id(row):
	if pd.notnull(row["found_id"]):
		row["rejection_reasons"] += f"Existing Merchant ID found: {row["found_id"]}; "
	return row

def validate_region(df, db):
	db_region_pic = db.query("SELECT * FROM region_pic")
	matched_region = pd.merge(
		df,
		db_region_pic,
		how='left',
		on='region',
		indicator='ind'
	).query("ind == 'both'").loc[:, ["pic_name", "pic_email"]]
	df[matched_region.columns] = matched_region
	df[df.columns] = df[df.columns].apply(lambda x: write_region(x), axis=1)

def write_region(row):
	if pd.isnull(row["pic_name"]) and pd.isnull(row["pic_email"]):
		row["rejection_reasons"] += "Outside Operating Region; "
	return row

def validate_phone_number(df):
	df[df.columns] = df[df.columns].apply(lambda x: write_phone_number(x), axis=1)

def write_phone_number(row):
	if len(row["contact_phone"]) < 9:
		row["rejection_reasons"] += "Contact Number contains less than 9 digits; "
	return row

def validate_email(df):
	df[df.columns] = df[df.columns].apply(lambda x: write_email(x), axis=1)

def write_email(row):
	email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	if not isinstance(row["contact_email"], str) or \
		not re.match(email_regex, row["contact_email"]):
		row["rejection_reasons"] += "Invalid Email; "
	return row

def validate_register_date(df, ref_date):
	df[df.columns] = df[df.columns].apply(lambda x: write_register_date(x, ref_date), axis=1)

def write_register_date(row, ref_date):
	if not isinstance(row["registration_date"], date) or row["registration_date"] > ref_date:
		row["rejection_reasons"] += "Invalid Registration Date; "
	return row
