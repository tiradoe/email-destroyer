import imaplib
import chardet
import time
import re
import sys
from email.parser import HeaderParser

imaplib._MAXLINE = 3000000

def connect_imap(email_account):
    """Log into email account"""

    imap_conn = imaplib.IMAP4_SSL(email_account.host, int(email_account.port))
    imap_conn.login(email_account.email, email_account.password)

    return imap_conn


def get_inbox_count(email_account):
    """Returns current inbox message count"""
    print('Getting message count...')

    imap_conn = connect_imap(email_account)
    count = imap_conn.select(email_account.folder)[1][0]
    imap_conn.logout()

    print('\nCurrent message count for %s is %d\n' % (email_account.email, int(count)))

    return int(count)


def delete_imap(email_account, date, imap_search):
    """Delete emails from provided account"""
    try:
        print('Connecting to %s' % email_account.email)
        imap_conn = connect_imap(email_account)
    except:
        print('Login Failed.  Trying again.')
        time.sleep(3)
        delete_imap(email_account,date)

    imap_conn.select(email_account.folder)

    #Get emails from provided date
    imap_search = '(%s)' % imap_search
    print("Search criteria: %s" % imap_search)

    typ, data = imap_conn.search(None, imap_search)

    print('Removing emails marked for deletion...')
    imap_conn.expunge()


    print('Deleting email from %s.  Folder: %s\n' % (email_account.email, email_account.folder))

    for num in data[0].split():
        try:
            if int(num) % 500 == 0:
                print('\n****Removing emails marked for deletion****\n')
                imap_conn.expunge()

            typ, data = imap_conn.fetch(num, '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
            raw_header = data[0][1]
            reload(sys)
            sys.setdefaultencoding('utf-8')
            #encoding = chardet.detect(raw_header)
            #header_data = raw_header.decode(encoding['encoding'])
            try:
                header_data = raw_header.encode('utf-8')

                parser = HeaderParser()
                msg = parser.parsestr(header_data)

                imap_conn.store(num, '+FLAGS', '\\Deleted')
                print('Message %s\n%s\n' % (int(num), msg['subject'].encode('utf-8')))
            except:
                pass

        except imap_conn.abort as e:
            print(e)
            time.sleep(5)
            #imap_conn.close()

            delete_imap(email_account,date)
            continue

        except Exception as e:
            print(e)
            time.sleep(5)
            #imap_conn.close()

            delete_imap(email_account,date)
            continue

    imap_conn.expunge()
    imap_conn.close()
    imap_conn.logout()
