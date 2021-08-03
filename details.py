from igramscraper.instagram import Instagram
# from lolwa import get_followers
# from lolwa import login
from time import sleep
import os
from os import path
import datetime
import ast
import sys
from pytz import timezone
from twilio.rest import Client

# Get the following from your twilio account
account_sid = ""
auth_token = ""

client = Client(account_sid, auth_token)

FOLLOWER_LIMIT = 10**6

#Your instagram bot account username
insta_username = ''

#Your instagram bot account password
insta_password = ''

#Username of the real instagram account which you want to monitor
username = 'epic.valo.fails'

#Change this at your own risk, it is advised to keep anything above 30
MINS_TO_SLEEP = 1


def check_unfollowers(current,old):
	return list(set(old) - set(current))

def check_followers(current,old):
	return list(set(current) - set(old))

def send_message(followers, unfollowers):
	print("sending message")
	body = "New Followers: " +str(followers) +"\n Unfollowers: "+str(unfollowers)
	client.messages.create(from_="+18302436279", to="+91 95949 58505", 
	body=body)
	print('message sent')

def start():
	while True:
		try:
			print("iter")
			instagram = Instagram()
			instagram.with_credentials(insta_username, insta_password)
			instagram.login(force=False,two_step_verificator=True)
			sleep(2) # Delay to mimic user

			followers = []
			account = instagram.get_account(username)
			sleep(1)
			curr_time = datetime.datetime.now(timezone('Asia/Kolkata'))
			curr_time = curr_time.strftime("%b %d, %Y - %H:%M:%S")
			followers = instagram.get_followers(account.identifier, FOLLOWER_LIMIT, 100, delayed=True) # Get 150 followers of 'kaalu', 100 a time with random delay between requests
			# print(followers)

			current_followers = []

			for follower in followers['accounts']:
				current_followers.append(follower.username)

			if not path.exists("follower_list.txt"):
				f = open("follower_list.txt","w")
				f.write(str(current_followers))
				f.close()
			else:
				f = open("follower_list.txt","r+")
				old_followers = f.read()
				f.close()
				old_followers = ast.literal_eval(old_followers)

				unfollowers = check_unfollowers(current_followers,old_followers)
				followers = check_followers(current_followers,old_followers)

				follower_change  = len(current_followers)-len(old_followers)

				follow_count = len(followers)
				unfollow_count = len(unfollowers)

				if (follow_count > 0 or unfollow_count > 0):
					send_message(followers, unfollowers)
				f = open("follower_list.txt","w")
				f.write(str(current_followers))
				f.close()
				

			

		except KeyboardInterrupt:
			print("Exiting...")
			sys.exit(0)
		except Exception as e:
			print(e)

		sleep(MINS_TO_SLEEP*60)


if __name__ == '__main__':
	start()
