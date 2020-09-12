## Master's thesis project at the LSE: Blog Part 1 

# How do Twitter users experience COVID-19? 
# A sentiment analysis and topic modelling approach

The coronavirus pandemic has fundamentally changed our lives. It has altered the way we socialize with others, walk down the street, shop for essentials, travel and work. As part of my Master’s degree in Applied Social Data Science at the London School of Economics and Political Science (LSE), I decided to focus my capstone project on this crisis. Precisely, I made it my mission to diagnose how twitter users in the United Kingdom were experiencing this pandemic, how they responded to policies, and finally understand what topics of discussion fed their emotions. I decided to use Twitter as on this micro-blogging platform, users share their candid reactions and feelings to events. 

As I started this research, it came to my attention that finding centralized information to help a data scientist conduct a big data project was challenging. I therefore decided to share the knowledge I have acquired throughout this journey, the tips and helpful resources I found along the way with this community. Here is Part 1 of a series of blog posts designed in this aim where I run you through my Data Collection strategy. As summary, I used continuously streamed tweets since March using AWS computing power. Below, I explain everything from set up to storage. 

To collect Social Media data, and precisely Twitter data, you have to use an API. An Application Programming Interface, or API, can be used to share data between systems and therefore comes in very handy for most developers. In simple terms, it acts as a messenger which receives a data request, processes it, and returns the system’s response. In this case, the Twitter API is your portal to the data; upon request it will grant you access to some data (however, if you are using the Standard APIs, then your access will be restricted). There are two kind of Standard APIs (free) made available by Twitter: the REST APIs and the Streaming APIs. The former enables you to retrieve tweets from the past 7 days as well as any related information. The latter is a gateway to retrieving real-time tweets, collected as they are posted. If you are interested in working on a project involving the REST APIs, I invite you to read Twitter’s guides for developers for further information as I used the Streaming API for this project.

In order to collect tweets, you first need to create a Twitter developer account which will equip you with your unique authentications used to request the Twitter API.

1)	**Setting up a Twitter developer account and an app**

