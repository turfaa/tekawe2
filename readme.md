# Tebakata Web Engine v2
This is 1 of 3 applications for Tebakata Line@ bot game. This application handles :
- Line Messaging API Webhook receiver + command converter
- API for one-on-one chat with players
- Front end for API for one-on-one chat with players
Each of those three points builded on one Blueprint.

## Requirements
- Python 3
- Flask

## Installation
- Create a database from `tebakata.sql` if you have not.
- Create a file named `myconfig.py` and complete this with your database and Line@ bot account information.
```python
channel_secret = ''
channel_access_token = ''
host = ''
user = ''
password = ''
database = ''

ACTION_CREATE_GAME = 0
ACTION_START_GAME = 1
ACTION_JOIN_GAME = 2
ACTION_GUESS = 3
```
- Run with `python3 app.py`
