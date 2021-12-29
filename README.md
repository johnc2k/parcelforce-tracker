# Parcelforce Tracker

**About:**

Scrapes the Parcelforce Tracking website every hour for tracking events and sends updates to Telegram.

**Usage:**

`docker run -d --env TRACKING_ID=EV123456789CN --env TG_BOT_TOKEN=12345:foObaRsTr1ng --env TG_CHAT_ID=12345 --name ParcelforceTracker parcelforcetracker:latest`

**Todo:**
* ~~Fix: Make Tracking ID an environmental variable~~
* ~~Fix: Make Telegram secrets an environmental variable~~
* Fix: Array reporting order (multiple messages are sent newest to oldest)
* Fix: Global variables for TG secrets
* Add: Exit on Delivered event?
* Add: Handle multiple Tracking IDs?
* Add: SQLite DB for persistant tracking?
* Add: Royal Mail Tracking?