import requests
from bs4 import BeautifulSoup

class Session(object):
    def __init__(self, user, passwd):
        s = requests.session()
        initUrl = r'https://v.vungle.com/dashboard/login'
        r = s.get(initUrl)
        soup = BeautifulSoup(r.text, "lxml")
        _csrf = soup.input['value']

        login_data = {'email': user, 'password': passwd, '_csrf': _csrf}
        s.post(initUrl, login_data)

        self.session = s

    def getSession(self):
        return self.session
