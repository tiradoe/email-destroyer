import imaplib
import chardet
import time
import re
from email.parser import HeaderParser

imaplib._MAXLINE = 3000000

def connect_imap(email_account):
    print('Connecting to %s' % email_account.email)
    imap_conn = imaplib.IMAP4_SSL(email_account.host, int(email_account.port))
    imap_conn.login(email_account.email, email_account.password)

    return imap_conn


def delete_imap(email_account):
    try:
        imap_conn = connect_imap(email_account)
    except:
        print('Login Failed.  Trying again.')
        time.sleep(3)
        delete_imap(email_account)

    imap_conn.select(email_account.folder)

    typ, data = imap_conn.search(None, 'ALL')

    print('Clearing out emails marked for deletion...')
    imap_conn.expunge()


    print('Deleting email from %s\n' % email_account.email)

    for num in data[0].split():
        try:
            typ, data = imap_conn.fetch(num, '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
            raw_header = data[0][1]
            encoding = chardet.detect(raw_header)
            header_data = raw_header.decode(encoding['encoding'])

            parser = HeaderParser()
            msg = parser.parsestr(header_data)

            imap_conn.store(num, '+FLAGS', '\\Deleted')
            print('Message %s\n%s\n' % (int(num), msg['subject']))

        except imap_conn.abort as e:
            print(e)
            time.sleep(5)
            imap_conn.logout()

            delete_imap(email_account)
            continue

        except Exception as e:
            print(e)
            time.sleep(5)
            imap_conn.logout()
            delete_imap(email_account)
            continue

    imap_conn.expunge()
    imap_conn.close()
    imap_conn.logout()
