import json
import os
import re
import requests
from typing import Union
from natsort import natsorted


Json = Union[dict, list, str, int, float, bool, None]


def download_json(url: str, use_cache: bool = True) -> Json:
    directory = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(directory, "../../__cache__")
    if not os.path.exists(fn):
        os.mkdir(fn)
    url2 = url.replace(":", "")
    fn = os.path.join(fn, url2.replace("/", "@"))

    if use_cache and os.path.exists(fn):
        with open(fn) as f:
            j = json.load(f)
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
        page = requests.get(url, headers=headers)
        j = page.json()
        if use_cache:
            with open(fn, "w") as f:
                json.dump(j, f)
    return j


def get_latest_patch_version():
    versions = download_json("http://ddragon.leagueoflegends.com/api/versions.json", use_cache=False)
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
