import sys, os, argparse, time, logging, json, schedule
from selenium import webdriver
from redisService import connection
from Logger.Logger import Logger as logger
import csv
redis = connection()


def save_data():
	logger.LogInfo("Working...")

	# pop out the last data of redis. (like stack in data structure)
	logger.LogInfo("Popping out last pushed data from redis")

	# "REDIS_YOUTUBE_VIDEO_DETAILS" comes from .env 
	details = redis.lpop(os.getenv('REDIS_YOUTUBE_VIDEO_DETAILS'))
	fieldnames = []
	# try:

	print("details::", details)
	if details:

		details = details.decode('ascii')
		
		# convert string to python dictionary
		details = json.loads(details)
		
		
		len_details = details.keys()
		
		# it will put all the header name to fieldnames as list.
		for i in range(len(len_details)):
			fieldnames.append(list(len_details)[i])

		# comma seperated values
		header = ', '.join(fieldnames)
		
		column_value = []
		for i in fieldnames:
			column_value.append('{}'.format(json.dumps(details[i])))
		column_value = ', '.join(column_value)

		csv_file_name = "YoutubeLinkDetails.csv"
		# assigning path of the csv file to save
		file_path = "./csv/{}".format(csv_file_name)
		if(os.path.exists(file_path)):
			# 'a' mode is used to append into the file
			with open(file_path, 'a') as fp: 
				
				fp.writelines("\n{}".format(column_value))
		else:
			# 1) 'w' mode is used to write into the file
			with open(file_path, 'w') as fp: 

				# 2) write header in 1st line
				fp.writelines(header)
				fp.writelines("\n{}".format(column_value))
				
		save_data()
	else:
		logger.LogInfo("process complete done")


save_data()