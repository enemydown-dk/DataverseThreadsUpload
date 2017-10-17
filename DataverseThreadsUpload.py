#!/usr/bin/env python3
# coding=utf8

"""
Python script uploads a number of files to an API
"""

from threading import Thread
from time import sleep
import json
import uuid
import os
import requests

# --------------------------------------------------
# Update params below to run code
# --------------------------------------------------
DATAVERSE_SERVER = '' #no trailing slash
API_KEY = '' #apikey from userprofile
PERSISTENT_ID = "" #DOI or HDL of the dataset
TIMEOUT = 0.1 #timeout between postattempts, use this to awoid blacklist
PATH = "files/" #path of auto-generated files
RANGE = 100 #number of files to generate

def create_file():
    """function that creates files of random size and name"""
    unique_name = str(uuid.uuid4())
    file = open(PATH + unique_name + ".txt", 'w')
    file.write(unique_name)
    file.close()

def upload_file():
    """Function that uploads a file to a URL"""
    url = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % \
    (DATAVERSE_SERVER, PERSISTENT_ID, API_KEY)

    for file in os.listdir(PATH):
        print(file)
        fpath = os.path.join(PATH, file)
        file_temp = open(fpath)
        file_content = file_temp.read()
        files = {'file': (file, file_content)}
        params = dict(description='Asger was here!',
                      categories=['One', 'More', 'File Uploaded'])
        params['forceReplace'] = True
        params_as_json_string = json.dumps(params)
        payload = dict(jsonData=params_as_json_string)
        req = requests.post(url, data=payload, files=files)
        print('-' * 40)
        print(req.json())
        print(req.status_code)

def thread_work():
    """Function for thread work"""
    print("Uploading file")
    upload_file()
    sleep(TIMEOUT)

def start_threads():
    """Function that launches threads"""
    for _ in range(1, RANGE):
        create_file()
    thread1 = Thread(target=thread_work)
    thread1.start()

def main():
    """main"""
    start_threads()

if __name__ == '__main__':
    main()
