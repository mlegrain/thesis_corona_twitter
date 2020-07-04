import tweepy
import sys
import json
import time
import sqlite3

keywords = ['coronavirus', 'covid-19', 'corona virus', 'virus', 'flu', 'cold',
'disease', 'outbreak', 'epidemic', 'pandemic', 'Wuhan', 'health', 'public health',
'SARS', 'ebola', 'WHO', 'CDC', 'Mike Pence', 'cases', 'death', 'fatality', 'fatalities',
'Mohammad Mirmohammadi', 'recovery', 'recoveries', 'symptoms', 'pneumonia',
'fever', 'cough', 'headache', 'prevention', 'masks', 'transmission', 'transmit',
'contagion', 'contagious', 'spread', 'widespread', 'infection', 'infections',
'infected', 'elderly', 'treatment', 'self-isolate', 'quarantine', 'tested positive',
'vaccine', 'virus fear', 'treatment', 'diagnosis', 'diagnosed', 'diagnostics',
'Iran', 'China', 'Korea', 'Italy', 'emergency', 'NHS', 'PHE', 'lockdown', 'UKlockdown',
'social distancing', 'confinement', 'confined', 'deconfinement']

# Twitter authentication
auth = tweepy.OAuthHandler("wY5tZomH1jUKbFah7ooEuwAeW", "IPHMBer6yiV2og5uaU8pynxuXtfvzlmmWmnbJn6lKtaEChumCp")
auth.set_access_token("1195096510863679494-FBhnMKaYy9qhMS0Z1S8qJwzrfQFh1p", "Dy8oeMKf2eDTb7Q1Oxquo9Gd10HMlPvaQ5dd6rZXVlnBn")
api = tweepy.API(auth)

def store_data(created_at, id_str, text, truncated, user_id_str, user_location,
user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord,
lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type,
place_bounding_box_coords, full_tweet_text):
    # DB creation/connection
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    insert_query = "INSERT INTO tweet_info (created_at, id_str, text, truncated, user_id_str, user_location, user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type, place_bounding_box_coords, full_tweet_text) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    c.execute(insert_query, (created_at, id_str, text, truncated, user_id_str, user_location, user_description,
    utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname,
    place_country, place_bounding_box_type, place_bounding_box_coords, full_tweet_text))
    conn.commit()
    c.close()
    conn.close()
    return

# Stream Listener class
class StreamListener(tweepy.StreamListener):

    # When data is received
    def on_data(self, data):

        # Error handling
        try:

            # Make it JSON
            datajson = json.loads(data)

            # grab the wanted data from the Tweet
            created_at = datajson['created_at']
            id_str = datajson['id_str']
            text = datajson['text']
            truncated = datajson['truncated']
            user_id_str = datajson['user']['id_str']
            user_location = datajson['user']['location']
            user_description = datajson['user']['description']
            utc_offset = datajson['user']['utc_offset']
            time_zone = datajson['user']['time_zone']
            geo_enabled = datajson['user']['geo_enabled']

            if datajson['coordinates'] != None:
                geo_long = datajson['geo']['coordinates'][1]
                geo_lat = datajson['geo']['coordinates'][0]
            else:
                geo_long = None
                geo_lat = None

            if datajson['coordinates'] != None:
                long_coord = datajson['coordinates']['coordinates'][0]
                lat_coord = datajson['coordinates']['coordinates'][1]
            else:
                long_coord = None
                lat_coord = None

            if datajson['place'] != None:
                place_type = datajson['place']['place_type']
                place_name = datajson['place']['name']
                place_fullname = datajson['place']['full_name']
                place_country = datajson['place']['country']
                place_bounding_box_type = datajson['place']['bounding_box']['type']
                place_bounding_box_coords = str(datajson['place']['bounding_box']['coordinates'])
            else:
                place_type = None
                place_name = None
                place_fullname = None
                place_country = None
                place_bounding_box_type = None
                place_bounding_box_coords = None

            try:
                full_tweet_text = datajson['retweeted_status']['extended_tweet']['full_text']
            except KeyError:
                full_tweet_text = None

            # insert the data into the sqlite3 database
            store_data(created_at, id_str, text, truncated, user_id_str, user_location, user_description,
            utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname,
            place_country, place_bounding_box_type, place_bounding_box_coords, full_tweet_text)
            print("success")

        # Let me know if something bad happens
        except Exception as e:
            print(e)
            pass

        return True

import time

# Driver
if __name__ == "__main__":
    while True:

        # Run the stream!
        l = StreamListener()
        stream = tweepy.Stream(auth, l)
        try:
            print("streaming...")
            # Filter the stream for keywords and english language
            stream.filter(track = keywords, languages = ['en'])

        except Exception as e:
            print("error. Restarting Stream... Error:")
            time.sleep(60)
