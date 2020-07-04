import sqlite3

def create_db():
    '''This function creates a database called twitter.db
    it then creates a table in the db called tweet_info.'''
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE tweet_info
                (created_at TEXT,
                id_str TEXT,
                text TEXT,
                truncated BLOB,
                user_id_str TEXT,
                user_location TEXT,
                user_description TEXT,
                utc_offset TEXT,
                time_zone TEXT,
                geo_enabled BLOB,
                geo_long TEXT,
                geo_lat TEXT,
                long_coord TEXT,
                lat_coord TEXT,
                place_type TEXT,
                place_name TEXT,
                place_fullname TEXT,
                place_country TEXT,
                place_bounding_box_type TEXT,
                place_bounding_box_coords TEXT,
                full_tweet_text TEXT)''')

    conn.commit()
    conn.close()

def store_tweet(created_at, id_str, text, truncated, user_id_str, user_location,
user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord,
lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type,
place_bounding_box_coords, full_tweet_text):

    '''This function puts the relevant tweet information in the twitter.db tweet_info table.'''

    # DB connection
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

    # define query
    insert_query = "INSERT INTO tweet_info (created_at, id_str, text, truncated, user_id_str, user_location, user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type, place_bounding_box_coords, full_tweet_text) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    # insert tweet
    c.execute(insert_query, (created_at, id_str, text, truncated, user_id_str, user_location, user_description,
    utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname,
    place_country, place_bounding_box_type, place_bounding_box_coords, full_tweet_text))
    conn.commit()
    c.close()
    conn.close()
    return

# deal with file size for time efficiency tracker
import enum

# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes

import os

def get_file_size(file_name, size_type = SIZE_UNIT.BYTES ):
   """ Get file in size in given unit like KB, MB or GB"""
   size = os.path.getsize(file_name)
   return convert_unit(size, size_type)

from glob import glob
import time
import json

if __name__ == "__main__":
    # create the db
    create_db()

    start_time = time.time() # this is the start time of when this code was executed

    for filename in glob('*.json'): # loop over .json files in the cwd

        print(filename) # so we know which file we are working with

        for line in open(filename):

            tweet = [] # only save one tweet at a time in memory: gain efficiency

            try:

                tweet.append(json.loads(line))

                # grab all wanted data from the tweet
                created_at = tweet[0]['created_at']
                id_str = tweet[0]['id_str']
                text = tweet[0]['text']
                truncated = tweet[0]['truncated']
                user_id_str = tweet[0]['user']['id_str']
                user_location = tweet[0]['user']['location']
                user_description = tweet[0]['user']['description']
                utc_offset = tweet[0]['user']['utc_offset']
                time_zone = tweet[0]['user']['time_zone']
                geo_enabled = tweet[0]['user']['geo_enabled']

                if tweet[0]['coordinates'] != None:
                    geo_long = tweet[0]['geo']['coordinates'][1]
                    geo_lat = tweet[0]['geo']['coordinates'][0]
                else:
                    geo_long = None
                    geo_lat = None

                if tweet[0]['coordinates'] != None:
                    long_coord = tweet[0]['coordinates']['coordinates'][0]
                    lat_coord = tweet[0]['coordinates']['coordinates'][1]
                else:
                    long_coord = None
                    lat_coord = None

                if tweet[0]['place'] != None:
                    place_type = tweet[0]['place']['place_type']
                    place_name = tweet[0]['place']['name']
                    place_fullname = tweet[0]['place']['full_name']
                    place_country = tweet[0]['place']['country']
                    place_bounding_box_type = tweet[0]['place']['bounding_box']['type']
                    place_bounding_box_coords = str(tweet[0]['place']['bounding_box']['coordinates'])
                else:
                    place_type = None
                    place_name = None
                    place_fullname = None
                    place_country = None
                    place_bounding_box_type = None
                    place_bounding_box_coords = None

                try:
                    full_tweet_text = tweet[0]['retweeted_status']['extended_tweet']['full_text']
                except KeyError:
                    full_tweet_text = None

                # insert into db

                store_tweet(created_at, id_str, text, truncated, user_id_str, user_location,
                            user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord,
                            lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type,
                            place_bounding_box_coords, full_tweet_text)

            # Let me know if something bad happens
            except Exception as e:
                
                print("Error is", e) # this is because of the new line character
                continue

        # keep track of time and size of file: efficiency tracker

        # get time_delta
        new_time = time.time()
        time_delta = (new_time - start_time)
        minutes = time_delta / 60

        # get file size in python
        size = get_file_size(filename, SIZE_UNIT.GB)
        print(filename, 'of size', size ,  'GB took', minutes, 'mins to store in twitter.db')
