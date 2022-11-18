import os
import requests
from pprint import pprint


def get_token():
    with open("token.txt", "r") as file_to_upload:
        return file_to_upload.readline()


class YaUploader:
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    @property
    def header(self):
        return self.get_headers()

    def get_upload_link(self, file_path):
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.header)
        pprint(response.json())
        return response.json()

    def upload(self, file_path):
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, "rb") as file_to_upload:
            response = requests.put(href, data=file_to_upload)
            if response.status_code == 201:
                print("Файл загружен")
                return True
            print("Файл не загружен потому что", response.status_code)
            return False


files_to_upload = os.listdir('files_to_upload')
uploader = YaUploader(get_token())
os.chdir('files_to_upload')
for file in files_to_upload:
    uploader.upload(file)
