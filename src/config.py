from os import environ

from dotenv import load_dotenv

load_dotenv()

PATH_TO_DB = environ.get("PATH_TO_DB", "*")
DEFAULT_IMG = environ.get("DEFAULT_IMG", "*")
