import sqlite3

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
