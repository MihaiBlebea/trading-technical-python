from dotenv import dotenv_values
import os
from pathlib import Path

dir = Path(__file__).parent.resolve()

"""
Docs gogo
"""
def get_key(key: str) -> str:
	"""
	Get the value of the key from the .env file or from the environment variables
	"""
	config = dotenv_values(f"{dir}/../.env")
	if key not in config:
		return os.getenv(key)

	return config[key]