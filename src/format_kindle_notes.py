import pandas as pd
import glob
import os


def extract_title_author(raw_notes_path):
    """
    Extract title and author from header of raw kindle notes csv file.
    """
    with open(raw_notes_path) as file:
        lines = file.readlines()
        # skip ",,,"
        title = lines[1].strip()[:-3].title().strip('"')
        # also skip "by "
        author = lines[2].strip()[3:-3].title().strip('"')
        return title, author


def create_kindle_notes_filename(title):
    """
    Return filename as title of book with "_" as spaces followed by "_notes.csv".

    Example:
    "ego_is_the_enemy_notes.csv"

    """
    return ('_').join(title.lower().split()) + "_notes.csv"


def format_kindle_notes_to_csv(raw_notes_path, formatted_notes_directory):
    """
    Format kindle notes and export to csv file with each row containing data for:

        - Annotation Type
        - Location
        - Starred?
        - Annotation
        - Author
        - Title

    """
    title, author = extract_title_author(raw_notes_path)

    # import notes to df without header
    notes_df = pd.read_csv(raw_notes_path, header=7)

    # add columns for title and author
    notes_df["Author"] = author
    notes_df["Title"] = title

    formatted_notes_path = formatted_notes_directory + create_kindle_notes_filename(title)
    notes_df.to_csv(formatted_notes_path, index=False)


def archive_raw_kindle_notes(raw_notes_path, kindle_raw_notes_archive_directory):
    """
    Move raw kindle notes from raw directory to raw/archive directory.
    """
    raw_notes_archive_path = raw_notes_path.replace(os.path.dirname(raw_notes_path), kindle_raw_notes_archive_directory)
    os.rename(raw_notes_path, raw_notes_archive_path)


def format_kindle_notes(kindle_raw_notes_directory, kindle_formatted_notes_directory, kindle_raw_notes_archive_directory):
    """
    Grab list of raw kindle notes files. Format the raw kindle notes and export formatted notes to formatted notes directory. Move raw kindle notes to raw archive directory.
    """

    # grab list of raw kindle notes files
    raw_notes_paths = glob.glob(kindle_raw_notes_directory+'/*.csv')

    for raw_notes_path in raw_notes_paths:
        format_kindle_notes_to_csv(raw_notes_path, kindle_formatted_notes_directory)
        archive_raw_kindle_notes(raw_notes_path, kindle_raw_notes_archive_directory)
