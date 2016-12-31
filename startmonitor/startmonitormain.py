import subprocess
import imaplib
import traceback
import time
import email
import smtplib
import os

SERVERACCOUNT = ''
ACCOUNTPASS = ''
PHONE = ''

def LoadLoginInformation():
    global SERVERACCOUNT
    global ACCOUNTPASS
    global PHONE
    monitorConfigurationFilePath = os.path.normpath('config/monitor.conf')
    loginInformationFile = open(monitorConfigurationFilePath)
    fileContents = loginInformationFile.read();
    fileContents = fileContents.split(' ')
    SERVERACCOUNT = fileContents[0]
    ACCOUNTPASS = fileContents[1]

    phoneConfigurationFilePath = os.path.normpath('config/phone.conf')
    loginInformationFile = open(phoneConfigurationFilePath)
    fileContents = loginInformationFile.read();
    fileContents = fileContents.split(' ')
    PHONE = fileContents[0]

    return

def main():

    global SERVERACCOUNT
    global ACCOUNTPASS
    global PHONE

    authorizedFilePath = os.path.normpath('config/authorized.conf')

    LoadLoginInformation()

    print(SERVERACCOUNT)
    print(ACCOUNTPASS)

    authorizedEmails = open(authorizedFilePath, 'r')

    emails = authorizedEmails.read();

    authorizedEmails.close();

    authorizedEmails = emails.split('\n')

    while True:
        try:
            inbox = imaplib.IMAP4_SSL("imap.gmail.com")
            inbox.login(SERVERACCOUNT, ACCOUNTPASS)
        except:
            print (traceback.format_exc()) #This should get logged
            print ("Failed to connect to server email")


        checkForStart = True


        while checkForStart:
            try:
                time.sleep(60)
                print("Checking")
                status = inbox.select("INBOX")
                if status[0] == 'OK':
                    typ, msgnums = inbox.search(None, 'UNSEEN', 'SINCE "05-Aug-2016"')
                    msgnum = msgnums[0].split()

                    if msgnum:
                        status, data = inbox.fetch(msgnum[-1], "(RFC822)")

                        message = data[0][1]

                        email_message = email.message_from_string(message.decode('utf-8'))

                        fromAddress = email_message.get_all('From')[0]

                        if fromAddress not in authorizedEmails:

                            print(os.getcwd())

                            preLogFilePath = os.path.normpath('log/prelog.log')

                            log = open(preLogFilePath, 'a')

                            log.write("Unauthorized email from: " + fromAddress +'\n')

                            log.close()

                        elif fromAddress in authorizedEmails:

                            body = email_message.get_payload()

                            body = body.strip()

                            print(body.lower())

                            if body.lower() == "start":
                                interfacePath = os.path.normpath('../smartinterface')
                                os.chdir(interfacePath)
                                print(os.getcwd())
                                process = subprocess.Popen('python smartinterface.py')
                                inbox.close()
                                inbox.logout()
                                checkForStart = False
                                process.wait()

                            elif body.lower() == 'st op':
                                try:
                                    connection = smtplib.SMTP("smtp.gmail.com")
                                    connection.starttls()
                                    connection.login(SERVERACCOUNT, ACCOUNTPASS)
                                except:
                                    print (traceback.format_exc())
                                    print ("Failed to connect to send")

                                try:
                                    connection.sendmail("server@server.com", PHONE, "offline")
                                except:
                                    print(traceback.format_exc())
                                    print("Failed to send mail")

                                try:
                                    connection.quit()
                                except:
                                    print (traceback.format_exc())
                                    print ("Failed to terminate SMTP properly")
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print (traceback.format_exc()) #This should get logged
                print ("Something failed in IMAP")



if __name__ == '__main__':
    main()
