import logging #I don't know if I need this
import os
import informationobjects

# This should be a singleton

LOGFILE = os.path.normpath("log/log.log")

class ServerLogger:

    _Instance = None

    def Instance():
        if ServerLogger._Instance == None:
            ServerLogger._Instance = ServerLogger()
        return ServerLogger._Instance

    def __init__(self):
        self._errorlist = []
        self._infolist = []

    def LogError(self, error):
        logFile = open(LOGFILE, 'a')
        errorString = "ERROR : "
        errorString += error.ToString()
        logFile.write(errorString)
        self._errorlist.append(error)
        logFile.close()

    def LogInfo(self, info):
        logFile = open(LOGFILE, 'a')
        infoString = "INFO : "
        infoString += info.ToString()
        logFile.write(infoString)
        logFile.close()

    def ClearErrors(self):
        self._errorlist = []
        #TODO log clear error list

    def ClearInfo(self):
        self._infolist = []
        #TODO log clear info list

    def GetErrorCount(self):
        return len(self._errorlist)

    def GetInfoEventCount(self):
        return len(self._errorlist)

    def GetSpecificError(self, index):
        specificError = self._errorlist[index]
        returnString = specificError.GenericTruncString()
        return returnString
        #TODO log looking at details

    def GetSpecificInfoEvent(self, index):
        specificEvent = self._infolist[index]
        returnString = specificEvent.GenericTruncString()
        return returnString
        #TODO log looking at info event
