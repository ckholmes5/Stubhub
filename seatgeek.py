#Creating a new database
#CREATE DATABASE seatgeek;
#use seatgeek;

import MySQLdb
import requests
from datetime import datetime
import time

#Establishing some things
client_id = 'NjA2ODc0NXwxNDc5ODM4NDQ5'
client_secret = 'ijFY1lDupCIuzmdFlt2EiSJiXy3u8q9EoqLaD27J'


#/usr/local/mysql/bin/mysql -u root -p

#Connecting to SQL
while True:

    db = MySQLdb.connect(host = 'localhost',
                        user = 'root',
                        passwd = 'ckh123',
                        db = 'test')
    cur = db.cursor()
    cur.execute('use seatgeek;')

    #cur.execute("CREATE TABLE tickets (SnapshotDate varchar(255), EventName varchar(255), EventDate varchar(255), Venue varchar(255), City varchar(255), quantity varchar(255), avg_price varchar(255), low_price int, high_price varchar(255));");

    add_ticket = ("INSERT INTO tickets "
                "(SnapshotDate, EventName, EventDate, Venue, City, quantity, avg_price, low_price, high_price)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    geo_list = [[40.7128, -74.0059], [39.9526, -75.1652], [42.3601, -71.0589], [41.8781, -87.6298], [36.1699, -115.1398], [37.7749, -122.4194], [34.0522, -118.2437], [25.7617, -80.1918]]
    geo_dict = {40.7128: 'New York City', 39.9526: 'Philadelphia', 42.3601: 'Boston', 41.8781: 'Chicago', 36.1699: 'Las Vegas', 37.7749: 'San Francisco', 34.0522: 'Los Angeles', 25.7617: 'Miami'}

    def get_listings(lat, lon):
        url = 'https://api.seatgeek.com/2/events?lat=' + str(lat) + '&lon=' + str(lon) + '&range=10mi&per_page=5000&client_id=' + client_id + '&client_secret=' + client_secret
        r = requests.get(url)
        SnapshotDate = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        City = geo_dict[lat]

        print r.json()

        for listing in r.json()['events']:
            EventName = listing['title']
            Venue = listing['datetime_local']
            EventDate = listing['venue']['name']
            quantity = listing['stats']['listing_count']
            if quantity == 0 or quantity == None:
                continue
            avg_price = listing['stats']['average_price']
            low_price = listing['stats']['lowest_price']
            high_price = listing['stats']['highest_price']
            new_row = [SnapshotDate, EventName, EventDate, Venue, City, quantity, avg_price, low_price, high_price]
            print new_row
            cur.execute(add_ticket, new_row)

    for geo in geo_list:
        get_listings(geo[0], geo[1])

    db.commit()

    db.close()

    time.sleep(3600 * 24)  # scrape every 24 hours