import requests, re
from extras.old.Data.Classes.useful import WikiPageRetriever, urls
from bs4 import BeautifulSoup


class ChampionsStatusTransform:
    def __init__(self):
        self._champions_all_attributes = WikiPageRetriever(url=urls['champion_data']).return_dict()
        self._champions = self._get_champion_list_name()

    def _get_champion_list_name(self):
        champion_status = {}
        for name, champion in self._champions_all_attributes.items():
            self._remove_unnecessary_stats(champion['stats'])
            champion_status[name] = self._champion_stats(champion)
        return champion_status

    @staticmethod
    def _champion_stats(champion):
        stats = {
            'champion_id': champion['id'],
            'apiname': champion['apiname'],
            'resource': champion['resource'],
            'adaptivetype': champion['adaptivetype'],
            'stats': champion['stats']
        }

        if champion['id'] != float(240.1) and champion['id'] != float(150.2):
            stats['skills'] = champion['skills']

        return stats

    @staticmethod
    def _remove_unnecessary_stats(stats):
        for key in ['urf', 'aram', 'usb']:
            stats.pop(key, None)

    def return_champions(self):
        return self._champions


class SkillsScrapperModel:
    def __init__(self, url):
        self._url = url
        self._skills_of_champion()

    @classmethod
    def _request_wiki(cls, url):
        return requests.get(url)

    def _return_dict_ability_container(self):
        self._request = self._request_wiki(self._url)
        wiki_html = BeautifulSoup(self._request.content, 'html.parser')
        skills_html = wiki_html.findAll('div', class_='ability-info-container')
        return skills_html

    def _skills_of_champion(self):
        skills_html = self._return_dict_ability_container()
        damage_aux = str(skills_html[1].find_all('dd')[0].next)
        damage = self._remove_special_caracters(damage_aux)
        self._remove_empty_elements_from_list(damage)
        damages_list = self._create_list_with_integer(damage)

        aux = str(skills_html[1].find_all('dd')[0].span.next)
        scaling_aux = self._remove_special_caracters(aux)
        self._remove_empty_elements_from_list(scaling_aux)
        scalings = self._create_list_with_integer(scaling_aux)
        return scalings

    @staticmethod
    def _remove_special_caracters(string):
        return re.sub(r"[(+\xa0%)/]", "", string).split(" ")

    @staticmethod
    def _remove_empty_elements_from_list(list_with_space):
        for element in list_with_space:
            if element == "":
                list_with_space.remove(element)
        return list_with_space

    @staticmethod
    def _create_list_with_integer(list_with_str):
        new_list = []
        for num, scalling in enumerate(list_with_str):
            if scalling.isdigit():
                new_list.insert(num, int(scalling))
            else:
                new_list.insert(num, scalling)
        return new_list

    @staticmethod
    def _separate_list_int_str():
        pass

    def return_skills(self):
        return self._skills_of_champion()


class Aatrox(SkillsScrapperModel):
    def __init__(self, url):
        super().__init__(url)
        self._url = url
