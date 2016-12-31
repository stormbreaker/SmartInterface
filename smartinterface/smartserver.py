import featuremodule.mojicoder as mojicoder
import datetime


class SmartServer:
    def __init__(self):
        self._moji = mojicoder.MojiCoder()
        self._functionDict = self._GetFunctions()
        self._preparedCommand = None
        self._starttime = datetime.datetime.now()

    def _GetFunctions(self):
        d = {}
        d['demoji'] = self.Demoji
        d['enoji'] = self.Enoji
        d['st'] = self.Status
        d['term'] = self.Terminate

        return d

    def PrepareCommand(self, commandString):
        commandList = commandString.split()
        command = commandList[0].lower()
        commandParameters = " ".join(commandList[1:])

        self._preparedCommand = [command, commandParameters]

        return

    def ProcessCommand(self):
        if self._preparedCommand[0] not in self._functionDict:
            return "command " + self._preparedCommand[0] + " not found"
        result = self._functionDict[self._preparedCommand[0]](self._preparedCommand[1])
        print(result)
        return result

    def Enoji(self, content):
        print("To be implemented")
        return

    def Demoji(self, content):
        # print("Content in server", content)
        returnVal = self._moji.Demoji(content)
        return returnVal

    def Status(self, detail):
        params = detail.split()
        information = ''

        print (params)

        if params[0] == 'op':
            information = 'online'

        elif params[0] == 'time':
            information = str(datetime.datetime.now() - self._starttime)
            information = information.replace(':', '_')

        elif params[0] == 'detail':
            information = 'online';
            information += " " + str(datetime.datetime.now() - self._starttime)
            information = information.replace(':', '_')
        # print("To be implemented")
        return information

    def Terminate(self, detail):
        return True
