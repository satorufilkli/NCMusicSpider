import os
from dotenv import load_dotenv

load_dotenv()

PLAYLIST_API = os.getenv('PLAYLIST_API',"")
DOWNLOAD_API = os.getenv('DOWNLOAD_API',"")
COOKIE = os.getenv('NETEASE_COOKIE',"")

HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': os.getenv('USER_AGENT'),
    'Cookie':COOKIE
}
