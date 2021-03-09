import sys, os, argparse, time, logging, json, re
from redisService import connection
from Logger.Logger import Logger as logger
# logger = logging.getLogger()
parser = argparse.ArgumentParser(description='Paste your youtube url')
parser.add_argument('link', type=str, help='Youtube URL')
args = parser.parse_args()


def validating(link):
	youtube_url = "https://www.youtube.com/watch?v="

	flag = False
	if link.startswith(youtube_url):
		flag = True

	return flag


link = args.link
isValid = True
isValid = validating(args.link)

if isValid:

	try:		
		
		# starting connection to redis
		redis = connection()
		
		# to push into redis db
		redis.lpush(os.getenv('REDIS_YOUTUBE_VIDEO_LIST'), link)
		logger.LogInfo("youtube link queued")
	except Exception as e:
		logger.LogError("error: {}".format(str(e)))
else:
	logger.LogError("Link is not valid")
