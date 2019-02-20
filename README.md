# tokenCollector

Collect Twitter API-tokens from invited users for research purposes and export them in a user-friendly way.

## Installation

`git clone https://github.com/Kudusch/tokenCollector.git`

`cd tokenCollector`

`virtualenv -p python3 flaskServer/venv`

`source flaskServer/venv/bin/activate`

`pip3 install -r requirements.txt`

Edit [example_config.py](flaskServer/example_config.py) and rename to config.py.

`FLASK_APP=flaskServer FLASK_ENV=development python -m flask init-db`

You can now run the build-in development server with this command:

`FLASK_APP=flaskServer FLASK_ENV=development python -m flask run`

## Deployment

You can use this app locally with the build-in development server:

`FLASK_APP=flaskServer FLASK_ENV=development python -m flask run`

You can also deploy it with Apache, mod_wsgi and virtual hosts (see [this tutorial](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/) and the example configurations in [000-example.conf](000-example.conf)  and [example_flaskServer.wsgi](example_flaskServer.wsgi).

## Configuration

In order to use Twitters OAuth features, you have to [register an application](https://developer.twitter.com/en/apps). The Callback URL of your app should be set to `domain.tld/oauth-authorized` when deployed and `http://127.0.0.1:5000/oauth-authorized` when still in development.

## License

This software is released under MIT License (MIT).