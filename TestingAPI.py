import requests
import yaml
from yaml import load
from urllib import parse

# Testing getting API Key from Config.yaml
api_keys_stream = open('config.yaml', 'r')
config = yaml.load(stream=api_keys_stream, Loader=yaml.Loader)
faceit_api_key = config['Keys']['Faceit-API']

player_id = config['Keys']['Player_id']
game_id = config['Keys']['Game_id']
region = config['Keys']['Region']
match_id = config['Keys']['Match_id']


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


def get_player_match_history(player_id, game_id, from_ = "", to_ = ""):
    relative_url = f'players/{player_id}/history'
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


get_player_match_history(player_id, game_id, region)
get_match_details(match_id)
get_match_statistics(match_id)
get_player_statistics(player_id)