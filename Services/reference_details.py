class ISO(object):

    def __init__(self):
        self.params = str()
        self.__msgType = {"length": 4, "start": 0, "end": 4}
        self.__primaryBitMap = {"length": 16, "start": 4, "end": 20}
        self.__secondBitMap = {"length": 16, "start": 20, "end": 36}
        self.__processingCode = {"length": 6, "start": 55, "end": 61}
        self.__timeLocalTrx = {"length": 6, "start": 79, "end": 85}
        self.__dateLocalTrx = {"length": 8, "start": 85, "end": 93}
        self.__transactionCurrency = {"length": 3, "start": 189, "end": 192}
        self.__pll = {"length": 4, "start": 192, "end": 196}

    def consult(self, params: str):
        self.params = self.__parse_iso(params)

    def __parse_iso(self, iso: str):
        msg = "0210"
        iso = iso.replace(iso[self.__msgType["start"]:self.__msgType["end"]], msg, 1)
        return iso
