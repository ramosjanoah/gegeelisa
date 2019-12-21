from env import *

from bs4 import BeautifulSoup
beautiful_soup = BeautifulSoup

import redis as redis_lib
redis = redis_lib.Redis(
    host=env['REDIS_HOST'], 
    port=env['REDIS_PORT'], 
    db=0
)

from py2neo import Graph
graph = Graph(
    host=env['NEO4J_HOST'],
    port=env['NEO4J_PORT'],
    user=env['NEO4J_USER'],
    password=env['NEO4J_PASSWORD'],
)
