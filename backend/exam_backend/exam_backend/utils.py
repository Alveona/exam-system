import requests
import json
import os
import uuid
from exam_backend.connection import FILES_PASSWORD, FILES_USERNAME, FILES_HOST
from exam_backend.settings import TEMP_DIR_PATH
from django.core.files.storage import default_storage

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def upload_media_file(file):
    create_new_folder(TEMP_DIR_PATH)
    unique_modifier = uuid.uuid4().hex
    saved_path = os.path.join(TEMP_DIR_PATH, unique_modifier + file.name)
    # file.save(saved_path)
    default_storage.save(saved_path, file)

    response = requests.post(FILES_HOST + '/upload', 
    files={'file': open(saved_path, 'rb')},
    auth=(FILES_USERNAME, FILES_PASSWORD))

    if response.status_code != 200:
        if response.status_code == 401:
            return {"message":"Basic Auth required"}, 401
        if response.status_code == 400:
            return {"message":"Bad request"}, 400

    response_dict = json.loads(response.text)
    return FILES_HOST + response_dict.get('path')