# gcal-forecast
Script to post weather forecasts from forecast.io to GCal
Currently this runs on Linux. It was developed on Ubuntu 14.04 and runs on Python 2.7.6. It may work on other versions and distributions, but I haven't verified any.

Requires API access to forecast.io and Google Calendar

Sign up for forecast.io API here - https://developer.forecast.io/
The API key should be added to post_forecast.py CONSTANTS section

Sign up for Google Calendar API here - https://developers.google.com/apps-script/advanced/calendar
The Oauth ket should be stored in the same directory as post_forecast.py as client_secret.json

LOCATION and TZ should be completed in the CONSTANTS section. LOCATION is a string containing the Latitude & Longitude of the location you wish to forecast for. This string is in the form "XX.XXXXX,YY.YYYYYY" where XX.XXXXX is Latitude in decimal format, and YY.YYYYY is Longitude in decimal format. TZ is a Timezone specification as per tzdata - https://en.wikipedia.org/wiki/Tz_database

When first run, Google will initiate an Oauth authentication session. This requires a browser to accept the authentication request, so the first run should take place on a computer with a browser which has access to Google services.

Once run, the credentiaials will be stored in ~/.credentials/calendar-forecast.json
If you wish to run this on some other computer, the credential file will need to be relocated to the same location on the new machine.
