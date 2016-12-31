import imaplib, smtplib, email
import serverlogger, informationobjects
import smartserver
import traceback #for error checking
import base64, quopri
import datetime
import re
import time
import os

SERVERACCOUNT = ''
ACCOUNTPASS = ''
PHONE = ''

class MailAccessor:
    def __init__(self):
        global SERVERACCOUNT
        global ACCOUNTPASS
        global PHONE

        accessorConfigurationFilePath = os.path.normpath('config/accessor.conf')
        loginInformationFile = open(accessorConfigurationFilePath)
        fileContents = loginInformationFile.read();
        fileContents = fileContents.split(' ')
        SERVERACCOUNT = fileContents[0]
        ACCOUNTPASS = fileContents[1]

        phoneConfigurationFilePath = os.path.normpath('config/phone.conf')
        loginInformationFile = open(phoneConfigurationFilePath)
        fileContents = loginInformationFile.read();
        fileContents = fileContents.split(' ')
        PHONE = fileContents[0]

        self._logger = serverlogger.ServerLogger()
        self._monitoredList = []
        # dictionary struct to put in monitoredList : { account, password}
        with open(os.path.normpath('database/monitored.conf')) as monitoredFile:
            for line in monitoredFile:
                tempDict = {}
                line = line.split(' ')
                tempDict['account'] = line[0].strip()
                tempDict['password'] = line[1].strip()
                self._monitoredList.append(tempDict)
        self._monitoredConnections = []
        self._server = smartserver.SmartServer()
        self._SMTPConnection = None
        self._currentCommand = None
        try:
            self._serverInbox = imaplib.IMAP4_SSL("imap.gmail.com")
            self._serverInbox.login(SERVERACCOUNT, ACCOUNTPASS)
            info = informationobjects.InfoObject('IMAP', datetime.datetime.now(), 'command connection success', 'mail constructor')
            self._logger.LogInfo(info)
            connectedCommands = True
        except:
            connectedCommands = False
            stackTrace = traceback.format_exc()
            error = informationobjects.ErrorObject('IMAP', datetime.datetime.now(), 'comman connection failed: ' + stackTrace, 'mail constructor')
            self._logger.LogError(error)
            print (stackTrace)
            print ("Failed to connect to server email")

        try:
            for mailbox in self._monitoredList:
                tempConnection = imaplib.IMAP4_SSL("imap.gmail.com")
                tempConnection.login(mailbox['account'], mailbox['password'])
                self._monitoredConnections.append(tempConnection)
                info = informationobjects.InfoObject('IMAP', datetime.datetime.now(), 'notification connection success', 'mail constructor')
                self._logger.LogInfo(info)
                connectedNotifications = True
        except:
            connectedNotifications = False
            stackTrace = traceback.format_exc()
            error = informationobjects.ErrorObject('IMAP', datetime.datetime.now(), '1 or more notification connections failed: ' + stackTrace, 'mail constructor')
            self._logger.LogError(error)
            print (stackTrace)
            print ("Failed to connect to one or more monitored emails")

        if connectedNotifications and connectedCommands:
            self.ConnectSMTPSender(SERVERACCOUNT, ACCOUNTPASS)
            self.SendMail("Successfully started server")
            self.TerminateSMTPSender()
            info = informationobjects.InfoObject('general', datetime.datetime.now(), 'Startup success', 'mail constructor')
            self._logger.LogInfo(info)

    def CheckForNotifications(self):
        notificationList = []
        for box in self._monitoredConnections:
            try:
                box.select("INBOX")
                typ, msgnums = box.search(None, 'UNSEEN', 'Since "05-Aug-2016"')
            except:
                print (traceback.format_exc())
                print ("Failed to select an inbox")

            msgnum = msgnums[0].split()
            print(msgnum)
            emptylist = []

            if msgnum != emptylist:
                for item in msgnum:
                    status, data = box.fetch(item, "(RFC822)")

                    message = data[0][1]

                    email_message = email.message_from_string(message.decode('utf-8'))
                    notificationList.append(email_message['Subject'])
        return notificationList

    def SendNotifications(self, notificationList):
        global SERVERACCOUNT
        global ACCOUNTPASS
        for item in notificationList:
            self.ConnectSMTPSender(SERVERACCOUNT, ACCOUNTPASS)
            item.replace(':', '')
            print(item)
            self.SendMail(item)
            self.TerminateSMTPSender()


    def SelectInbox(self):
        status = self._serverInbox.select("INBOX")
        if status[0] == 'OK':
            return True
        return False

    def RetrieveCommands(self):
        typ, msgnums = self._serverInbox.search(None, 'UNSEEN', 'SINCE "05-Aug-2016"')
        msgnum = msgnums[0].split()

        if msgnum:
            status, data = self._serverInbox.fetch(msgnum[-1], "(RFC822)")

            message = data[0][1]
            # print(message)

            email_message = email.message_from_string(message.decode('utf-8'))

            transferEncoding = email_message['Content-Transfer-Encoding']
            print(email_message['Content-Transfer-Encoding'])

            temporaryBody = email_message.get_payload()

            if transferEncoding == 'base64':
                temporaryBody = self._ConvertFromBase64(temporaryBody)
                # print (temporaryBody)
            elif transferEncoding == 'quoted-printable':
                temporaryBody = self._ConvertFromQuotedPrintable(temporaryBody)

            self._currentCommand = temporaryBody
            return True
        return False

    def ProcessCommand(self):
        global SERVERACCOUNT
        global ACCOUNTPASS
        self._server.PrepareCommand(self._currentCommand)
        result = self._server.ProcessCommand()

        returnToMain = False
        # print(result)

        # print(type(result))
        if type(result) == bool:
            returnToMain = result
            result = "terminating server"

        self.ConnectSMTPSender(SERVERACCOUNT, ACCOUNTPASS)
        self.SendMail(result)
        self.TerminateSMTPSender()
        return returnToMain

    def ConnectSMTPSender(self, account, password):


        try:
            self._SMTPConnection = smtplib.SMTP("smtp.gmail.com", 25)
            print(self._SMTPConnection.starttls())
            print(self._SMTPConnection.login(account, password))
        except:
            print (traceback.format_exc())
            print ("Failed to connect to send.")

    def SendMail(self, message):
        global PHONE
        specialChars = re.compile(r'\n|:|\r|/|\[|\]|#')
        message = re.sub(specialChars, '', message)
        print (datetime.datetime.now())
        try:
            print(self._SMTPConnection.sendmail("server@server.com", PHONE, message))
            time.sleep(5)
        except:
            print ("Failed to send mail")
            print (traceback.format_exc())

    def TerminateSMTPSender(self):
        try:
            print(self._SMTPConnection.quit())
        except:
            print(traceback.format_exc())
            print("Failed to terminate SMTP properly")

    def TerminateIMAP(self):
        try:
            for mailbox in self._monitoredConnections:
                mailbox.close()
                mailbox.logout()
        except:
            print (traceback.format_exc())
            print ("Failed to terminate one or more monitored emails")
        try:
            self._serverInbox.close()
            self._serverInbox.logout()
        except:
            print(traceback.format_exc())
            print("Failed to Terminate server IMAP properly")

    def _ConvertFromQuotedPrintable(self, quotedPrintableString):
        bytesOfDecodedFromQuoPri = quopri.decodestring(quotedPrintableString)
        stringDecodedFromQuoPri = bytesOfDecodedFromQuoPri.decode()
        # print(stringDecodedFromQuoPri)
        return stringDecodedFromQuoPri

    def _ConvertFromBase64(self, b64String):
        print(type(b64String))
        base64bytes = b64String.encode()
        bytesOfDecodedFromB64 = base64.decodestring(base64bytes)
        stringDecodedFromB64 = bytesOfDecodedFromB64.decode()
        # print("to be implemented")
        return stringDecodedFromB64

#for testing purposes only
def main():
    testserver = MailAccessor()
    print("hi")
    # testserver.SelectInbox()
    alerts = testserver.CheckForNotifications()
    testserver.SendNotifications(alerts)

if __name__ == "__main__":
    main()
