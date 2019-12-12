import imaplib
import email

from config import gmail_user_2, gmail_password_2
from config import KINDLE_RAW_NOTES_DIRECTORY


c = imaplib.IMAP4_SSL("imap.gmail.com")
c.login(gmail_user_2, gmail_password_2)
c.select(readonly=False)

# print("Searching inbox for unread emails with kindle notes to download...\n")

res, msg_ids = c.search(None, '(Unseen SUBJECT "Kindle Notes")')

for msg_id in msg_ids[0].split():
    res, data = c.fetch(msg_id, "(BODY.PEEK[])")
    body = data[0][1]
    msg = email.message_from_bytes(body)

    for part in msg.walk():

        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if ".csv" in filename:

            # print(f"Downloading {filename}...")

            fp = open(KINDLE_RAW_NOTES_DIRECTORY + '/' + part.get_filename(), 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

# print("\nProcess complete.")