# TODO
# 1) Figure out how to download data from API (which calls to make) - DONE
# 2) Make storing strategy - DONE
# 3) Implement Storing Strategy
# 4) Logging
# 5) Error Handling
# 6) Retries
# 7) Testing

import psycopg2
import requests
import yaml
from urllib import parse
import logging
import TestingAPI as api
from hdfs import InsecureClient
from pywebhdfs.webhdfs import PyWebHdfsClient
from datetime import datetime

# Testing getting API Key from Config.yaml
api_keys_stream = open('config.yaml', 'r')
config = yaml.load(stream=api_keys_stream, Loader=yaml.Loader)
faceit_api_key = config['Keys']['Faceit-API']
database_connection_details = config['Database']['postgres']
hdfs_connection_details = config['Database']['hdfs']


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
    hdfs_client = InsecureClient(url=f'http://{hdfs_connection_details["host"]}:{hdfs_connection_details["port"]}',
                                 user=hdfs_connection_details['user'])
    current_date_time = datetime.now()

    for (player_id, region_name, game_name) in clients:
        matches = api.get_player_match_history(player_id, game_name,
                                               region_name).json()  # Match history with small details
        hdfs_client.write(
            hdfs_path=f'data/raw/matches/{player_id}/{current_date_time.year}/{current_date_time.month}/{current_date_time.day}/{current_date_time.strftime("%H.%M.%S")}',
            data=matches,
            overwrite=True)
        player_statistics = api.get_player_statistics(player_id).json()  # Player statistics and statistics per map
        hdfs_client.write(
            hdfs_path=f'data/raw/player_statistics/{player_id}' +
                      f'/{current_date_time.year}/{current_date_time.month}/{current_date_time.day}' +
                      f'/{current_date_time.strftime("%H.%M.%S")}.json',
            data=player_statistics,
            overwrite=True
        )
        player_details = api.get_player_details(player_id).json()  # Friend list
        hdfs_client.write(
            hdfs_path=f'data/raw/player_details/{player_id}/{current_date_time.year}/{current_date_time.month}/{current_date_time.day}/{current_date_time.strftime("%H.%M.%S")}',
            data=player_details,
            overwrite=True
        )
        print("Matches downloaded: ", len(matches['items']))
        for match in matches['items']:
            match_details = api.get_match_details(match['match_id']).json()  # Match details - Server, Maps chosen
            hdfs_client.write(
                hdfs_path=f'data/raw/match_details/{match["match_id"]}/{current_date_time.strftime("%H.%M.%S")}',
                data=match_details,
                overwrite=True
            )
            match_statistics = api.get_match_statistics(match['match_id']).json()  # Match statistics for players
            hdfs_client.write(
                hdfs_path=f'data/raw/match_statistics/{match["match_id"]}/{current_date_time.strftime("%H.%M.%S")}',
                data=match_statistics,
                overwrite=True
            )
            break


if __name__ == '__main__':
    main()
