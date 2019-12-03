import smtplib

from config import gmail_user, gmail_password, recipient_emails

sent_from = gmail_user
to = recipient_emails
subject = 'Test - Send Email Script'
body = 'This is a test e-mail. Test success?'

email_text = f"""\
From: {sent_from}
To: {", ".join(to)}
Subject: {subject}

{body}
"""

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')