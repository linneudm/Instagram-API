#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password



from InstagramAPI import InstagramAPI
from random import randint
import time
import getpass
import os

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
    #print("Informe o limite de comentarios:")
    #maxcomment = int(input())
    maxcomment = 20
    print("Informe o nome do instagram que deseja pegar os seguidores:")
    user_f = str(input())
    user_id = getIdByUsername(api, user_f)

    print("Informe o nome do instagram que deseja comentar a foto:")
    ig_comment = str(input())
    ig_id = getIdByUsername(api, ig_comment)
    result = api.getUserFeed(ig_id)
    if(result):
        feed = api.LastJson
    else:
        print("nao deu certo.")
    print("Selecione a foto do sorteio com base na legenda.")
    select = 0
    for f in (feed['items']):
        if select != 1:
            try:
                caption = f['caption']['text']
            except:
                caption = "Sem legenda."
            print('Legenda:', caption)
            print("É esta a foto do sorteio? 1 - Sim, 2 - Não.")
            select = int(input())
            if(select == 1):
                print("OK! Foto encontrada...")
                media_id = str(f['caption']['media_id'])
                with open('test.txt', 'a') as f:
                    f.write(str(media_id)+'\n')
        else:
            break
