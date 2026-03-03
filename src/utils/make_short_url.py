import os

from dotenv import load_dotenv

load_dotenv()

SHORT_URL = os.environ.get("SHORT_URL")

def make_short_url(short_name):
    return f'{SHORT_URL}/{short_name}' 