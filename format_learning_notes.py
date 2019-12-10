"""

Script to format raw learning notes html file in the data/apple_notes/raw directory and export formatted learning notes csv file to the data/apple_notes directory.

"""
import re

from config import APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORYAPPLE_NOTES_FORMATTED_NOTES_DIRECTORY


def remove_html_tags_extraneous_whitespaces(line):
    """
    Remove html tags and extraneous whitespace chars from line.
    """
    line = re.sub('<[^<]+?>', '',line).strip()
    return line


def format_learning_notes_to_csv(html_file, csv_file):
    """
    Format learning notes and export to csv file with each row containing data for:

        - Author
        - Title
        - Annotation
        - Date

    """
    # add header to csv file
    csv_file.write("Author,Title,Annotation,Date\n")

    for idx, line in enumerate(html_file):

        line = remove_html_tags_extraneous_whitespaces(line)

        # skip empty lines
        if line:
            # reset author and title after divider
            if "==========" in line:
                div_idx = idx
                author = None
                title = None
            # store author and title data
            # "" to ensure commas in data ok with csv format
            elif idx == div_idx + 1:
                author = '"' + line + '"'
            elif idx == div_idx + 2:
                title = '"' + line + '"'
            # write author, title, annotation, and date data to csv file
            else:
                try:
                    # extract date
                    date = re.search("(\d+/\d+/\d+)", line).group(1)
                    line = line.strip("(" + date + ")").strip()
                    csv_file.write(','.join([author, title, '"' + line + '"', '"' + date + '"']))
                except:
                    csv_file.write(','.join([author, title, '"' + line + '"']))
                csv_file.write('\n')
    csv_file.close()
    html_file.close()


if __name__ == "__main__":

    html_file = open(APPLE_NOTES_RAW_LEARNING_NOTES_DIRECTORY+'/learning_notes.html', 'r', encoding="ISO-8859-1")
    csv_file = open(APPLE_NOTES_FORMATTED_NOTES_DIRECTORY+'/learning_notes.csv', 'w')

    format_learning_notes_to_csv(html_file, csv_file)
