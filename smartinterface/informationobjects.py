import re

class ErrorObject:
    def __init__(self, errorType, errorTime, errorDetails, erredFunction):
        self.errorType = errorType
        self.errorTime = errorTime
        self.errorDetails = errorDetails
        self.erredFunction = erredFunction

    def ToString(self):
        returnString = str(self.errorType) + " error occurred in " + str(self.erredFunction)
        timeString = str(self.errorTime).replace(':', '-')
        returnString += " at " + timeString + " Detail: " + str(self.errorDetails) + "\n"
        return returnString

    def GenericTruncString(self):
        returnString = str(self.errorType) + re.sub("\.[0-9]*", " ", str(self.errorTime))
        returnString += str(self.erredFunction)
        return returnString

class InfoObject:
    def __init__(self, infoType, infoTime, infoDetails, infoedFunction):
        self.infoType = infoType
        self.infoTime = infoTime
        self.infoDetails = infoDetails
        self.infoedFunction = infoedFunction

    def ToString(self):
        returnString = str(self.infoType) + " event occurred in " + str(self.infoedFunction)
        timeString = str(self.infoTime).replace(':', '-')
        returnString += " at " + timeString + " Detail: " + str(self.infoDetails) + "\n"
        return returnString

    def GenericTruncString(self):
            returnString = str(self.infoType) + re.sub("\.[0-9]*", " ", str(self.infoTime))
            returnString += str(self.infoedFunction)
            return returnString
