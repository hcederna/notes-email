import re


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

        # skip title and empty lines
        if idx > 0 and line:
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


def format_learning_notes(apple_notes_raw_learning_notes_directory, apple_notes_formatted_notes_directory):
    """
    Extract data from raw apple notes html file and save formatted apple notes as a csv file in formatted notes directory.
    """
    html_file = open(apple_notes_raw_learning_notes_directory+'/learning_notes.html', 'r', encoding="ISO-8859-1")
    csv_file = open(apple_notes_formatted_notes_directory+'/learning_notes.csv', 'w')

    format_learning_notes_to_csv(html_file, csv_file)
