from dotenv import load_dotenv
load_dotenv()

from .database import redis_client
if redis_client.ping():
    print("Redis instance is running")
