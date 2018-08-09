def get_auth():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_uri = 'http://211.159.189.158:8001/complete/weibo/'
    auth_url = weibo_auth_url + '?client_id={client_id}&redirect_uri={re_url}'.format(client_id=543023931,
                                                                                      re_url=redirect_uri)
    print(auth_url)


def get_access_token(code='60cfbd5c1e6945f46c8559661c7c159f'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'

    import requests
    re_dict = requests.post(access_token_url, data={
        'client_id': 543023931,
        'client_secret': 'ea23cb0a4feaabe9c671a750b02cadca',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://211.159.189.158:8001/complete/weibo/'

    })
    pass
    # print(re_dict)

def get_user_info(access_token='2.00yxCjLG0V1Tka418f56c7bbnxXT5C', uid=''):
    user_url = 'https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}'.format(token=access_token, uid=uid)

    print(user_url)
if __name__ == '__main__':
    # get_auth()
    # get_access_token(code='60cfbd5c1e6945f46c8559661c7c159f')
    get_user_info(access_token='2.00yxCjLG0V1Tka418f56c7bbnxXT5C', uid='5670072854')

'''
'{"access_token":"2.00yxCjLG0V1Tka418f56c7bbnxXT5C","remind_in":"157679999","expires_in":157679999,"uid":"5670072854","isRealName":"true"}'
'''