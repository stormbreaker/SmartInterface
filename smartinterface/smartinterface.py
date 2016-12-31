import os
import emailaccessor
import time


def main():

    accessor = emailaccessor.MailAccessor()

    termination = False


    while not termination:
        alerts = accessor.CheckForNotifications()
        if alerts:
            accessor.SendNotifications(alerts)

        accessor.SelectInbox()
        command = accessor.RetrieveCommands()
        print(command)
        if command:
            termination = accessor.ProcessCommand()

        print("running")

        # attempt to avoid black listing
        time.sleep(5)

    # We don't wanna leave a bunch of IMAP connections floating around
    accessor.TerminateIMAP()

if __name__ == "__main__":
    main()
