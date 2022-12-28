import datetime


class ValidateISO(object):

    def __init__(self):
        self.__msgType = {"length": 4, "start": 0, "end": 4}
        self.__primaryBitMap = {"length": 16, "start": 4, "end": 20}
        self.__secondBitMap = {"length": 16, "start": 20, "end": 36}
        self.__processingCode = {"length": 6, "start": 55, "end": 61}
        self.__timeLocalTrx = {"length": 6, "start": 79, "end": 85}
        self.__dateLocalTrx = {"length": 8, "start": 85, "end": 93}
        self.__transactionCurrency = {"length": 3, "start": 189, "end": 192}
        self.__pll = {"length": 4, "start": 192, "end": 196}
        self.__codErrorOri = ''

    def validate_iso(self, iso: str):
        code = '000'
        msg = iso[self.__msgType['start']:self.__msgType['end']]
        primary = iso[self.__primaryBitMap['start']:self.__primaryBitMap['end']]
        second = iso[self.__secondBitMap['start']:self.__secondBitMap['end']]
        currency = iso[self.__transactionCurrency['start']:self.__transactionCurrency['end']]

        other_code = self.__validate_other(msg, primary, second, currency)
        if other_code:
            return other_code

        date_code = self.__validate_date(str(iso[self.__dateLocalTrx['start']:self.__dateLocalTrx['end']]))
        if date_code:
            return date_code

        time_code = self.__validate_time(iso[self.__timeLocalTrx['start']:self.__timeLocalTrx['end']])
        if time_code:
            return time_code

        return code

    @staticmethod
    def get_description_response(code: str) -> str:
        match code:
            case "000":
                return "TRANSACCION PROCESADA OK      "
            case "002":
                return "TIPO MSG. INVÁLIDO            "
            case "060":
                return "FECHA TXN. INVÁLIDO           "
            case "061":
                return "HORA TXN. INVÁLIDO            "
            case "019":
                return "CUOTA PAGADA NO EXISTE        "
            case _:
                return "TRANSACCION PROCESADA OK      "

    def __validate_other(self, msg: str, primary: str, second: str, currency: str) -> str:
        code = self.__codErrorOri

        if msg != '0200' or primary != 'F038048188E00000' or second != '0000000000000080' or currency != '604':
            return '002'

        return code

    def __validate_date(self, date: str) -> str:
        code = self.__codErrorOri

        try:
            date = str(datetime.datetime.strptime(f"{date[0:2]}-{date[2:4]}-{date[4:8]}", '%d-%m-%Y'))
        except ValueError:
            return '060'

        if datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') > datetime.datetime.now():
            return '060'

        return code

    def __validate_time(self, time: str) -> str:
        code = self.__codErrorOri

        try:
            datetime.datetime.strptime(f"{time[0:2]}:{time[2:4]}:{time[4:6]}", '%H:%M:%S')
        except ValueError:
            return '061'

        return code
