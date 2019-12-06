import pandas as pd


# store formatted kindle notes in this directory
KINDLE_FORMATTED_NOTES_DIRECTORY = "data/kindle/"


def extract_title_author(raw_notes_path):
    """
    Extract title and author from header of raw kindle notes csv file.
    """
    with open(raw_notes_path) as file:
        lines = file.readlines()
        # skip ",,,"
        title = lines[1].strip()[:-3].title()
        # also skip "by "
        author = lines[2].strip()[3:-3].title()
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


format_kindle_notes_to_csv("Ego Is the Enemy-Notebook - Ego Is the Enemy-Notebook.csv", KINDLE_FORMATTED_NOTES_DIRECTORY)

# # check results...
# pd.read_csv("data/kindle/ego_is_the_enemy_notes.csv").sample(5)