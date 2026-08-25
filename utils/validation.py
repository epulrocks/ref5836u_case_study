import pandas as pd
import re
from datetime import date

def validation(df, db, ref_date):
	validate_existing_merchant(df, db)
	validate_region(df, db)
	validate_phone_number(df)
	validate_email(df)
	validate_register_date(df, ref_date)
	validate_category(df)
	df["rejected"] = df["rejection_reasons"] != ""

def validate_existing_merchant(df, db):
	df['rejection_reasons'] = ""
	df['valid_name'] = True
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
		row["valid_name"] = False
	elif not isinstance(row["merchant_name"], str):
		row["rejection_reasons"] += "Invalid Merchant Name; "
		row["valid_name"] = False
	elif len(row["merchant_name"]) == 0:
		row["rejection_reasons"] += "Merchant Name Empty; "
		row["valid_name"] = False	
	return row

def validate_region(df, db):
	df["valid_region"] = True
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
	if isinstance(row["region"], str) and len(row["region"]) == 0:
		row["rejection_reasons"] += "Region Empty; "
		row["valid_region"] = False
	elif pd.isnull(row["pic_name"]) and pd.isnull(row["pic_email"]):
		row["rejection_reasons"] += "Invalid Region; "
		row["valid_region"] = False
	return row

def validate_phone_number(df):
	df["valid_number"] = True
	df[df.columns] = df[df.columns].apply(lambda x: write_phone_number(x), axis=1)

def write_phone_number(row):
	if len(row["contact_phone"]) < 9:
		row["rejection_reasons"] += "Contact Number contains less than 9 digits; "
		row["valid_number"] = False
	return row

def validate_email(df):
	df["valid_email"] = True
	df[df.columns] = df[df.columns].apply(lambda x: write_email(x), axis=1)

def write_email(row):
	email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	if not isinstance(row["contact_email"], str) or \
		not re.match(email_regex, row["contact_email"]):
		row["rejection_reasons"] += "Invalid Email; "
		row["valid_email"] = False
	return row

def validate_register_date(df, ref_date):
	df["valid_date"] = True
	df[df.columns] = df[df.columns].apply(lambda x: write_register_date(x, ref_date), axis=1)

def write_register_date(row, ref_date):
	if not isinstance(row["registration_date"], date) or row["registration_date"] > ref_date:
		row["rejection_reasons"] += "Invalid Registration Date; "
		row["valid_date"] = False
	return row

def validate_category(df):
	df["valid_category"] = True
	df[df.columns] = df[df.columns].apply(lambda x: write_category(x), axis=1)

def write_category(row):
	if pd.isnull(row["canonical_category"]):
		row["rejection_reasons"] += "Invalid Category; "
		row["valid_category"] = False
	return row