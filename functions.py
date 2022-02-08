import random
import string

class Constants:
	CONSTANTS = {
		"DIR": "uploads/",
		"TOKENS": [],
		"ENABLE_CUSTOM_FILENAMES": False,
		"TOKEN_GENERATION_LENGTH": 6,
		"BASE_URL": "https://cdn.senarc.org/"
	}

	@staticmethod
	def get(constant):
		return Constants.CONSTANTS[constant]

class Generate:
	def file_token():
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))