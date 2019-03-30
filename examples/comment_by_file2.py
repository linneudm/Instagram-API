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
    ok = True
    times = 0
    user_swap = 0

    if times == 0:
        print("Informe o nome de usuario 1:")
        username1 = input()
        passw1 = getpass.getpass("Informe a senha:")

        print("Informe o nome de usuario 2:")
        username2 = input()
        passw2 = getpass.getpass("Informe a senha:")

    while(ok):
        if(times != 0):
            time.sleep(60*3)
        if(user_swap == 0):
            username = username1
            passw = passw1
            user_swap = 1
        else:
            username = username2
            passw = passw2
            user_swap = 0

        api = InstagramAPI(username, passw)
        api.login()

        # user_id = '1461295173'
        #print("Informe o limite de comentarios:")
        #maxcomment = int(input())
        maxcomment = 20

        user_f = username
        user_id = getIdByUsername(api, user_f)

        if times == 0:
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
                        res = api.getMediaComments(media_id)
                else:
                    break
                    
        ig_id = getIdByUsername(api, ig_comment)
        result = api.getUserFeed(ig_id)
        if(result):
            feed = api.LastJson
        else:
            print("nao deu certo.")

        print("Quantos usuarios por comentário?")
        usr_qtd = int(input())
        #maxcomment = 20
        partial = 0
        count = 0
        times += 1
        text = ""
        print("Agora, vamos comentar com os segudires de {}.".format(user_f))
        users_commented = []

        if(username == username1):
            namef = "users.txt"
        else:
            namef = "users2.txt"

        if not os.path.exists(namef):
            open(namef, 'w')
        with open(namef, 'r') as f:
            for line in f:
                tmp = line.replace('\n', '')
                users_commented.append(tmp)
        followers2 = getTotalFollowers(api, user_id)
        followers = []
        for fol in followers2:
            if(fol['is_verified'] == False):
                followers.append(fol['username'])
        for fol in followers:
            if(count < usr_qtd):
                if(fol not in users_commented):
                    text += "@" + fol + " "
                    count+=1
                    with open(namef, 'a') as f:
                        f.write(fol+'\n')
            else:
                if(comments < maxcomment):
                    if(partial == 10):
                        partial = 0
                        print("Precisamos parar por 15 minutos")
                        time.sleep(60*15)
                    interval = randint(0, 30)
                    time.sleep(60+interval)
                    print("Comentando: {}. Aguarde {} segundos...".format(text, 60+interval))
                    print("Comentarios ate agora: {}".format(comments))
                    ok = api.comment(media_id, text)
                    if(ok):
                        with open('qtd.txt', 'a') as f:
                            f.write(str(comments)+'\n')
                    else:
                        break
                    count = 0
                    partial+=1
                    comments+=1
                    text = ""
                else:
                    break
        #print(result)
