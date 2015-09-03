import imaplib

def connect_imap(email_account):
    imap_conn = imaplib.IMAP4_SSL(email_account.host, int(email_account.port))
    imap_conn.login(email_account.email, email_account.password)

    return imap_conn


def delete_imap(email_account):
    imap_conn = connect_imap(email_account)
    imap_conn.select(email_account.folder)

    typ, data = imap_conn.search(None, 'ALL')

    for num in data[0].split():
        try:
            typ, data = imap_conn.fetch(num, '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
            header_data = data[0][1]
            parser = HeaderParser()
            msg = parser.parsestr(header_data)
            imap_conn.store(num, '+FLAGS', '\\Deleted')
            print('Message %s\n%s\n' % (num, msg['subject']))

        except imap_conn.abort, e:
            print('abort')
            continue

        except error, e:
            print(e)

        except Exception, e:
            print(e)
            continue

    imap_conn.expunge()
    imap_conn.close()
    imap_conn.logout()
