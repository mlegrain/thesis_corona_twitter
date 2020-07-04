import tweepy
import sys
import json
import time

keywords = ['coronavirus', 'covid-19', 'corona virus', 'virus', 'flu', 'cold',
'disease', 'outbreak', 'epidemic', 'pandemic', 'Wuhan', 'health', 'public health',
'SARS', 'ebola', 'WHO', 'CDC', 'Mike Pence', 'cases', 'death', 'fatality', 'fatalities',
'Mohammad Mirmohammadi', 'recovery', 'recoveries', 'symptoms', 'pneumonia',
'fever', 'cough', 'headache', 'prevention', 'masks', 'transmission', 'transmit',
'contagion', 'contagious', 'spread', 'widespread', 'infection', 'infections',
'infected', 'elderly', 'treatment', 'self-isolate', 'quarantine', 'tested positive',
'vaccine', 'virus fear', 'treatment', 'diagnosis', 'diagnosed', 'diagnostics',
'Iran', 'China', 'Korea', 'Italy', 'emergency', 'NHS', 'PHE', 'lockdown', 'UKlockdown',
'social distancing', 'confinement', 'confined']

# add NHS

auth = tweepy.OAuthHandler("wY5tZomH1jUKbFah7ooEuwAeW", "IPHMBer6yiV2og5uaU8pynxuXtfvzlmmWmnbJn6lKtaEChumCp")
auth.set_access_token("1195096510863679494-FBhnMKaYy9qhMS0Z1S8qJwzrfQFh1p", "Dy8oeMKf2eDTb7Q1Oxquo9Gd10HMlPvaQ5dd6rZXVlnBn")
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(StreamListener,self).__init__()
        self.output_file = output_file

    def on_status(self, status):
        #with open(self.output_file, 'a') as tf:
        with open('tweets{}.json'.format(time.strftime("%d%m%y")), 'a') as tf:
            # Write a new line
            tf.write('\n')

            # Write the json data directly to the file
            json.dump(status._json, tf)
            # Alternatively: tf.write(json.dumps(all_data))

        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener(output_file='tweets.json')
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

import time

if __name__ == "__main__":
    while True:
        stream_listener = StreamListener(output_file='tweets{}.json'.format(time.strftime("%y%m%d")))
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        try:
            print("streaming...")
            stream.filter(track = keywords, languages = ['en'])
            # might need to add location: locations parameter
            # can't filter by location and keywords at the same time
            # the output would be for the whole location and all mentions
            # how can I get around this issue?
        except Exception as e:
            print("error. Restarting Stream... Error:")
            time.sleep(60)
