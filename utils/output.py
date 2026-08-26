def output(clean_df, errors_df, output_folder_path):
	output_clean(clean_df, output_folder_path)
	output_errors(errors_df, output_folder_path)

def output_clean(clean_df, output_folder_path):
	clean_col = [
		"merchant_name", "canonical_category", "region",
		"contact_phone", "contact_email", "registration_date",
		"region_pic_email", "source_submission_id", "duplicates_collapsed"
	]
	column_name_map = {
		'pic_email': 'region_pic_email',
		'submission_id': 'source_submission_id'
	}
	clean_df.rename(columns=column_name_map, inplace=True)
	clean_df[clean_col].to_csv(output_folder_path / "clean.csv", index=False)

def output_errors(errors_df, output_folder_path):
	errors_col = [
		"submission_id", "source_file", "merchant_name",
		"region", "region_pic_email", "rejection_reasons"
	]
	column_name_map = {
		'pic_email': 'region_pic_email'
	}
	errors_df.rename(columns=column_name_map, inplace=True)
	errors_df[errors_col].to_csv(output_folder_path / "errors.csv", index=False)