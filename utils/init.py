from datetime import datetime, timezone
from argparse import ArgumentParser
import logging
from pathlib import Path
import sys
import yaml
from .model import Config
from pydantic import ValidationError

def get_ts(ts_format: str = "%Y%m%d%H%M%S"):
	return datetime.now(timezone.utc).strftime(ts_format)

def get_args():
	parser = ArgumentParser(
		description="Data Processing Automation Pipeline"
	)
	parser.add_argument(
		'--debug', 
		action='store_true', 
		help="Enable detailed debug logging"
	)
	args = parser.parse_args()
	return args

def setup_logging(debug: bool = False, log_folder: str = "logs"):
	log_level = logging.DEBUG if debug else logging.INFO
	logger = logging.getLogger("main")
	logger.setLevel(log_level)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	Path(log_folder).mkdir(exist_ok=True)
	file_handler = logging.FileHandler(f"{log_folder}/{get_ts()}.log")
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(formatter)
	logger.addHandler(console_handler)
	logger.debug("Debug: On")
	return logger

def load_config(config_path: str):
	path = Path(config_path)
	if not path.exists():
		raise Exception(f"'{config_path}' missing")
	with path.open('r') as file:
		config_dict = yaml.safe_load(file) or {}
		try:
			config = Config(**config_dict)
		except ValidationError as e:
			exp_msg = f"Error while loading config file: '{config_path}'"
			for err in e.errors():
				exp_msg += f"\n\t{" -> ".join(err['loc'])}: \t{err['msg']}"
			logging.getLogger("main").error(exp_msg)
			sys.exit(1)
		Path(config.output_path).mkdir(exist_ok=True)
		config.reference_date = config.reference_date or datetime.now().date()
		return config