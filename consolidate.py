from utils.init import get_args, setup_logging, load_config
from utils.model import Config
from utils.input import read_data_files
from utils.normalize import normalize

def consolidate(config: Config):
	# Read, concat data files and create a copy for transformation
	original_df = read_data_files(config.input_path.data)
	df = original_df.copy()
	# Normalize
	df = normalize(df)

if __name__ == "__main__":
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