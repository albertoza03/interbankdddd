import json
import random
import datetime

from Services.validate import ValidateISO


class ISO(object):

    def __init__(self):
        self.params = str()
        self.__msgType = {"length": 4, "start": 0, "end": 4}
        self.__processingCode = {"length": 6, "start": 55, "end": 61}

        self.__codErrorOriPosition = {"length": 3, "start": 171, "end": 174}
        self.__merchantNamePosition = {"length": 25, "start": 234, "end": 259}
        self.__codErrorOri = '000'

        self.__valid = ValidateISO()

        iso_file = open("./iso.json", "r")
        self.__baseFile = json.loads(iso_file.read())
        self.__baseTrx: dict = self.__baseFile['trx']
        self.__consultRespISO = self.__baseFile['consultRespISO']
        iso_file.close()

    def consult(self, params: str):
        self.params = self.__parse_iso(params)

    def __parse_iso(self, iso: str):
        base_iso = iso[0:192]
        is_valid = self.__valid.validate_iso(base_iso)
        if is_valid != '000':
            self.__codErrorOri = is_valid

        base_iso = base_iso.replace(base_iso[self.__msgType['start']:self.__msgType['end']], "0210", 1)
        pro = base_iso[self.__processingCode['start']:self.__processingCode['end']]

        if pro != '310000':
            self.__codErrorOri = '002'

        reference_number = str(self.__baseTrx.get('referenceProcessor'))
        iso_reference_number = iso[208:221].strip()
        if reference_number != iso_reference_number:
            self.__codErrorOri = '019'

        first_part = self.__generate_new_base_iso(base_iso)
        second_iso = self.__generate_second_part_iso(iso)
        second_length = self.__get_second_part_length(str(len(second_iso)))
        print(second_length)

        return first_part + second_length + second_iso

    def __generate_second_part_iso(self, old_iso: str) -> str:
        data = self.__baseFile['response']
        consult_type = old_iso[206:207]
        consult_num = old_iso[208:222]
        print(len(consult_num), old_iso[208:222])
        description = self.__valid.get_description_response(self.__codErrorOri)
        client_name = data['clientName']
        merchant_name = self.__get_merchant_name(self.__baseFile['trx']['merchantName'])
        product_code = old_iso[203:206]
        product_description = self.__get_merchant_name(self.__baseFile['trx']['merchantName'], 20)
        document_number = self.__get_amount(random.randint(000000000000000, 999999999999999), 15)
        document_description = data['documentDescription']
        expiration_date = datetime.datetime.fromtimestamp(self.__baseFile['trx']['expirationTime']).strftime("%d%m%Y")
        created = datetime.datetime.now().strftime("%d%m%Y")
        request_amount = self.__get_amount(self.__baseFile['trx']['requestAmount'])
        amount_zero = "000000000000"
        minimum_payment = self.__get_amount(int(request_amount) + int(amount_zero) + int(amount_zero))

        return data['code'] + consult_type + consult_num + self.__codErrorOri + description + client_name + \
            merchant_name + data['documentNumber'] + product_code + product_description + document_number + \
            data['filler01'] + document_description + expiration_date + created + request_amount + amount_zero + \
            amount_zero + minimum_payment + minimum_payment + data['period'] + created[4:8] + data['share'] + \
            data['currency'] + data['filler']

    @staticmethod
    def __get_merchant_name(name: str, max_len=25) -> str:
        if len(name) > max_len:
            name = name[0:max_len]
        else:
            count = max_len - len(name)
            for x in range(count):
                name = name + " "

        return name

    @staticmethod
    def __generate_new_base_iso(old_iso: str) -> str:
        first_part = old_iso[20:126]
        primary = "F03804818E808000"
        approval = str(random.randint(000000, 999999))
        response = "00"
        card_acceptor = old_iso[126:134]
        currency_code = old_iso[189:192]
        return old_iso[0:4] + primary + first_part + approval + response + card_acceptor + currency_code

    @staticmethod
    def __get_amount(amount: int, max_len=12) -> str:
        base_amount = ""
        count = max_len - len(str(amount))
        for x in range(count):
            base_amount = base_amount + "0"

        return base_amount + str(amount)

    @staticmethod
    def __get_second_part_length(second: str) -> str:
        base = ""
        count = 4 - len(second)
        for x in range(count):
            base = base + "0"

        return base + str(second)
