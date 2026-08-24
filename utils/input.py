import pandas as pd
from pathlib import Path
import logging

def read_data_files(data_path: Path):
	logger = logging.getLogger("main")
	data_files_list = data_path.iterdir()
	df_list = []
	for data_file in data_files_list:
		try:
			df_list.append(pd.read_csv(data_file.absolute()))
		except UnicodeDecodeError as e:
			# A '.DS_Store' file in 'data' folder is causing read error
			# This error handling only shows read error in the log file/terminal
			# but CONTINUES THE PROCESS. We might need to handle error properly
			# if the file with error is important for the process
			logger.error(f"Error reading file: '{data_file.name}'")
	return pd.concat(df_list, ignore_index=True)