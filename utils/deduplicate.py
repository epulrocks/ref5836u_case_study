def deduplicate(df):
	dedupe_df = df.copy()
	dedupe_df["sort_key"] = None
	dedupe_df = dedupe_df.apply(lambda x: set_sort_key(x), axis=1)
	dedupe_df.sort_values(["sort_key", "rejected", "registration_date"], ascending=[True, True, True], inplace=True)

	dupe_group = dedupe_df.loc[dedupe_df.duplicated(subset="sort_key", keep=False)]
	dupe_group_map = dupe_group.groupby('merchant_name')['file_submission'].agg(list).reset_index()
	dupe_group_dict = dupe_group_map.set_index("merchant_name")["file_submission"].to_dict()

	dedupe_df = dedupe_df[~dedupe_df.duplicated(subset="sort_key", keep="first")]
	dedupe_df.sort_index(inplace=True)

	dedupe_df["duplicate_collapsed"] = dedupe_df["merchant_name"].map(dupe_group_dict)
	dedupe_df = dedupe_df.apply(lambda x: format_dupe_list(x), axis=1)

	return dedupe_df

def set_sort_key(row):
	if not isinstance(row["merchant_name"], str):
		row["sort_key"] = row["submission_id"]
	elif row["merchant_name"].strip() == "":
		row["sort_key"] = row["submission_id"]
	else:
		row["sort_key"] = row["merchant_name"]
	return row

def format_dupe_list(row):
	if isinstance(row["duplicate_collapsed"], list):
		row["duplicate_collapsed"].remove(row["file_submission"])
		row["duplicate_collapsed"] = "\n".join(row["duplicate_collapsed"])
	return row