# Twitter Bot
##### This project is a Twitter bot that posts random technology news articles to a Twitter account. The bot uses the News API to get the news articles, and it stores the articles it has already posted in a SQLite database to avoid duplicates.

## Requirements
- `Python 3.6 or higher`
- `Docker`
- ---
### Getting Started
1. Clone the repository and navigate to the project directory
2. Create a new file `constants.py` in the project directory and add the following variables with their respective API keys:
```python
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
news_apikey = 'YOUR_NEWSAPI_ORG_API_KEY'
```
3. Build the Docker image using the provided Dockerfile:
`docker build -t twitbot .`
4. Run the Docker container with the following command:
`docker run -d --name twitbot twitbot`
This will start the cron job inside the container, which will run the `twitbot.py` script twice every hour.
---
### Code Explanation
The `twitbot.py` script performs the following steps:
1. Imports the necessary modules and API keys from `constants.py`
2. Defines a function random_fact() that gets a random technology news article from the News API using the requests module.
3. Defines a function format_fact() that formats the news article as a dictionary that can be used as the payload for the Twitter API.
4. Defines a function connect_to_oauth() that sets up the OAuth authentication for the Twitter API using the requests_oauthlib module.
5. Defines the main() function that:
6. Creates a connection to the SQLite database and checks if the POSTED table exists.
7. Gets a random news article and checks if it has already been posted by hashing the article title and checking if the hash is in the POSTED table.
8. If the article has not been posted, it formats the article and posts it to Twitter using the Twitter API.
9. Inserts the hash of the posted article into the POSTED table to avoid duplicates.
10. Finally, the script calls the main() function if the script is run as the main program.
11. The Dockerfile sets up a Ubuntu environment with the necessary dependencies and sets up a cron job to run the `twitbot.py` script *twice* every hour. The cronjob file specifies the cron job schedule.
---
### Contributing
Feel free to contribute to the project by submitting issues or pull requests. Follow the standard GitHub workflow for contributions.
---
### License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as per the license terms.
---
### Tools Used
##### The following tools were used in this project:
1. Python - A programming language used to write the script.
2. Requests - A Python library used for making HTTP requests to the News API.
3. Requests-OAuthlib - A Python library used for OAuth authentication with the Twitter API.
4. SQLite3 - A database management system used to store the hashed titles of already posted news articles.
5. Hashlib - A Python library used for hashing the title of the news article.
6. Docker - A platform used to create a container for running the script.
7. Cron - A job scheduler used to run the script at a specified time every day.
---
##### References
- Python documentation: https://docs.python.org/3/
- Requests documentation: https://docs.python-requests.org/en/latest/
- Requests-OAuthlib documentation: https://requests-oauthlib.readthedocs.io/en/latest/
- SQLite documentation: https://www.sqlite.org/docs.html
- Hashlib documentation: https://docs.python.org/3/library/hashlib.html
- Docker documentation: https://docs.docker.com/
- Cron documentation: https://manpages.debian.org/stretch/cron/cron.8.en.html
