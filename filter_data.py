from os import listdir
from os.path import isfile, join
import json
import pandas as pd
import time

start_time = time.time()
run_number = 1
files_per_run = 10000


range_high = run_number * files_per_run
range_low = range_high - files_per_run

print(range_high)
print(range_low)


#input twitter data
my_path = '/Volumes/backup/aws_data/z_piet'  
##create file to save data
outfile = '/Volumes/backup/aws_data/z_piet_filter/' ## CHANGE ME


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
print("How many tweets: " + str(len(all_tweets)))


zpiet_text_list = ['zwarte piet', 'black piet', 'zwartepiet', 'zwartepieten' , '#zwartepiet', '#zwartepieten', '#blackpiet']
zpiet_hashtag_list = ['#zwartepiet', '#zwartepieten', '#blackpiet', 'zwartepiet', 'zwartepieten', 'blackpiet']
zwarte_text = ['zwarte', 'black']
piet_text = ['piet', 'pieten']
verified_no_piet = []
verified_piet = []
activist_no_piet = []
activist_piet = []


def is_verified(tweet):
	verified = tweet['user']['verified']
	if verified == True:
		return True
	else:
		return False


def is_retweet(tweet):
	if 'retweeted_status' in tweet.keys():
		return True
	else:
		return False


def get_text(tweet):
	try:
		text = tweet['retweeted_status']['extended_tweet']['full_text'].lower()
	except:
		try:
			text = tweet['retweeted_status']['quoted_status']['extended_tweet']['full_text'].lower()	
		except:
			try: 
				text = tweet['quoted_status']['text'].lower()
			except:
				text = tweet['text'].lower()

	return text	

	# if is_retweet(tweet):


	# text = tweet['text'].lower()
	# hashtag = get_hashtag(tweet)

def is_zpiet_related(text):
	if ('zwarte' and 'piet') in text:
		return True
	elif ('black' and 'piet') in text:
		return True
	for word in text:
		if word in zpiet_text_list:
			return True
	


for tweet in all_tweets:
	text = get_text(tweet)

	if is_verified(tweet):
		if is_zpiet_related(text):
			verified_piet.append(tweet)
		else:
			verified_no_piet.append(tweet)
	elif is_zpiet_related(text):
		activist_piet.append(tweet)
	else:
		activist_no_piet.append(tweet)



print("total verified no piet: " + str(len(verified_no_piet)))
print("total verified piet: " + str(len(verified_piet)))
print("total activist no piet: " + str(len(activist_no_piet)))
print("total activist piet: " + str(len(activist_piet)))


with open(outfile + 'verified_no_piet' + str(run_number) + '.json', 'w') as f:
	json.dump(verified_no_piet, f)

with open(outfile + 'verified_piet' + str(run_number) + '.json', 'w') as f:
	json.dump(verified_piet, f)

with open(outfile + 'activist_no_piet' + str(run_number) + '.json', 'w') as f:
	json.dump(activist_no_piet, f)

with open(outfile + 'activist_piet' + str(run_number) + '.json', 'w') as f:
	json.dump(activist_piet, f)





print('done')