As mentioned on Twitter’s developer page, “All new developers must apply for a developer account to access Twitter APIs”. Follow this [link](https://developer.twitter.com/en/apply-for-access) to start the process. You will be asked to sign into your Twitter account and answer questions detailing what you will use the APIs for. 

Once your developer account is created and verified, head on [here](https://twitter.com/login?redirect_after_login=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fapps) to create a new app. Once you filled in the details, you can create your access token. 

Two keys, (1) API key – also known as consumer key – and (2) API secret key –known as consumer secret, and two tokens, (1) Access token – or OAuth access token – and (2) Access token secret – or OAuth access token secret, are needed to connect to the API. These codes are unique to your account and should not be shared. Make sure to note down your Access token and Access token secret as these two codes will not be visible after creation.

Congratulations! You now successfully created an app. You can now use it to connect to Twitter’s APIs. 

2)	**Setting up an AWS account and instance**

For my project, I had to continuously stream tweets for several months without any interruption. This is not wise to do on a basic laptop, as it would have to stay open and running for months. Therefore, I decided to use AWS. 

Let’s set it up! 

First, we have to create an AWS account, [click the hyperlink](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) to have details on how to set up the account. Start [here](https://aws.amazon.com/) and click on “Create an AWS account”. Follow the instructions by filling in all the required information. Note that your account can take up to 24h to be approved. In addition, AWS accounts include 12 months of Free Tier Access. 

Now that we have an AWS account, we need to create our EC2 instance. I followed [this guide](https://druce.github.io/aws) in my setup. If you wish to conduct a project similar to mine, you’ll need to go through steps 1-3. Make sure to follow the tutorial exactly, line by line, so no errors occur. It is very important that you store in a memorable place your AWS key as you will always need it to access your instance from terminal.

3)	**Create a database to store the data**

I decided to store my data in a SQLite database, as it is a light weight database which was designed to be efficient, reliable, independent and simple. However, note that I recognize in hindsight that for the purpose of my project, it would have made more sense to use a non-relational database. 

In order to create this database and conduct my data collection, I used **Python**.

Onto the code… Don’t worry, I commented my code thoroughly to make sure each step is clear to you!

First, I created a database to store the collected data. 

Here’s the code I wrote:

```python
# import the required library
import sqlite3

# create the databse, I named mine 'twitter.db'
conn = sqlite3.connect('twitter.db')
# set up the connection
c = conn.cursor()

# create a table in this database called tweet_info
# add the names of required columns followed by the variable type
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

# save and commit changes
conn.commit()
# always close the connection when you are done
conn.close()
```

4)	**Stream the tweets: write and understand the code**

Now that we created our Twitter developer account and app, that we set up an AWS account and our instance, and that we have a place to store our tweets, we can move on to the code used to collect tweets. I used python and the Tweepy library, which is specifically designed to ease working with Twitter’s APIs. 

Now’s the time to get your unique keys and tokens.

```python
# import all required libraries
import tweepy
import sys
import json
import time
import sqlite3

# prepare a list of key words you want to use to filter the API stream
keywords = ['coronavirus', 'covid-19', 'corona virus', 'virus', 'flu', 'cold',
'disease', 'outbreak', 'epidemic', 'pandemic', 'Wuhan', 'health', 'public health',
'SARS', 'ebola', 'WHO', 'CDC', 'cases', 'death', 'fatality', 'fatalities',
'recovery', 'recoveries', 'symptoms', 'pneumonia', 'fever', 'cough', 'headache',
'prevention', 'masks', 'transmission', 'transmit', 'contagion', 'contagious',
'spread', 'widespread', 'infection', 'infections', 'infected', 'elderly',
'treatment', 'self-isolate', 'quarantine', 'tested positive', 'vaccine',
'virus fear', 'treatment', 'diagnosis', 'diagnosed', 'diagnostics',
'Iran', 'China', 'Korea', 'Italy', 'emergency', 'NHS', 'PHE', 'lockdown',
'UKlockdown', 'social distancing', 'confinement', 'confined', 'deconfinement']

# Twitter authentication
# these codes are unique, do not share them
auth = tweepy.OAuthHandler("XXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXX")
auth.set_access_token("XXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXX")
api = tweepy.API(auth)

# create a first function called store_data
def store_data(created_at, id_str, text, truncated, user_id_str, user_location,
user_description, utc_offset, time_zone, geo_enabled, geo_long, geo_lat, long_coord,
lat_coord, place_type, place_name, place_fullname, place_country, place_bounding_box_type,
place_bounding_box_coords, full_tweet_text):

'''The store_data function will store only the fields of the data received that
are of interest. '''

    # connect to the DB we created in section 3. I called mine 'twitter.db'
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

    # this is the SQL query I will use to fill the table. This is naming the
    # column names of the table and saying that values will fill these columns
    # the specific values are marked by ?. Note that there are as many ? as
    # number of columns.
    insert_query = "INSERT INTO tweet_info (created_at, id_str, text, truncated, "\
    "user_id_str, user_location, user_description, utc_offset, time_zone, "\
    "geo_enabled, geo_long, geo_lat, long_coord, lat_coord, place_type, place_name, "\
    "place_fullname, place_country, place_bounding_box_type, place_bounding_box_coords, "\
    "full_tweet_text) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    # 
    c.execute(insert_query, (created_at, id_str, text, truncated, user_id_str,
    user_location, user_description, utc_offset, time_zone, geo_enabled, geo_long,
    geo_lat, long_coord, lat_coord, place_type, place_name, place_fullname,
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
            store_data(created_at, id_str, text, truncated, user_id_str,
            user_location, user_description, utc_offset, time_zone, geo_enabled,
            geo_long, geo_lat, long_coord, lat_coord, place_type, place_name,
            place_fullname,place_country, place_bounding_box_type,
            place_bounding_box_coords, full_tweet_text)
            print("success")

        # Let me know if something bad happens
        except Exception as e:
            print(e)
            pass

        return True

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
```

5)	**Stream the tweets: run the code in your AWS EC2 instance**

I used FileZilla to transfer my .py code files from my laptop to the instance in order to run the code on AWS. Click here to download FileZilla for Mac; or here to get it for Windows (there is also a 32bit version available for Windows). Go through the installation process.

Once it is installed, go to “File” and click on “Site Manager …”. Create a new site. Here is how you should fill in the blanks:

-	Protocol: Select “SFTP – SSH File Transfer Protocol”.
-	Host: Sign into your AWS account. Click on “EC2” then “Running Instances” to view your EC2 instances and copy the Public DNS (IPv4). This information is found either by scrolling to the right of the instance row or can be directly copied from the description of your instance. Paste this host reference here.
-	Logon type: Select “Key file”.
-	User: Write “ubuntu” as when you follow the suggested tutorial this is what you set up.
-	Key file: Select the path where you store your AWS access key.

