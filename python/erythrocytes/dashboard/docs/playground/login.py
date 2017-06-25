# import requests
# from bs4 import BeautifulSoup
#
# url = r'https://v.vungle.com/dashboard/login'
# user = 'user'
# passwd = 'passwd'
# s = requests.session()
# r = s.get(url)
#
# soup = BeautifulSoup(r.text)
# _csrf = soup.input['value']
#
# login_data = {'email': user, 'password': passwd, '_csrf': _csrf}
# s.post(url, login_data)
# # r = s.get(r'https://v.vungle.com/dashboard/api/1/accounts/59262ee197ee38d51300116a')
# r = s.get(r'https://v.vungle.com/dashboard/api/1/accounts/561e8d936b8d90f61a0010c7')
# rson = r.json()
#
# print(rson)
