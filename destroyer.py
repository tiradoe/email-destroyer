#!/usr/bin/python

"""
Empties email folder for a provided list of email accounts
Author: Edward Tirado Jr
"""

from __future__ import print_function
from socket import error
import csv
import argparse
import sys
import modules.imap as imap_mod
import modules.pop as pop_mod

class EmailAccount(object):
    """An email account"""
    def __init__(self, host="", email="", password="", folder="", port=993, connection='imap'):
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self.folder = folder
        self.connection = connection


def process_args():
    """Process provided command line arguments"""
    parser = argparse.ArgumentParser(description="Empty email folders using csv account list")
    parser.add_argument('--file', '-f', help='File location')
    parser.add_argument('--list', '-l', help="List available folders and exit. Takes in file location.")
    args = parser.parse_args()

    return args


def list_folders(accounts):
    """Show available folders for provided accounts"""
    for email_account in accounts:
        account_info = email_account.split(',')

        email_account = EmailAccount(account_info[0], # host
                                     account_info[1].strip(), # email
                                     account_info[2].strip(), # password
                                     account_info[3].strip(), # folder
                                     account_info[4], # port
                                     account_info[5], #connection
                                    )


        if 'imap' in email_account.connection.lower():
            imap_conn = imap_mod.connect_imap(email_account)
            print('\nFolders for %s:\n' % email_account.email)
            print(imap_conn.list())

        else:
            print('\nFolders for %s:' % email_account.email)
            print('Cannot list folders for accounts using POP3')



    sys.exit()


def get_accounts(file_name):
    """creates list of accounts from csv"""
    account_info = []

    try:
        with open(file_name, 'rU') as csvfile:
            accounts = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in accounts:
                account_info.append(', '.join(row))

    except IOError:
        print("Could not read account list")
        sys.exit()

    return account_info


def empty_folder(email_account):
    """Empties trash folder for provided account"""

    if 'imap' in email_account.connection.lower():
        imap_mod.delete_imap(email_account)
    else:
        pop_mod.delete_pop(email_account)


def main():
    """Main.  Where the magic happens."""

    args = process_args()
    accounts_csv = args.file if args.file != None else 'accounts.csv'
    all_accounts = get_accounts(accounts_csv)

    if args.list != None:
        list_folders(all_accounts)

    for account in all_accounts:
        account_info = account.split(',')

        email_account = EmailAccount(account_info[0], # host
                                     account_info[1].strip(), # email
                                     account_info[2].strip(), # password
                                     account_info[3].strip(), # folder
                                     account_info[4], # port
                                     account_info[5], #connection
                                    )

        empty_folder(email_account)

    print("Hasta la vista, email.")


if  __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('\nBye!')
