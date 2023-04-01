import requests
from requests_oauthlib import OAuth1
import constants
from datetime import date
import sqlite3
import hashlib


def random_fact():
    url = "https://newsapi.org/v2/everything?q=technology&language=en&from=" + \
        str(date.today())+"&apiKey="+news_apikey

    # querystring = {"category": "Technology",
    #                "safeSearch": "Off", "textFormat": "Raw"}

    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Key": "9589337a3fmsh25dc89ca639303fp1a2db7jsna257f4506309",
        "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers)

    return response.json()['articles']


def format_fact(fact):

    return {"text": "{}".format(fact)}


def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret,
                  acccess_token, access_token_secret)
    return url, auth


def main():
    try:
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('bot.db')
        cursor = sqliteConnection.cursor()
        print('DB Init')

        # check if table exists
        print('Check if POSTED table exists in the database:')
        listOfTables = cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
        AND name='POSTED'; """).fetchall()

        if listOfTables == []:
            # create tables
            cursor.execute(
                """CREATE TABLE POSTED(HASH VARCHAR(255));""")
            print('POSTED table created')
            # commit changes
            sqliteConnection.commit()
        else:
            print('Table found!')

        newstopost = ''

        fact = random_fact()
        for fct in fact:
            if newstopost == '':
                # print(fct['source']['name'])
                # print(fct['author'])
                print(fct['title'])
                # print(fct['description'])
                # print(fct['url'])
                # print(fct['urlToImage'])

                h = hashlib.new('sha256')
                h.update(fct['title'].encode())
                newshash = h.hexdigest()  # the Hash
                # Write a query and execute it with cursor
                findquery = """SELECT * FROM POSTED WHERE HASH='"""+newshash+"""';"""
                cursor.execute(findquery)

                # Fetch and output result
                result = cursor.fetchall()
                if result == []:
                    print('SQLite Result is Empty, Proceed to insert')
                    newstopost = fct['title'] + "\n\n" + \
                        fct['description'] + fct['url']
                else:
                    print('SQLite Result is: '+str(result))

        # commit changes
        sqliteConnection.commit()
        payload = format_fact(newstopost)
        print(payload)
        url, auth = connect_to_oauth(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        request = requests.post(
            auth=auth, url=url, json=payload, headers={
                "Content-Type": "application/json"}
        )
        print(request)
        insertquery = """INSERT INTO POSTED (HASH) VALUES ('""" + \
            newshash+"""');"""
        cursor.execute(insertquery)

        sqliteConnection.commit()
        # Close the cursor
        cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')


if __name__ == "__main__":
    main()
