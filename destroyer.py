#!bin/python

"""
Empties email folder for a provided list of email accounts
Author: Edward Tirado Jr
"""

from __future__ import print_function
from socket import error
import csv
import argparse
import sys
import datetime
import modules.imap as imap_mod
import modules.pop as pop_mod

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

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
    parser.add_argument('--count', '-c', help="Get count of emails in provided accounts.  Takes in a file location.")
    parser.add_argument('--before', '-b', help="Limit deleted messages to those before the provided date")
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


def get_date_for_processing(current_date):
    """Takes in a date and returns a date that is one month earlier."""
    split_date = current_date.split('-')
    day,month,year= split_date[0],split_date[1],split_date[2]

    if MONTHS.index(month) == 0:
        month = 'Dec'
        year = int(year) - 1
    else:
        month = MONTHS[MONTHS.index(month) -1 ]

    date = '-'.join([day,month,year])

    return date


def empty_folder(email_account, imap_search):
    """Empties trash folder for provided account"""

    current_date = datetime.datetime.now().strftime("%d-%b-%Y")
    date = get_date_for_processing(current_date)
    print(date)

    if 'imap' in email_account.connection.lower():
        email_count = imap_mod.get_inbox_count(email_account)

        while (email_count > 0):
            imap_mod.delete_imap(email_account, date, imap_search)
            date = get_date_for_processing(date)
            email_count = imap_mod.get_inbox_count(email_account)
    else:
        pop_mod.delete_pop(email_account)


def main():
    """Main.  Where the magic happens."""

    args = process_args()
    arg_list = [args.file, args.count, args.list]
    accounts_csv = 'accounts.csv'

    for arg in arg_list:
        if arg != None:
            accounts_csv = arg

    all_accounts = get_accounts(accounts_csv)


    if args.list != None:
        list_folders(all_accounts)

    if args.before != None:
        imap_search = 'SENTBEFORE "%s"' % str(args.before)
    else:
        imap_search = 'ALL'


    for account in all_accounts:
        account_info = account.split(',')

        email_account = EmailAccount(account_info[0], # host
                                     account_info[1].strip(), # email
                                     account_info[2].strip(), # password
                                     account_info[3].strip(), # folder
                                     account_info[4], # port
                                     account_info[5], #connection
                                    )

        if args.count != None:
            email_count = imap_mod.get_inbox_count(email_account)
        else:
            empty_folder(email_account, imap_search)

    print("Hasta la vista, email.")


if  __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('\nBye!')
