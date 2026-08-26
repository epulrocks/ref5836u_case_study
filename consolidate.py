from dotenv import load_dotenv
from utils.init import get_args, setup_logging, load_config
from utils.model import Config
from utils.input import read_data_files
from utils.normalize import normalize
from utils.db import ReferenceDB
from utils.validation import validation
from utils.classify import classify
from utils.deduplicate import deduplicate
from utils.output import output
from utils.split import split

def consolidate(config: Config):
	db = ReferenceDB(config.input_path.reference_db)
	original_df = read_data_files(config.input_path.data)
	df = original_df.copy()
	normalize(df)
	classify(df, db)
	validation(df, db, config.reference_date)
	accepted_df, original_rejected_df = split(df, original_df)
	dedupe_accepted_df = deduplicate(accepted_df)
	output(dedupe_accepted_df, original_rejected_df, config.output_path)
	db.close()

if __name__ == "__main__":
	load_dotenv()
	logger = None
	try:
		# Setup (init.py)
		args = get_args()
		logger = setup_logging(args.debug)
		config = load_config("config.yaml")
		logger.debug(f"config => {config}")

		# Main consolidate process
		consolidate(config)
	except Exception as e:
		if logger:
			logger.exception("Unexpected Error Occurred!")
		raise e