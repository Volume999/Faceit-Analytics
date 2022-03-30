# TODO
# 1) Figure out how to download data from API (which calls to make) - DONE
# 2) Make storing strategy
# 3) Logging
# 4) Error Handling
# 5) Retries
# 6) Testing

import psycopg2
import requests
import yaml
from urllib import parse
import logging
import TestingAPI as api

# Testing getting API Key from Config.yaml
api_keys_stream = open('config.yaml', 'r')
config = yaml.load(stream=api_keys_stream, Loader=yaml.Loader)
faceit_api_key = config['Keys']['Faceit-API']
database_connection_details = config['Database']['postgres']


def get_database_connection():
    try:
        return psycopg2.connect(
            database="faceit_analytics_operations",
            user=database_connection_details['username'],
            password=database_connection_details['password'],
            host=database_connection_details['host'],
            port=database_connection_details['port']
        )
    except Exception as e:
        print(e)
        raise


def main():
    print("Initializing Database Connection")
    database_conn = get_database_connection()
    database_cursor = database_conn.cursor()
    print("Connection Complete")
    print("Querying the players to download data for")
    database_cursor.execute(r"""
    SELECT player_id, r.name as region_name, g.name as game_name
    FROM client_game_region cgr
    JOIN clients c on cgr.client_id = c.client_id
    JOIN games g on cgr.game_id = g.game_id
    JOIN regions r on cgr.region_id = r.region_id
    WHERE download_flag = TRUE
    AND c.date_deleted IS NULL
    """)
    clients = database_cursor.fetchall()
    print("Downloading data for players")
    for (player_id, region_name, game_name) in clients:
        matches = api.get_player_match_history(player_id, game_name,
                                               region_name).json()  # Match history with small details
        print(api.get_player_statistics(player_id).json())  # Player statistics and statistics per map
        print(api.get_player_details(player_id).json())  # Friend list
        print("Matches downloaded: ", len(matches['items']))
        for match in matches['items']:
            print(api.get_match_details(match['match_id']).json())  # Match details - Server, Maps chosen
            print(api.get_match_statistics(match['match_id']).json())  # Match statistics for players


if __name__ == '__main__':
    main()
