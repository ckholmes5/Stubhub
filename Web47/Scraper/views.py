from django.shortcuts import render

# Create your views here.
#cd /usr/local/mysql/bin/
#sudo ./mysql -u root -h localhost -p
#passwords = ckh123

#Creating a new database
#CREATE DATABASE stubhub;
#use stubhub;

import requests
import pprint
import pandas as pd
from datetime import datetime
import re
import time
from settings import (basic_authorization_token, stubhub_username,
                      stubhub_password)


from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response





def index(request):
    date = datetime.now()
    return render(request, 'scraper/index.html', {'date': date})



def scrape(request):
    ## POST parameters for API call
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + basic_authorization_token}
    body = {
        'grant_type': 'password',
        'username': stubhub_username,
        'password': stubhub_password,
        'scope': 'PRODUCTION'}
    ## Making the call
    url = 'https://api.stubhub.com/login'
    r = requests.post(url, headers=headers, data=body)

    token_respoonse = r.json()
    print token_respoonse
    access_token = token_respoonse['access_token']
    user_GUID = r.headers['X-StubHub-User-GUID']
    '''

    #/usr/local/mysql/bin/mysql -u root -p
    #Connecting to SQL
    while True:

        db = MySQLdb.connect(host = 'localhost',
                            user = 'root',
                            passwd = 'ckh123',
                            db = 'test')
        cur = db.cursor()
        cur.execute('use stubhub;')

        #cur.execute("CREATE TABLE tickets (SnapshotDate varchar(255), EventName varchar(255), EventDate varchar(255), Venue varchar(255), sectionName varchar(255),row varchar(255),seatNumbers varchar(255),quantity int,deliveryType varchar(255),amount varchar(255));")

        add_ticket = ("INSERT INTO tickets "
                    "(SnapshotDate, EventName , EventDate , Venue ,sectionName ,row,seatNumbers,quantity,deliveryType,amount)"
                    "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)")

        def get_listing(listing_id):
            #### Step 1 - Searching inventory for an event ####
            inventory_url = 'https://api.stubhub.com/search/inventory/v1?eventid=' + str(listing_id) + '&rows=100000'
            headers['Authorization'] = 'Bearer ' + access_token
            headers['Accept'] = 'application/json'
            headers['Accept-Encoding'] = 'application/json'
            print access_token

            inventory = requests.get(inventory_url, headers=headers)
            inv = inventory.json()
            listing = inv['listing']

            ## Flattening some nested dictionary for ticket price
            for t in listing:
                for k,v in t.items():
                    if k == 'currentPrice':
                        t['amount'] = v['amount']
            ## Converting to Pandas dataframe and exporting to CSV
            listing_df = pd.DataFrame(listing)
            listing_df.to_csv(open('export.csv', 'wb'))

            #### Step 2 - Adding Event and Venue Info ####

            ## Calling the eventsearch api
            info_url = 'https://api.stubhub.com/catalog/events/v2/' + str(listing_id)
            info = requests.get(info_url, headers=headers)

            pprint.pprint(info.json())

            info_dict = info.json()

            full_title = info_dict['title'].split('[', 2)
            event_name = full_title[0].strip()
            event_date = re.search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(full_title)).group()


            venue = info_dict['venue']['name']
            snapshotdate = datetime.datetime.today().strftime('%m/%d/%Y')

            my_col = ['SnapshotDate','EventName','EventDate', 'Venue', 'sectionName', 'row',
                      'seatNumbers', 'quantity', 'deliveryTypeList', 'amount']
            listing_df['SnapshotDate'] = snapshotdate
            listing_df['EventName'] = event_name
            listing_df['EventDate'] = event_date
            listing_df['Venue'] = venue
            final_df = listing_df[my_col]

            return final_df

        listings = [9697937,9694467,9679383,9679081,9664596,9566637,9510281]
        listings_url = 'https://api.stubhub.com/search/catalog/events/v2?point=40.2,-83.1&radius=120'
        headers['Authorization'] = 'Bearer ' + access_token
        headers['Accept'] = 'application/json'
        headers['Accept-Encoding'] = 'application/json'

        #listing = requests.get(listings_url, headers = headers)


        for listing in listings:
            df = get_listing(listing)
            print listing
            for row in df.iterrows():
                new_row = []
                for item in row[1]:
                    new_row.append(str(item))
                cur.execute(add_ticket, new_row)


        #cur.execute(add_ticket, ('10/19/16', 'Twenty One Pilots Providence Tickets - Twenty One Pilots', '01/17/2017', 'Dunkin Donuts Center Tickets on StubHub!', 'Upper 227', 'R', '14', '1', '[1]', '117.5'))

        db.commit()

        db.close()

        time.sleep(3600 * 24)  # scrape every 24 hours
    '''

    return Response(token_respoonse)
