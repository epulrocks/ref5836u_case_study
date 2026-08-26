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
import logging

logger = logging.getLogger(__name__)

def consolidate(config: Config):
	logger.info("Reading Reference DB...")
	db = ReferenceDB(config.input_path.reference_db)
	logger.info("Reading input files...")
	original_df = read_data_files(config.input_path.data)
	df = original_df.copy()
	logger.info("Normalizing data...")
	normalize(df)
	logger.info("Classifying categories...")
	classify(df, db)
	logger.info("Validating data...")
	validation(df, db, config.reference_date)
	accepted_df, original_rejected_df = split(df, original_df)
	logger.info("Deduplicating accepted data...")
	dedupe_accepted_df = deduplicate(accepted_df)
	logger.info("Outputting results...")
	output(dedupe_accepted_df, original_rejected_df, config.output_path)
	db.close()

if __name__ == "__main__":
	load_dotenv()
	try:
		# Setup (init.py)
		args = get_args()
		setup_logging(args.debug)
		config = load_config("config.yaml")
		logger.debug(f"config => {config}")

		# Main consolidate process
		consolidate(config)
	except Exception as e:
		logger.exception("Unexpected Error Occurred!")
		raise e