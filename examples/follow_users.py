#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
from random import randint
import time
import getpass

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

    # user_id = '1461295173'
    user_id = api.username_id
    print("Informe o limite para seguir:")
    limit = int(input())
    print("Informe o instagram que deseja pegar os seguidores:")
    ig_follows = input()
    ig_follows = getIdByUsername(api, ig_follows)

    # List of all followers
    myfollowings = getTotalFollowings(api, user_id)
    followers = getTotalFollowers(api, ig_follows)
    followings = getTotalFollowings(api, ig_follows)
    print('Number of followers:', len(followers))
    print('Number of followings:', len(followings))

    lfollowings = []
    for fol in myfollowings:
        lfollowings.append(fol['username'])
    
    count = 0
    folok = 0
    #limit = 400
    for fol in followers:
        interval = randint(0, 15)
        if(fol['username'] not in lfollowings and folok < limit):
            if(count == 60):
                print("Precisamos parar por 5 minutos...")
                time.sleep(60*5)
                count=0
            print("{} - Seguindo {} ... Aguarde {} segundos.".format(folok, fol['username'], 5+interval))
            api.follow(fol['pk'])
            count+=1
            folok+=1
            time.sleep(5+interval)