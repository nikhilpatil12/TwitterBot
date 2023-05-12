import requests
from requests_oauthlib import OAuth1
from constants import consumer_key
from constants import consumer_secret
from constants import access_token
from constants import access_token_secret
from constants import news_apikey
import datetime
import sqlite3
import hashlib
import logging


def random_fact():
    dt = datetime.date.today() - datetime.timedelta(days=1)
    url = "https://newsapi.org/v2/everything?q=technology&language=en&from=" + \
        str(dt)+"&apiKey="+news_apikey
    print(url)
    response = requests.request("GET", url)
    # print(response.json())
    return response.json()['articles']


def format_fact(fact):

    return {"text": "{}".format(fact)}


def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret,
                  acccess_token, access_token_secret)
    return url, auth


def main():
    newshash = ''
    try:
        # Configure logging
        logging.basicConfig(
            filename='/var/log/twitbot.log', level=logging.INFO)

        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('bot.db')
        cursor = sqliteConnection.cursor()
        logging.info('DB Init')

        # check if table exists
        logging.info('Check if POSTED table exists in the database:')
        listOfTables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='POSTED'; ").fetchall()

        if listOfTables == []:
            # create tables
            cursor.execute("CREATE TABLE POSTED(HASH VARCHAR(255));")
            logging.info('POSTED table created')
            # commit changes
            sqliteConnection.commit()
        else:
            logging.info('Table found!')

        newstopost = ''

        fact = random_fact()
        for fct in fact:
            if newstopost == '':
                # print(fct['source']['name'])
                # print(fct['author'])
                logging.info(fct['title'])
                # print(fct['description'])
                # print(fct['url'])
                # print(fct['urlToImage'])

                h = hashlib.new('sha256')
                h.update(fct['title'].encode())
                newshash = h.hexdigest()  # the Hash
                # Write a query and execute it with cursor
                findquery = "SELECT * FROM POSTED WHERE HASH='"+newshash+"';"
                logging.info(findquery)
                cursor.execute(findquery)

                # Fetch and output result
                result = cursor.fetchall()
                logging.info(result)
                if result == []:
                    logging.info('SQLite Result is Empty, Proceed to insert')
                    newstopost = fct['description'] + "\n\n" + \
                        fct['url'] + """ #tech #TechNews"""
                    if len(newstopost) > 280:
                        newstopost = fct['title'] + "\n\n" + \
                            fct['url'] + """ #tech #TechNews"""
                else:
                    logging.info('SQLite Result is: '+str(result))

        # commit changes
        sqliteConnection.commit()
        payload = format_fact(newstopost)
        logging.info(payload)
        url, auth = connect_to_oauth(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        logging.info(url)
        logging.info(str(auth))
        request = requests.post(
            auth=auth, url=url, json=payload, headers={
                "Content-Type": "application/json"}
        )
        logging.info(request.json())

        # Log the response
        logging.info(f'Response status code: {request.status_code}')
        logging.info(f'Response content: {request.content}')
        if (request.status_code >= 200 and request.status_code < 300) or request.status_code == 403:
            insertquery = "INSERT INTO POSTED (HASH) VALUES ('" + \
                newshash + "');"
            cursor.execute(insertquery)
            sqliteConnection.commit()
            logging.info(f'Added hash {newshash} to DB')
            # Close the cursor
            cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        logging.info('SQLite Error')
        logging.info(f'Error occurred -  {error}')

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logging.info('SQLite Connection closed')


if __name__ == "__main__":
    main()
