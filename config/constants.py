import os
from dotenv import load_dotenv

load_dotenv()

# Database configurations
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')


DEFUALT_OFFSET = 0
DEFUALT_LIMIT = 20

