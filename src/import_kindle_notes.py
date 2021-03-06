import imaplib
import email


def import_kindle_notes(gmail_user, gmail_password, kindle_raw_notes_directory):
    """
    Access unread emails in specified gmail accounts. Find the unseen emails with kindle notes in the subject. Download the csv files containing the kindle notes and save in the raw kindle notes directory.
    """

    c = imaplib.IMAP4_SSL("imap.gmail.com")
    c.login(gmail_user, gmail_password)
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

                fp = open(kindle_raw_notes_directory + '/' + part.get_filename(), 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    # print("\nProcess complete.")