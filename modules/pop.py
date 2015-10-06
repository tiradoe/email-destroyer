import poplib
from email import parser
from email.parser import HeaderParser

def connect_pop(email_account):
    pop_conn = poplib.POP3(email_account.host)
    pop_conn.user(email_account.email)
    pop_conn.pass_(email_account.password)

    return pop_conn


def delete_pop(email_account):
    pop_conn = connect_pop(email_account)
    pop_list = pop_conn.list()

    if pop_list[0].startswith('+OK'):
        msg_list = pop_list[1]

        for msg_spec in msg_list:
            try:
                msg_num = int(msg_spec.split(' ')[0])
                print("Deleting message %d\n" % msg_num )
                pop_conn.dele(msg_num)

            except Exception as e:
                print(e)
                continue


    else:
        print("Could not list messages: status", pop_list[0])

    pop_conn.quit()
