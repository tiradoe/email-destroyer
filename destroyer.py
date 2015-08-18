"""
Empties trash for a provided list of email accounts
Author: Edward Tirado Jr
"""
import imaplib
import csv
from email.parser import HeaderParser


class EmailAccount(object):
    """An email account"""
    def __init__(self, host, email, password, folder, port=993):
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self.folder = folder


def get_accounts(file_name):
    """creates list of accounts from csv"""
    account_info = []

    with open(file_name, 'rU') as csvfile:
        accounts = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in accounts:
            account_info.append(', '.join(row))

        return account_info


def empty_folder(email_account):
    """Empties trash folder for provided account"""
    imap_conn = imaplib.IMAP4_SSL(email_account.host, int(email_account.port))
    imap_conn.login(email_account.email, email_account.password)
    imap_conn.select(email_account.folder)

    typ, data = imap_conn.search(None, 'ALL')

    for num in data[0].split():
        typ, data = imap_conn.fetch(num, '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
        header_data = data[0][1]
        parser = HeaderParser()
        msg = parser.parsestr(header_data)
        imap_conn.store(num, '+FLAGS', '\\Deleted')
        print 'Message %s\n%s\n' % (num, msg['subject'])

    imap_conn.expunge()
    imap_conn.close()
    imap_conn.logout()


def main():
    """Main.  Where the magic happens."""

    all_accounts = get_accounts('accounts.csv')

    for account in all_accounts:
        account_info = account.split(',')

        print "Deleting email from %s folder in %s account" % (account_info[3], account_info[1])

        email_account = EmailAccount(account_info[0], # host
                                     account_info[1].strip(), # email
                                     account_info[2].strip(), # password
                                     account_info[3].strip(), # folder
                                     account_info[4], # port
                                    )

        empty_folder(email_account)

    print "Hasta la vista, email."

if  __name__ == '__main__':
    main()
