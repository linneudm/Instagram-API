#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import time
from datetime import datetime

API = InstagramAPI("username", "password")
API.login()

def getIdByUsername(targetname):
    API.searchUsername(targetname)
    return API.LastJson['user']['pk']

#Get date (local) comments from all pictures

user = getIdByUsername("username_profile")
auth = API.getUserFeed(user)
if(auth):
	feed = API.LastJson
	if(len(feed['items'])>0):
		for f in (feed['items']):
			caption = f['caption']['text']
			print('Caption:', caption)
			media_id = str(f['caption']['media_id'])
			res = API.getMediaComments(media_id)
			res2 = API.LastJson['comments']
			if res2 != []:
				for c in res2:
					##print(c['created_at_utc'])
					#Convert int to date
					date = datetime.fromtimestamp(c['created_at_utc'])
					user_comment = c['user']['username']
					print('Comment by:', user_comment)
					print('Date comment:', date)
					time.sleep(2)
			else:
				print('No comments here.')
				time.sleep(2)
	else:
		print('Nothing found.')
else:
	print('Maybe this is a private profile.')