import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
AMQP_URI = os.getenv("AMQP_URI")
UNIQUE_PREFIX = os.getenv("UNIQUE_PREFIX")
