import sys, os, argparse, time, logging, json, schedule
from selenium import webdriver
from redisService import connection
from Logger.Logger import Logger as logger

redis = connection()
# def mapping():
# 	youtube_feature_extraction_map = {
# 		'video_title': '//*[@id="container"]/h1/yt-formatted-string',
# 		'hash_tags': '//*[@id="container"]/yt-formatted-string',
# 		'views': '//*[@id="count"]/yt-view-count-renderer/span[1]',
# 		'upload_date': '//*[@id="date"]/yt-formatted-string',
# 		'channel_name': '//*[@id="text"]/a',
# 		'description': "",
# 		'duration': 0.0
# 	}

def extract_data(youtube_link):
	details = {}
	try:

		driver = webdriver.Chrome()
		driver.get(youtube_link)
		time.sleep(3)
		details = {
			"link": youtube_link,
			'video_title': "",
			'hash_tags': "",
			'views': 0,
			'upload_date': None,
			'channel_name': "",
			'description': "",
			'duration': 0.0
		}
		# sleep is used to take time to reload the page
		response = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
		logger.LogInfo("Title extracted: {}".format(response))
		if(response):
			details["video_title"]=response

		response = driver.find_element_by_xpath('//*[@id="container"]/yt-formatted-string').text
		logger.LogInfo("Hah tags extracted")
		if(response):
			details["hash_tags"]=response

		response = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
		logger.LogInfo("Views extracted")
		if(response):
			details["views"]=response

		response = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text
		logger.LogInfo("Upload date extracted")
		if(response):
			details["upload_date"]=response

		response = driver.find_element_by_xpath('//*[@id="text"]/a').text
		logger.LogInfo("Channel name extracted")
		if(response):
			details["channel_name"]=response

		time.sleep(3)

		response = driver.find_element_by_css_selector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div.ytp-time-display.notranslate > span.ytp-time-duration').text
		logger.LogInfo("Duration extracted")
		if(response):
			details["duration"]=response

		driver.find_element_by_xpath('//*[@id="more"]/yt-formatted-string').click()
		logger.LogInfo("Description extended")
		time.sleep(4)

		response = driver.find_element_by_xpath('//*[@id="description"]').text
		logger.LogInfo("Description extracted")
		if(response):
			details["description"]=response

		print(details)
		logger.LogInfo('Succesfully extracted')
		
		redis.lpush(os.getenv('REDIS_YOUTUBE_VIDEO_DETAILS'), json.dumps(details))
		logger.LogInfo('Details saved Succesfully in Redis')
	
	except Exception as e:
		logger.LogError('Something Not good with URL')
		details = {}



def job():
    logger.LogInfo("Working...")
    youtube_link = redis.lpop(os.getenv('REDIS_YOUTUBE_VIDEO_LIST'))
    if(youtube_link):
    	youtube_link = youtube_link.decode('ascii')
    	print("youtube_data: ", youtube_link)
    	extract_data(youtube_link)
    logger.LogInfo("Job Done")
# job()
schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)