Now that you created a connection to transfer from/to, you can connect to it by clicking on “Server” then “Reconnect” or by going in “File”, “Site Manager…”, clicking on the site you want to connect to and clicking “Connect”. Another way is also to click on the icon with a green tick. You will now see on the right-hand side your EC2 instance directory.

Transfer both .py files you have for 1) creating your database and 2) streaming the tweets from a directory on your laptop or hard drive onto the AWS instance.

Now that the code is in the instance, open a terminal window. Change your directory to the place where your AWS key is located using “cd /the_path_where_the_key_is/”. Connect to your instance using the following line of code: ssh -i “key_name” ubuntu@“your_IP_address”. Note that your IP address can be found under IPv4 Public IP either by scrolling to the right of the instance row or copying it from the description of your instance. You should now be connected to your instance from your terminal. There will be a message welcoming you onto the system. 

Now, you can run the code. First, run “python create_db.py”. As we saw above, this will create the database with our desired table. Second, run “nohup python DBstream.py &”. Using nohup enables the code to run in the background even if you disconnect yourself from the instance. The output returned from your code will be stored in a nohup.out file. When you run this line of code, a unique code process number will be returned. Be sure to keep this number safe as you will need it to kill this process.

Now that your code is up, running and that the tweets are being collected, you can log out from your instance on terminal by clicking on “control” and “d”.

6)	**Transfer the data you collected onto your computer or hard drive**

If you followed the tutorial I suggested above to set up your AWS instance, there is 30GB of storage on your instance. This means that once you are approaching the capacity of your instance, you need to transfer the data and store it somewhere else, such as on your computer if it has enough storage space or on a hard drive. 

Here are two options to check how much storage is left on your instance:

a.	As in 5), open a terminal window. Change your directory to the place where your AWS key is located using “cd /the_path_where_the_key_is/”. Connect to your instance using the following line of code: ssh -i “key_name” ubuntu@“your_IP_address”. The welcome message usually tells you how much storage is in use next to “Usage of /:”. However, sometimes the welcome message looks different. Therefore, here is a second hack:
b.	Open FileZilla, connect to the instance (click the icon with the green tick). Under the directory list it will indicate the “Total Size” used up. Once it gets close to 20GB, that’s the maximum to transfer your file. Indeed, 10GB are used by the instance itself.

As mentioned above in 5), I use FileZilla for transfers to and from my AWS instance. This time, you want to transfer the data collected on AWS to your computer or hard drive.

Connect to your connection as mentioned before (click the icon with the green tick). Now that the directory appeared on the right, change the name of the file you want to transfer to something meaningful. This will interrupt the streaming process slightly, as no more tweets are being fed into this file. Double click on this file. It will now transfer onto the directory selected on the left. You can now delete the nohup.out file and the twitter.db file (as the new one is empty).

I ran into quite a few issues during transfers as 20GB takes a while or can even crash when your WiFi isn’t the best. To avoid this problem, I advise you to connect directly to your internet with an Ethernet cable. 

Once the transfer is done, you can disconnect from the connection.

7)	**Continue the streaming after the transfer**

In my case, I continuously streamed for months. Therefore, as soon as my file was in the process of being transferred, I made sure to get the streaming back and running.

Remember the code process number generated after running “nohup python DBstream.py &” in Bash? Now, open terminal and reconnect to your EC2 instance, as we did above. Run “kill “process_number”” to interrupt the previous process. 

To start a new one, run “python create_db.py” and then “nohup python DBstream.py &” once more. Now, your stream is working again. 

If you forgot your code process number, do not worry. Here’s an easy tip, in terminal still in your instance, run “ps -ef |grep python” this will output all the processes up and running using python. You will see that one of the rows is for our code process “python DBstream.py”. To the left, you can find the process number.

8)	**Merging all your databases together**

In my case streaming for months about THE hot topic of the moment means that I have many .db files. Here’s how to merge two databases if you are interested.

Open terminal. Set a working directory where your databases are stored. Follow these steps, run:

```bash
sqlite3 “db_A.db” # The SQLite interface will now open
```

Note that if for some reason your mac does not have it follow this.

```bash
“attach “db_B.db” as toMerge;” # this links a database to the main one.
“BEGIN;”
“insert into tweet_info select * from toMerge.tweet_info;” # here you are copying all rows from the linked database to the main database.
“COMMIT;” # saving the changes.
“detach database toMerge;” # unlinking both databases.
```
Now, exit sqlite by pressing on “control” and “d”. Both databases should now be merged into “db_A.db”.
