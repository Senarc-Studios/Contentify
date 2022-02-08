import os
import json
import uvicorn

from random import randint
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from functions import Constants, Generate

app = FastAPI()

def get_extension(path: str):
	if os.path.is_file(path) == False:
		return None
	file = path.split("/")[-1]
	extension = file.split(".")[-1]
	return extension

def get_clean_filename(path: str):
	if os.path.is_file(path) == False:
		return None
	file = path.split("/")[-1]
	filename = ""

	seperated_filename_list = file.split(".")
	for i in len(seperated_filename_list):
		filename = filename + seperated_filename_list[i]
		if i == (len(seperated_filename_list) - 1):
			break

	return filename

class UploadPayload(BaseModel):
	file: UploadFile = File(...)
	format: str
	name: Optional[str]

@app.post("/upload")
async def upload_file(payload: UploadPayload):
	if format.startswith("."):
		payload.format
	file = payload.file
	if Constants.get("ENABLE_CUSTOM_FILENAME") == False:
		file.filename = Generate.token()

	file.filename = f"{Generate.token()}.{format}"
	contents = await file.read()

	with open(Constants.get("DIR") + str(file.filename), "wb") as f:
		f.write(contents)

	payload = {
		"filename": file.filename,
		"url": f"{Constants.get('BASE_URL')}/{file.filename}"
	}

	return json.dumps(payload), 200, {'Content-Type': 'application/json'}

@app.get("/{filename}")
async def read_random_file(filename: str):
	files = os.listdir(Constants.get("DIR"))
	path = f"{Constants.get('DIR')}{files[filename]}"
	if os.path.is_file(path) == False:
		return json.dumps({ "404": "Not Found" }), 404, {'Content-Type': 'application/json'}

	return FileResponse(path), 200

if __name__ == '__main__':
	uvicorn.run("main:app", host='127.0.0.1', port=80, reload=True, debug=True, workers=2)