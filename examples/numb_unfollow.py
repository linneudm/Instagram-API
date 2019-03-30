#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
from random import randint
from datetime import datetime
import time
import getpass
from time import gmtime, strftime

def getIdByUsername(API, targetname):
    API.searchUsername(targetname)
    return API.LastJson['user']['pk']

def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowings(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


if __name__ == "__main__":
    print("Informe o nome de usuario:")
    username = input()
    passw = getpass.getpass("Informe a senha:")
    api = InstagramAPI(username, passw)
    api.login()

    print("Informe o Instagram que deseja calcular:")
    ig = input()

    # user_id = '1461295173'
    user_id = getIdByUsername(api, ig)

    # List of all followers
    followers = getTotalFollowers(api, user_id)
    followings = getTotalFollowings(api, user_id)

    id_fls = []
    id_fgs = []
    non_fol = []
    for fol in followers:
        id_fls.append((fol['pk'], fol['username']))
    for fol in followings:
        id_fgs.append((fol['pk'], fol['username']))
    count = 0

    for fol in id_fgs:
        if(fol not in id_fls):
            non_fol.append((fol[0], fol[1]))
    
    result = ""

    for i, item in enumerate(non_fol):
    	#print("{} - {}.".format(i, item[1]))
    	result += "{} - {}.".format(i, item[1]) + "\n"
	
    now = datetime.now()
    title = "Dados de {}".format(ig)
    timecap = ("{}/{}/{} {}:{}:{}".format(now.day, now.month, now.year, now.hour, now.minute, now.second))

    count = '\n\n' + 'Seguidores: {}'.format(len(followers)) + '\n' + 'Seguindo: {}'.format(len(followings)) + '\n' + 'Não correspondentes: {}'.format(len(non_fol))
    with open('non-followers.txt', 'a') as f:
    	f.write(title + '\n' + result + count + '\n' + "Hora da captura: " + timecap)
    #print('Seguidores:', len(followers))
    #print('Seguindo:', len(followings))
    #print('Não correspondentes:', (len(non_fol)))

'''
for fol in id_fgs:
	if(fol[0] not in id_fls[0]):
		#interval = randint(0, 15)
		name = fol[1]
		print(name)
'''