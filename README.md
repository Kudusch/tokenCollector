# tokenCollector

Collect Twitter API-tokens from invited users for research purposes and export them in a user-friendly way.

## Installation

`git clone https://github.com/Kudusch/tokenCollector.git`

`cd tokenCollector`

`virtualenv -p python3 flaskServer/venv`

`source flaskServer/venv/bin/activate`

`pip3 install -r requirements.txt`

Edit [example_config.py](flaskServer/example_config.py) and rename to *config.py*.

`FLASK_APP=flaskServer FLASK_ENV=development python -m flask init-db`

Make sure you have the correct permissions to read and write from the virtualenv and the instance directory.

## Development and Local Tests

You can use this app locally with the build-in development server:

`FLASK_APP=flaskServer FLASK_ENV=development python -m flask run`

## Deployment

You can deploy the app with Apache, mod_wsgi and virtual hosts.

`apt-get install libapache2-mod-wsgi-py3`

Edit [example_flaskServer.wsgi](example_flaskServer.wsgi) and rename to *flaskServer.wsgi* and move, edit and enable [000-example.conf](000-example.conf) to */etc/apache2/sites-available*.

## Configuration

In order to use Twitters OAuth features, you have to [register an application](https://developer.twitter.com/en/apps). The Callback URL of your app should be set to `domain.tld/oauth-authorized` when deployed and `http://127.0.0.1:5000/oauth-authorized` when still in development.

## Helper Scrips

- [token_generator.R](token_generator.R) can be used to create [rtweet](https://github.com/mkearney/rtweet/) compatible token-objects.
- [check_tokens.py](check_tokens.py) and its function `gen_api_list()` can be used with [Tweepy](https://github.com/tweepy/tweepy/) to generate a list of API-objects to use in multi-token scripts.

## License

This software is released under MIT License (MIT).
