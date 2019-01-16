from os import listdir
from os.path import isfile, join
import json
import pandas as pd
import time

start_time = time.time()
run_number = 1
files_per_run = 10


range_high = run_number * files_per_run
range_low = range_high - files_per_run

print(range_high)
print(range_low)


#input twitter data
my_path = '/Volumes/backup/dutch_data/sort_users_dutch'  
##create file to save data
outfile = '/Volumes/backup/dutch_data/engagement_stat/' ## CHANGE ME


files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
#load tweets in flie
all_tweets = []

print("Reading in files!")

json_errors = 0

##########
for file_no in range(range_low, range_high):
	if file_no >= len(files):
		break
	file = files[file_no]
	if (file_no % 1) == 0:
		print("Starting file #" + str(file_no) + ": " + file)
		print("Added " + str(len(all_tweets)) + " tweets")
	full_name = my_path + '/' + file
	if file != ".DS_Store":
		try:
			with open(full_name, 'r') as file:
				data = json.load(file)
				all_tweets.extend(data)
		except:
			print('error:' )
			json_errors += 1
			continue

############

##filter into 4 categories
## 1: check mark not zp related
## 2: check mark and zp related
## 3: no check mark not zp related
## 4: no check mark zp related


def is_verified(tweet):


def is_zpiet_related(tweet):
	text = tweet['text']	

