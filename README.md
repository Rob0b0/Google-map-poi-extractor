# Google POI Extractor

### Yunbo Chen

The program utilize the rectangle bound place search that only exists in Google Map Javascript API in frontend. Then it can be further stored into MongoDB.

I first tried programming solely on html(javascript). Then in order to make it available for persistance, I changed

### Disclaimer
The program is only developed for recreational and study purpose. I developed it to challenge myself and see if I could extract the API data in such strict condition (API only on frontend, API usage limiter from Google). Any commercial use in purpose of profiting is not allowed according to Google.

## Usage:

1. Install Selenium, Flask and chromedriver for Selenium.
2. In `/google_poi` directory, do `python server.py`.
3. In another terminal, do `python selenium_script.py`.

* In case of unknown_error happened in frontend (browser): 
  open console and do `continueSearch()`
with the last printed coordinates on the Selenium terminal (should have 4 paremeters).

* Update your own IP address in stormproxy.com beforehands. 

* Do appreciate and enjoy this sexy scraper.  
<img src='https://media1.tenor.com/images/6a74dd3502497d3bb85b00a054d1480f/tenor.gif?itemid=14873489'/>
