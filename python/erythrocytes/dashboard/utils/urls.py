# base_adv = r"https://v.vungle.com/dashboard/accounts/ad"
# base_pub = r"https://v.vungle.com/dashboard/accounts/pub"
base_api = r"https://v.vungle.com/dashboard/api/1/accounts"


class Url(object):
    def campaigns(self, account_id, startDate, endDate):
        return '%s/%s/campaigns?endDate=%s&startDate=%s&status=active' % (base_api, account_id, endDate, startDate)

    def brands(self, account_id, startDate, endDate):
        return '%s/%s/brands?endDate=%s&startDate=%s&status=active' % (base_api, account_id, endDate, startDate)

    def apps(self, account_id, startDate, endDate):
        return '%s/%s/apps?status=a&endDate=%s&startDate=%s' % (base_api, account_id, startDate, endDate)

    def accounts(self,account_id):
        return'%s/%s' % (base_api, account_id)
    # special encode
    # def creatives(self, account_id):
    #     return '%s/creatives?status=active&fields%5B%5D=status&fields%5B%5D=archived&fields%5B%5D=name&fields%5B%5D=application&fields%5B%5D=language&fields%5B%5D=enforceLanguage&fields%5B%5D=postBundle&fields%5B%5D=created&fields%5B%5D=format&populate%5Bapplication%5D%5B%5D=name&parentAccount=%s&limit=0' % (
    #         base_api, account_id)


# class PublisherUrl(object):

# class AccountsUrl(object):
