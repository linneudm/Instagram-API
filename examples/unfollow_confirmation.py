#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
from random import randint
import time
import getpass


def getIdByUsername(targetname):
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

    # user_id = '1461295173'
    user_id = api.username_id

    # List of all followers
    followers = getTotalFollowers(api, user_id)
    followings = getTotalFollowings(api, user_id)
    print('Number of followers:', len(followers))
    print('Number of followings:', len(followings))

    id_fls = []
    id_fgs = []
    for fol in followers:
        id_fls.append((fol['pk'], fol['username']))
    for fol in followings:
        id_fgs.append((fol['pk'], fol['username']))

    for fol in id_fgs:
        if(fol not in id_fls):
            interval = randint(0, 15)
            print("Deseja deixar de seguir {} ? 1 - Sim, 2 - Não.".format(fol[1]))
            confirmation = int(input())
            if(confirmation == 1):
                print("Deixando de seguir {} ... Aguarde {} segundos.".format(fol[0], 5+interval))
                api.unfollow(fol[0])
                time.sleep(5+interval)

'''
for fol in id_fgs:
	if(fol[0] not in id_fls[0]):
		#interval = randint(0, 15)
		name = fol[1]
		print(name)
'''