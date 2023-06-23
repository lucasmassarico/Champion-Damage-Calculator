import json
import os

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_user = os.environ.get("API_DB_LOGIN")
db_pass = os.environ.get("API_DB_PASSWORD")

'''
Necessário realizar uma refatoração neste código, criando uma função e provavelmente um Endpoint 
que realize este update, para quando estiver em produção, seja possível atualizar o BD facilmente.
precisamos também inserir o patch em que o champion está inserido no banco.
'''

response = requests.get(
    'https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json')
data = response.content
data_dict = json.loads(data)
champions = dict()

for champion_name, champion in data_dict.items():
    if champion['stats'].get('aramDamageTaken'):
        champion['stats'].pop('aramDamageTaken')
    if champion['stats'].get('aramDamageDealt'):
        champion['stats'].pop('aramDamageDealt')
    if champion['stats'].get('aramHealing'):
        champion['stats'].pop('aramHealing')
    if champion['stats'].get('aramShielding'):
        champion['stats'].pop('aramShielding')
    if champion['stats'].get('urfDamageTaken'):
        champion['stats'].pop('urfDamageTaken')
    if champion['stats'].get('urfDamageDealt'):
        champion['stats'].pop('urfDamageDealt')
    if champion['stats'].get('urfHealing'):
        champion['stats'].pop('urfHealing')
    if champion['stats'].get('urfShielding'):
        champion['stats'].pop('urfShielding')

    champion_id = champion['id']
    champion_dict = {
        "name": champion['name'],
        "resource": champion['resource'],
        "attackType": champion['attackType'],
        "adaptiveType": champion['adaptiveType'],
        "stats": champion['stats'],
        "abilities": champion['abilities']
    }

    login_json = {
        'username': db_user,
        'password': db_pass
    }
    url_login = f"http://127.0.0.1:5999/login"
    headers_login = {
        "Content-Type": "application/json"
    }
    login_token_json = requests.post(url_login, data=json.dumps(login_json), headers=headers_login)
    token = json.loads(login_token_json.content).get('access_token')

    url = f"http://127.0.0.1:5999/champions/{champion_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {token}'

    }
    request_put = requests.put(url, data=json.dumps(champion_dict), headers=headers)

    if request_put.status_code in (200, 201):
        print('Requisição PUT bem sucedida!')
    else:
        print("'Erro na requisição PUT'\n", "message:", request_put.status_code)
        print("content:", request_put.content, end='\n\n')
