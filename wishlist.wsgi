#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.append('/var/www/wishlist/')
sys.path.append('/var/www/wishlist/wishlist/')
sys.path.append('/var/www/wishlist/wishlist/venv/lib/python3.6/site-packages')
from wishlist import app as application
