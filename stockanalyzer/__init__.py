# Version of StockAnalyzer package
__version__ = "1.0.0"

from os import path
from configparser import ConfigParser as _ConfigParser

_cfg = _ConfigParser()
_cfg.read(str(path.join(path.dirname(__file__),'config.cfg')))

NewsFeedUrl = _cfg.get("news feed", "url")
TwitterSearchUrl = _cfg.get("twitter api","url")
TickerNames = _cfg["ticker names"]


passwdfile = open('TwitterAuthBearer.txt')
try:
    TwitterAuthBearer = passwdfile.readline()[:-1]
finally:
    passwdfile.close()
