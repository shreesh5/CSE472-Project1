import json
from twython import Twython, TwythonRateLimitError, TwythonAuthError
import time
import pickle
import csv
import numpy as np
import os

## Player twitter handles to be scraped
players = ['KingJames', 'stephenasmith', 'RealSkipBayless', 'SHAQ', 'MagicJohnson', 'DwyaneWade', 'kobebryant', 'KyrieIrving', 'StephenCurry30', 'KDTrey5']

## Initializing social_network and Id_map dictionary
social_network = dict()
id_map = dict()

## Path to read Credentials file
## Create a Credentials folder
credentials_path = 'Credentials/twitter_credentials.json'
with open(credentials_path, "r") as file:
    cred = json.load(file)
    consumer = cred["CONSUMER_KEY"]
    consumer_secret = cred["CONSUMER_SECRET"]
    access = cred["ACCESS_KEY"]
    access_secret = cred["ACCESS_SECRET"]

## Function to get 50 random followers for each celebrity
## Stores the ID, name and screen_name of each follower and players
## Essentially forms the users of our social network

def get_player_followers():
    for player in players:
        row = []
        users = api.get_followers_list(screen_name=player, count=50)
        users = users['users']
        print player
        for user in users:
            row.append([user['id']])
            map_idx(user['id'],user['name'],user['screen_name'])
        s = player + '.csv'
        with open(s,'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(row)
        csvFile.close()

## Function to re-initialize the twythoon api client
## Used when rate limit is exceeded

def init_api():
    api = Twython(consumer, consumer_secret, access, access_secret)
    return api

## Exception Handling when Rate Limit is EXCEEDED
## Only 15 calls every 15 mins are allowed
## Calculated time left before next call can be made and sleeps
def handle_rate_limit(api):
    # remainder -> time left for next call
    remainder = float(api.get_lastfunction_header('x-rate-limit-reset')) - time.time()
    print "RATE LIMIT EXCEEDED - SLEEPING for {} seconds".format(remainder)
    time.sleep(remainder + 3)
    # Re-initialize twython client
    api = init_api()
    print "AWAKE\n"
    return api

## Code to load existing social_network and Id_map pickle files
def load_dicts():
    try:
        with open('social_network.pkl', 'rb') as f:
            social_network = pickle.load(f)
        with open('id_map.pkl', 'rb') as f:
            id_map = pickle.load(f)
    except:
        social_network = dict()
        id_map = dict()
    return social_network, id_map

## Code to dump Id_Map and social_network as pickle objects
def dump():
    with open('social_network.pkl', 'wb') as f:
        print "Size of social network is {}".format(len(social_network))
        pickle.dump(social_network, f)
    with open('id_map.pkl', 'wb') as f:
        pickle.dump(id_map, f)

## Clean Social network
## Nodes which are private accounts are removed
def clean_network(network):
    for id in network.keys():
        if network[id] == -1:
            del network[id]
    return network

## Function to fill values of Id_map Dictionary
## ID -> [Name, screen_name] mapping
def map_idx(id, name, screen_name):
    id_map[id] = {'name':name, 'screen_name':screen_name}

## Wraps twython api call function with exception Handling
## TwythonRateLimitError implies 15 calls are exceed
## TwythonAuthError implies said account is private
## Returns list of user ID's
def make_api_call(api, id):
    try:
        users = api.get_friends_ids(id=id)
    except TwythonRateLimitError:
        api = handle_rate_limit(api)
        return make_api_call(api, id=id)
    except TwythonAuthError:
        return -1
    return users

## Add a user to social_network
## Check if user ID exist in network first
## For private account set value as -1, used for deletion later
def add_user_to_network(id, api):
    users = make_api_call(api=api, id=id)
    if users == -1:
        print "Private acct"
        social_network[id] = -1
        return
    social_network[id] = users['ids']

    # Save social_networkon each update
    #dump()

## Twitter hack to retrieve all Player details in One function call
## The screen_name below, only follows the players we are interested in
def get_player_details(api):
    # Get friends of the user
    player_details = api.get_friends_list(screen_name='shreesh73895021')
    for f in player_details['users']:
        map_idx(f['id'], f['name'], f['screen_name'])
        if int(f['id']) not in social_network.keys():
            add_user_to_network(f['id'], api)
    return player_details

if __name__ == "__main__":
    api = init_api()
    social_network, id_map = load_dicts()
    ## Run the line below to get 50 followers for each player in a CSV
    get_player_followers()
    ## Iterate through player handles
    for player in players:
        # Read CSV containing followers
        with open(player + '.csv','r') as f:
            reader = csv.reader(f)
            users = list(reader)

        # For each user in the CSV
        # Add user to social_network
        for u in users:
            if int(u[0]) not in social_network.keys():
                add_user_to_network(int(u[0]), api)
        print "{} is completed".format(player)

    # Get list of friends and ID of each player
    player_details = get_player_details(api)

    # Clean social_network, i.e remove private accounts
    social_network = clean_network(social_network)
    #dump()
