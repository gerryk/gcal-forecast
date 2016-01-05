 #!/usr/bin/python
 # -*- coding: UTF-8 -*-

from __future__ import print_function

import json
import urllib2
import datetime
import time

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
FORECAST_IO_API_KEY = ""
APPLICATION_NAME = 'Google Calendar Weather Forecast'
TZ = "Europe/Dublin"
LOCATION = "xx.xxxxx,yy.yyyyy"  # lat, long


def get_credentials():   # shamelessly ripped from Google sample code
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-forecast.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    daytime = ["Morning", "Lunchtime", "Evening"]
    timeindex = 0
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = int(time.mktime(time.localtime()))

    data = json.load(urllib2.urlopen("https://api.forecast.io/forecast/"+FORECAST_IO_API_KEY+"/"+LOCATION+","+str(now)))
    for i in [7,12,17]:
        eventtime = datetime.datetime.fromtimestamp(int(data["hourly"]["data"][i]["time"])).strftime('%Y-%m-%dT%H:%M:%S')
        eventdescription = "Weather: " + data["hourly"]["data"][i]["summary"] + "\n" + \
                           "Pressure: " + str(data["hourly"]["data"][i]["pressure"]) + "mbar\n" + \
                           "Windspeed: " + str(data["hourly"]["data"][i]["windSpeed"]) + "m/s\n" + \
                           "Temperature: " + str(data["hourly"]["data"][i]["temperature"]) + "dF"
                           # TODO - fix degrees symbol
                           #"Temperature: " + str(data["hourly"]["data"][i]["temperature"]) + "°F"
        event = {
          'summary': 'Weather Notification (' + daytime[timeindex] + '):'  + data["hourly"]["data"][i]["summary"],
          'description': eventdescription,
          'start': {
            'dateTime': eventtime,
            'timeZone': TZ,

          },
          'end': {
            'dateTime': eventtime,
            'timeZone': TZ,

          }
        }
        timeindex = timeindex + 1
        print (json.dumps(event, sort_keys=True, indent=4, separators=(',', ': ')))
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()


