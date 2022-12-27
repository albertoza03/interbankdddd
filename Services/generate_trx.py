import datetime
import json
import random

from faker import Faker


class GenerateTrx(object):

    def __init__(self):
        iso_file = open("./iso.json", "r")
        self.__baseTrx = json.loads(iso_file.read())
        iso_file.close()
        self.__fake = Faker()

    def generate(self):
        now = datetime.datetime.utcnow()
        expiration = now + datetime.timedelta(days=7)
        self.__baseTrx['trx']['merchantName'] = self.__fake.name()
        self.__baseTrx['trx']['referenceProcessor'] = str(random.randint(000000000, 999999999))
        self.__baseTrx['trx']['expirationTime'] = int(round(expiration.timestamp()))
        iso_file = open("./iso.json", "w")
        iso_file.write(json.dumps(self.__baseTrx, indent=4))
        iso_file.close()
        return self.__baseTrx['trx']
