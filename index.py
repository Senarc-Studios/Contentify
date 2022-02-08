import os
import json

from random import randint
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from functions import Constants, Generate

app = FastAPI()

class UploadPayload(BaseModel):
	file: UploadFile = File(...)
	name: Optional[str]

@app.post("/upload")
async def upload_file(payload: UploadPayload):
	file = payload['file']
	if Constants.get("ENABLE_CUSTOM_FILENAME") == False:
		file.filename = Generate.token()

	file.filename = f"{Generate.token()}.jpg"
	contents = await file.read()

	with open(Constants.get("DIR") + str(file.filename), "wb") as f:
		f.write(contents)

	payload = {
		"filename": file.filename,
		"url": f"{Constants.get('BASE_URL')}/{file.filename}"
	}

	return {"filename": file.filename}

@app.get("/{filename}")
async def read_random_file(filename: str):
	files = os.listdir(Constants.get("DIR"))
	path = f"{Constants.get('DIR')}{files[filename]}"
	if os.path.is_file(path) == False and os.path.is_file(path[:-3]) == False:
		return json.dumps({ "404": "Not Found" }), 404

	elif os.path.is_file(path) == False:
		path = path[:-3]

	return FileResponse(path)