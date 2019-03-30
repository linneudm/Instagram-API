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
                res = api.getMediaComments(media_id)
        else:
            break

    print("Quantos usuarios por comentário?")
    usr_qtd = int(input())
    comments = 0
    #maxcomment = 20
    partial = 0
    count = 0
    text = ""
    print("Agora, vamos comentar com os segudires de {}.".format(user_f))
    followers = getTotalFollowers(api, user_id)
    for fol in followers:
        if(count < usr_qtd):
            if(fol['is_verified'] == False):
                text += "@" + fol['username'] + " "
                count+=1
        else:
            if(comments < maxcomment):
                if(partial == 15):
                    partial = 0
                    print("Precisamos parar por 15 minutos")
                    time.sleep(60*15)
                interval = randint(0, 30)
                time.sleep(5+interval)
                print("Comentando: {}. Aguarde {} segundos...".format(text, 30+interval))
                print("Comentarios ate agora: {}".format(comments))
                api.comment(media_id, text)
                count = 0
                partial+=1
                comments+=1
                text = ""
            else:
                break
    #print(result)
