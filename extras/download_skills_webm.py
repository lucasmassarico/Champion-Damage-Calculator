import requests
import os
import json


def download_webm(urls, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            file_name = os.path.join(directory, url.split("/")[-1])

            with open(file_name, "wb") as file:
                file.write(response.content)

            print(f"Webm {file_name} baixado com sucesso!")

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao baixar o webm {url}: {e}")


webm_urls = []
output_directory = "webm/"


def get_id_champions():
    meraki_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"

    response = requests.get(meraki_url)
    response.raise_for_status()

    champions = json.loads(response.content)
    for champion_name, champion in champions.items():
        champion_id = champion["id"]
        if champion_name == "Annie":
            print(champion_id)
        if champion_id < 10:
            id_for_url = f"000{champion_id}"

        elif champion_id < 100:
            id_for_url = f"00{champion_id}"

        else:
            id_for_url = f"0{champion_id}"
        url_p = f"https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{id_for_url}/ability_{id_for_url}_P1.webm"
        url_q = f"https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{id_for_url}/ability_{id_for_url}_Q1.webm"
        url_w = f"https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{id_for_url}/ability_{id_for_url}_W1.webm"
        url_e = f"https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{id_for_url}/ability_{id_for_url}_E1.webm"
        url_r = f"https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{id_for_url}/ability_{id_for_url}_R1.webm"
        webm_urls.append(url_p)
        webm_urls.append(url_q)
        webm_urls.append(url_w)
        webm_urls.append(url_e)
        webm_urls.append(url_r)


get_id_champions()
download_webm(webm_urls, output_directory)
