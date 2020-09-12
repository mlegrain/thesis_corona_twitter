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

In order to create this database and conduct my data collection, I used Python.

Onto the code… Don’t worry, I commented my code thoroughly to make sure each step is clear to you!

First, I created a database to store the collected data. 

Here’s the code I wrote:

```{python}
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












You can use the [editor on GitHub](https://github.com/mlegrain/thesis_corona_twitter/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/mlegrain/thesis_corona_twitter/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
