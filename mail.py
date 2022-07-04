import smtplib
import time
import imaplib
import email
import email.header
import traceback

def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))

def read_email_from_gmail(user, password, mode):
    mails = []

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)
    try:

        mail.select('inbox', readonly=True)

        data = mail.search(None, mode)
        mail_ids = data[1]
        id_list = [int(i) for i in mail_ids[0].split()]

        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in id_list[::-1]:

            data = mail.fetch(str(i), '(RFC822)')

            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = decode_mime_words(msg['subject'])
                    email_from = decode_mime_words(msg['from'])
                    mails.append([email_from, email_subject])



    except Exception as e:
        pass
    return mails
