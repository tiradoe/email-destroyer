import imaplib
import chardet
import time
import re
import sys
import logging
from email.parser import HeaderParser

imaplib._MAXLINE = 3000000

logging.basicConfig(filename='logs/deleter.log',format='%(asctime)s:%(levelname)s:%(message)s',datefmt='%Y-%m-%d %H:%M',level=logging.DEBUG)


def connect_imap(email_account):
    """Log into email account"""

    imap_conn = imaplib.IMAP4_SSL(email_account.host, int(email_account.port))
    imap_conn.login(email_account.email, email_account.password)

    return imap_conn


def get_inbox_count(email_account):
    """Returns current inbox message count"""
    logging.info('Getting message count for %s...' % email_account.email)

    try:
        imap_conn = connect_imap(email_account)
        count = imap_conn.select(email_account.folder)[1][0]
        imap_conn.logout()

        logging.info('Current message count for %s is %d' % (email_account.email, int(count)))
    except Exception as e:
        logging.warning('Failed to get message count for %s' % email_account.email)
        logging.debug(e)
        count = 0


    return int(count)


def delete_imap(email_account, date, imap_search):
    """Delete emails from provided account"""
    try:
        logging.info('Connecting to %s' % email_account.email)
        imap_conn = connect_imap(email_account)
    except Exception as e:
        logging.warning('Login Failed for %s.  Trying again.' % email_account.email)
        logging.debug(e)
        time.sleep(3)
        delete_imap(email_account,date,imap_search)


    try:
        imap_conn.select(email_account.folder)

        #Get emails from provided date
        imap_search = '(%s)' % imap_search
        typ, data = imap_conn.search(None, imap_search)

        logging.info('Removing emails marked for deletion from %s' % email_account.email)
        imap_conn.expunge()
    except exception as e:
        logging.warning('Failed to select messages from %s' % email_account.email)
        logging.debug(e)



    logging.info('Deleting email from %s.  Folder: %s' % (email_account.email, email_account.folder))

    for num in data[0].split():
        try:
            if int(num) % 500 == 0:
                logging.info('Removing emails marked for deletion from %s' % email_account.email)
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
                #print('Message %s\n%s\n' % (int(num), msg['subject'].encode('utf-8')))
            except:
                pass

        except imap_conn.abort as e:
            logging.debug(e)
            time.sleep(5)
            #imap_conn.close()

            delete_imap(email_account,date,imap_search)
            continue

        except Exception as e:
            logging.debug(e)
            time.sleep(5)
            #imap_conn.close()

            delete_imap(email_account,date,imap_search)
            continue

    try:
        imap_conn.expunge()
        imap_conn.close()
        imap_conn.logout()
    except Exception as e:
        (e)
