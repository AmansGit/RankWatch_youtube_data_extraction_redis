import redis, os
from dotenv import load_dotenv
load_dotenv()

def connection():
	host = os.getenv('REDIS_HOST')
	port = os.getenv('REDIS_PORT')
	return redis.Redis(host=host, port=port)
