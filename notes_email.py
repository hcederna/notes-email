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
from config import RECIPIENT_EMAIL, NUM_NOTES


dir_path = os.path.dirname(os.path.realpath(__file__))
KINDLE_RAW_NOTES_DIRECTORY = dir_path + "/data/kindle/raw"
KINDLE_FORMATTED_NOTES_DIRECTORY = dir_path + "/data/kindle/"
KINDLE_RAW_NOTES_ARCHIVE_DIRECTORY = dir_path + "/data/kindle/raw/archive"
APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORY = dir_path + "/data/apple_notes/raw"
APPLE_NOTES_FORMATTED_NOTES_DIRECTORY = dir_path + "/data/apple_notes"


import_kindle_notes(GMAIL_USER, GMAIL_PASSWORD, KINDLE_RAW_NOTES_DIRECTORY)
format_kindle_notes(KINDLE_RAW_NOTES_DIRECTORY, KINDLE_FORMATTED_NOTES_DIRECTORY, KINDLE_RAW_NOTES_ARCHIVE_DIRECTORY)

# run import learning notes applescript
os.system("osascript " + dir_path + "/src/import_learning_notes.scpt")
format_learning_notes(APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORY, APPLE_NOTES_FORMATTED_NOTES_DIRECTORY)

send_email(GMAIL_USER, GMAIL_PASSWORD, RECIPIENT_EMAIL, NUM_NOTES, KINDLE_FORMATTED_NOTES_DIRECTORY, APPLE_NOTES_FORMATTED_NOTES_DIRECTORY)