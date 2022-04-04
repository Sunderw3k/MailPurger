#!/usr/bin/env python

import imaplib
import datetime
import math


def login():
    # Credentials
    mail = input("Input your mail: ")
    passwd = input("Input your password: ")

    # IMAP instance
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login
    imap.login(mail, passwd)

    return imap

def main():
    imap = login()
    # Time

    months = input("Input the number of months to keep: ")
    try:
        months = int(months)
    except ValueError:
        print("Date isnt a number!")

    now = datetime.datetime.now()

    if now.month - months % 12 <= 0:
        until = datetime.datetime(now.year - (math.floor(months/12)+1), now.month + 12 - months % 12, now.day)
        until = until.strftime('%d-%b-%Y')
    elif months >= 12:
        until = datetime.datetime(now.year - math.floor(months/12), now.month - months % 12, now.day)
        until = until.strftime('%d-%b-%Y')
    else:
        until = datetime.datetime(now.year, now.month - months % 12, now.day)
        until = until.strftime('%d-%b-%Y')

    print(f"\nRemoving all non-starred mails before {until}")
    print("Note: This is a loop, it will repeat forever.")

    # Messages
    while True:
    
        # Select messages
        imap.select("INBOX")

        status1, starred = imap.search(None, "FLAGGED")
        status2, data = imap.search(None, f'(BEFORE {until})')

        if status1 != "OK" or status2 != "OK":
            print("Something broke!")
    
        if starred != [b'']:
            starred = [int(x) for x in starred[0].split(b' ')]

        # Read messages
        for mail in data[0].split():

            mail = int(mail)
    
            if mail in starred:
                print(mail, "skip")
                continue
            print(mail)
            imap.store(str(mail), "+FLAGS", "\\DELETED")
    
        imap.expunge()

if __name__ == "__main__":
    main()
