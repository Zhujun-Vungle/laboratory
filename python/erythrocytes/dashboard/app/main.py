from utils.export import Excel
from utils.session import Session
from utils.urls import Url

user = 'user'
passwd = 'passwd'

instance = Session(user=user, passwd=passwd)
s = instance.getSession()

# res = s.get(r'https://v.vungle.com/dashboard/api/1/accounts/561e8d936b8d90f61a0010c7')

account_id = r'561e8d936b8d90f61a0010c7'
startDate = r'2017-05-30T00%3A00%3A00.000Z'
endDate = r'2017-06-06T00%3A00%3A00.000Z'

url = Url()
campaignUrl = url.campaigns(account_id, startDate, endDate)

res = s.get(campaignUrl)


# test = s.get(url.accounts('59262ee197ee38d51300116a'))

jsonData = res.json()

print(jsonData)
out = Excel()

# print(jsonData)
# out.ingestJson(jsonData[0])

print(len(jsonData[0]['appBlacklist']))
