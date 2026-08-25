import pandas as pd

def validate_existing_merchant(df, db):
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