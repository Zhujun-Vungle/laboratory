import csv

class Excel(object):
    def __init__(self):
        self.path = "~/"

    def ingestJson(self, dictData):
        with open('mycsvfile.csv', 'w') as f:
            w = csv.DictWriter(f, dictData.keys())
            w.writeheader()
            w.writerow(dictData)