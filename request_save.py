import sys, os, argparse, time, logging, json, schedule
from selenium import webdriver
from redisService import connection
from Logger.Logger import Logger as logger
import csv
redis = connection()


def save_data():
	logger.LogInfo("Working...")
	# details = redis.lpop(os.getenv('REDIS_YOUTUBE_VIDEO_DETAILS'))
	details = redis.lpop(os.getenv('REDIS_YOUTUBE_VIDEO_DETAILS'))
	fieldnames = []
	# try:

	print("details::", details)
	if details:

		details = details.decode('ascii')
		details = json.loads(details)
		
		# print("loads:", details)
		
		len_details = details.keys()
		# print(len_details)

		for i in range(len(len_details)):
			fieldnames.append(list(len_details)[i])

		header = ', '.join(fieldnames)
		# print(header)
		column_value = []
		for i in fieldnames:
			column_value.append('{}'.format(json.dumps(details[i])))
		column_value = ', '.join(column_value)

		csv_file_name = "YoutubeLinkDetails.csv"
		file_path = "./csv/{}".format(csv_file_name)
		if(os.path.exists(file_path)):
			# append wala logic likhna h 
			with open(file_path, 'a') as fp: 
				# 2) header 1st line m likhna h 
				# fp.writelines(header)
				fp.writelines("\n{}".format(column_value))
		else:
			# 1) new file create karna h 
			with open(file_path, 'w') as fp: 
				# 2) header 1st line m likhna h 
				fp.writelines(header)
				fp.writelines("\n{}".format(column_value))
				# 3) header k against m value dalna h
		save_data()
	else:
		logger.LogInfo("process complete done")


save_data()


