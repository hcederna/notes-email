import glob
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import gmail_user, gmail_password, recipient_email


# send this number of notes in email
NUM_NOTES = 5

# store formatted kindle notes in this directory
KINDLE_FORMATTED_NOTES_DIRECTORY = "data/kindle/"

# store formatted learning notes in this directory
APPLE_NOTES_FORMATTED_NOTES_DIRECTORY = "data/apple_notes"


def assemble_html_body_of_email(notes_df):
    """
    Assemble body of email from data in notes DataFrame.

    Format:

        ============================================

        {annotation}

        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        {title} | {author} | Annotated on {date}

    """

    body = """\
    <html>
      <head></head>
      <body>
    """

    for idx, row in notes_df.iterrows():

        annotation = row['Annotation']
        citation = f"{row['Title']} | {row['Author']} | Annotated on {row['Date']}"

        body = body + f"""\
        <p>
          <hr style="border: 5px solid grey">
          <br>
          {annotation}
          <br>
          <br>
          <hr style="border: 1px dashed grey">
          <blockquote><i>{citation}</i></blockquote>
        </p>
        """

    body += f"""\
      <hr style="border: 5px solid grey">
      </body>
    </html>
    """

    return(body)


if __name__ == "__main__":

    # grab list of formatted kindle and apple notes file paths
    kindle_notes_paths = glob.glob(KINDLE_FORMATTED_NOTES_DIRECTORY+'/*.csv')
    apple_notes_paths = glob.glob(APPLE_NOTES_FORMATTED_NOTES_DIRECTORY+'/*.csv')
    notes_paths = kindle_notes_paths + apple_notes_paths

    # concatenate formatted notes into DataFrame
    notes_dfs = [pd.read_csv(notes_path) for notes_path in notes_paths]
    notes = pd.concat(notes_dfs, sort=False)

    # select random sample of notes
    notes_df = notes.sample(NUM_NOTES)

    # prepare and send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Notes Digest"
    msg['From'] = gmail_user
    msg['To'] = recipient_email

    body = assemble_html_body_of_email(notes_df)
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, recipient_email, msg.as_string())
    server.quit()