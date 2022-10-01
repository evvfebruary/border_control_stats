import os
from dotenv import load_dotenv

load_dotenv('database/.env')

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_PORT = os.getenv('PG_PORT')
PG_HOST = os.getenv('PG_HOST')

# Tables
REPORTS_TABLE_NAME = 'reports'
HASHTAGS_STATS_TABLE_NAME = 'hashtag_stats'
PEOPLES_TABLE_NAME = 'peoples'

