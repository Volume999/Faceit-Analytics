import requests
import yaml
from yaml import load

# Testing getting API Key from Config.yaml
api_keys_stream = open('config.yaml', 'r')
faceit_api_key = yaml.load(stream=api_keys_stream,
                           Loader=yaml.Loader)['Keys']['Faceit-API']