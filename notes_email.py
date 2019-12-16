import imaplib
import email
import pandas as pd
import glob
import os
import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.import_kindle_notes import import_kindle_notes
from src.format_kindle_notes import format_kindle_notes
from src.format_learning_notes import format_learning_notes
from src.send_email import send_email

from config import GMAIL_USER, GMAIL_PASSWORD
from config import KINDLE_RAW_NOTES_DIRECTORY, KINDLE_FORMATTED_NOTES_DIRECTORY, KINDLE_RAW_NOTES_ARCHIVE_DIRECTORY
from config import APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORY, APPLE_NOTES_FORMATTED_NOTES_DIRECTORY
from config import RECIPIENT_EMAIL, NUM_NOTES



import_kindle_notes(GMAIL_USER, GMAIL_PASSWORD, KINDLE_RAW_NOTES_ARCHIVE_DIRECTORY)
format_kindle_notes(KINDLE_RAW_NOTES_DIRECTORY, KINDLE_FORMATTED_NOTES_DIRECTORY, KINDLE_RAW_NOTES_ARCHIVE_DIRECTORY)

# run import learning notes applescript
os.system("osascript /Users/hcederna/Desktop/notes-email/src/import_learning_notes.scpt")
format_learning_notes(APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORY, APPLE_NOTES_FORMATTED_NOTES_DIRECTORY)

send_email(GMAIL_USER, GMAIL_PASSWORD, RECIPIENT_EMAIL, NUM_NOTES, KINDLE_FORMATTED_NOTES_DIRECTORY, APPLE_NOTES_FORMATTED_NOTES_DIRECTORY)