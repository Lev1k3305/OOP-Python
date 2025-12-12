import requests 

BASE_URL = "https://rickandmortyapi.com/api"

def search_character(name):
    response = requests.get(f"{BASE_URL}/character/?name={name}")
    if response.status_code == 200:
        data = response.json()
        return data['results'][0] if data['results'] else None
    return None

def get_character_by_id(char_id):
    response = requests.get(f"{BASE_URL}/character/{char_id}")
    return response.json() if response.status_code == 200 else None

def get_random_character():
    import random
    char_id = random.randint(1, 826)
    return get_character_by_id(char_id)

def search_episode(code):
    response = requests.get(f"{BASE_URL}/episode/?episode={code}")
    if response.status_code == 200:
        results = response.json()['results']
        return results[0] if results else None
    return None

def search_location(name):
    response = requests.get(f"{BASE_URL}/location/?name={name}")
    if response.status_code == 200:
        results = response.json()['results']
        return results[0] if results else None
    return None

def get_all_episodes():
    episodes = []
    page = 1
    while True:
        response = requests.get(f"{BASE_URL}/episode?page={page}")
        if response.status_code != 200 or not response.json()['results']:
            break
        data = response.json()
        episodes.extend(data['results'])
        if not data['info']['next']:
            break
        page += 1
    return episodes