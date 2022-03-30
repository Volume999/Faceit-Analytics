import requests
import yaml
from yaml import load
from urllib import parse

# Testing getting API Key from Config.yaml
api_keys_stream = open('config.yaml', 'r')
config = yaml.load(stream=api_keys_stream, Loader=yaml.Loader)
faceit_api_key = config['Keys']['Faceit-API']

player_id = config['Debug']['Player_id']
game_id = config['Debug']['Game_id']
region = config['Debug']['Region']
match_id = config['Debug']['Match_id']


def make_faceit_api_call(relative_url="", payload=None):
    if payload is None:
        payload = {}
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {faceit_api_key}'
    }
    payload["offset"] = 0
    payload["limit"] = 20
    root_url = 'https://open.faceit.com/data/v4/'
    url = parse.urljoin(root_url, relative_url)
    response = requests.get(url, headers=headers, params=payload)
    return response


def get_player_id(player_nickname):
    payload = {
        "nickname": f'{player_nickname}'
    }
    relative_url = "search/players"
    response = make_faceit_api_call(relative_url=relative_url,
                                    payload=payload)
    return response


def list_games():
    payload = {
    }
    relative_url = "games"
    response = make_faceit_api_call(relative_url, payload)
    return response


def get_game_details(game_id):
    relative_url = f'games/{game_id}'
    response = make_faceit_api_call(relative_url)
    return response


def get_player_match_history(player_id, game_id, from_="", to_=""):
    relative_url = f'players/{player_id}/history'
    # One month back if not specified
    payload = {
        "game": game_id,
        "from": from_,
        "to": to_
    }
    response = make_faceit_api_call(relative_url, payload)
    return response


def get_player_ranking_in_game(player_id, game_id, region):
    relative_url = f'rankings/games/{game_id}/regions/{region}/players/{player_id}'
    response = make_faceit_api_call(relative_url)
    return response


def get_player_details(player_id):
    relative_url = f'players/{player_id}'
    response = make_faceit_api_call(relative_url)
    return response


def get_match_details(match_id):
    relative_url = f'matches/{match_id}'
    response = make_faceit_api_call(relative_url)
    return response


def get_match_statistics(match_id):
    relative_url = f'matches/{match_id}/stats'
    response = make_faceit_api_call(relative_url)
    return response


def get_player_statistics(player_id):
    relative_url = f'players/{player_id}/stats/{game_id}'
    response = make_faceit_api_call(relative_url)
    return response


# print(get_player_match_history(player_id, game_id, region).json())  # Match history with small details
# print(get_match_details(match_id).json())  # Match details - Server, Maps chosen
# print(get_match_statistics(match_id).json())  # Match statistics for players
# print(get_player_statistics(player_id).json())  # Player statistics and statistics per map
# print(get_player_details(player_id).json())  # Friend list
