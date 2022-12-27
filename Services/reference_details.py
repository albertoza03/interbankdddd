import json

from Services.validate import ValidateISO


class ISO(object):

    def __init__(self):
        self.params = str()
        self.__msgType = {"length": 4, "start": 0, "end": 4}
        self.__processingCode = {"length": 6, "start": 55, "end": 61}

        self.__codErrorOriPosition = {"length": 3, "start": 171, "end": 174}
        self.__codErrorOri = '000'

        self.__valid = ValidateISO()

        iso_file = open("./iso.json", "r")
        self.__consultRespISO = json.loads(iso_file.read())['consultRespISO']

    def consult(self, params: str):
        self.params = self.__parse_iso(params)

    def __parse_iso(self, iso: str):
        is_valid = self.__valid.validate_iso(iso)
        if is_valid != '000':
            self.__codErrorOri = is_valid

        iso = iso.replace(iso[self.__msgType['start']:self.__msgType['end']], "0210", 1)
        pro = iso[self.__processingCode['start']:self.__processingCode['end']]

        if pro != '310000':
            self.__codErrorOri = '002'

        iso = self.__consultRespISO.replace("ERRORCODE", self.__codErrorOri, 1)

        return iso
