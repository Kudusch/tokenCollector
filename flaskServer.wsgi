#!/usr/bin/python

import sys
import logging
import imp

logging.basicConfig(stream=sys.stderr)
# Edit path to tokenCollector
sys.path.insert(0,"/path/to/tokenCollector/")
# Edit path to virtual env
activate_this = 'tokenCollector/flaskServer/venv/bin/activate_this.py'
exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))

from flaskServer import app as application
