from pydantic import BaseModel, field_validator
from pathlib import Path
from datetime import date

class InputPath(BaseModel):
	data: Path
	reference_db: Path
	@field_validator('data', 'reference_db')
	@classmethod
	def check_path_exists(cls, v: Path) -> Path:
		if not v.exists():
			raise ValueError(f"Path does not exist: '{v}'")
		return v

class Config(BaseModel):
	input_path: InputPath
	output_path: Path
	reference_date: date | None = None


