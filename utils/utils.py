import json
import os
import re
from typing import Union
import requests
from natsort import natsorted


Json = Union[dict, list, str, int, float, bool, None]


def download_json(url: str, use_cache: bool = True) -> Json:
    directory = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(directory, "../../__cache__")
    if not os.path.exists(file_name):
        os.mkdir(file_name)
    url2 = url.replace(":", "")
    file_name = os.path.join(file_name, url2.replace("/", "@"))

    if use_cache and os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as file:
            j = json.load(file)
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
        page = requests.get(url, headers=headers, timeout=30)
        j = page.json()
        if use_cache:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(j, file)
    return j


def get_latest_patch_version():
    versions = download_json(
        "http://ddragon.leagueoflegends.com/api/versions.json", use_cache=False)
    versions = [v for v in versions if "_" not in v]
    versions = natsorted(versions)
    return versions[-1]


def get_patch_version_in_url(url, pattern):
    # pass a pattern and url and he find a patch version
    result = re.search(pattern, url)
    if result:
        patch = result.group(1)
        return patch
    else:
        raise ValueError("Error: not get patch version")

def get_father_directory_of_project():
    return os.environ.get("PYTHONPATH")
