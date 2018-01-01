#  -*- coding: utf-8 -*-

__author__ = 'labike'


def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = ''
    auth_url = weibo_auth_url + '?client_id={client_id}&redirect_uri={re_url}'.format(client_id=4182914825, re_url=redirect_url)
    print(auth_url)


def get_access_token(code=''):
    access_token_url = 'https://api.weibo.com/oauth2/authorize'
    import requests
    re_dict = requests.post(access_token_url, data={
        'client_id': 4182914825,
        'client_secret': '984445a3d59182f3004e7a42900650e4',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': ''
    })


def get_user_info(access_token='', uid=''):
    user_url = 'https://api.weibo.com/2/users/show.json&access_token={token}&uid={uid}'.format(token=access_token, uid=uid)
    print(user_url)


if '__name__' == '__main__':
    #get_auth_url()
    #get_access_token(code='')
    get_user_info(access_token='', uid='')