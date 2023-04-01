"""
Script that helps in the process of checking grammar
and spelling checks of latex files by removing
all latex specific items and only printing out the
text.
Note that you will have to manually check all
special elements such as figures, tables, enumerations etc.

Titles will be preserved!

Latex specific thigns like references etc. will not be checked

Call the script from the command line with the following arguments:
    python3 latex_to_txt.py <path-to-tex> <desired-out-path>

The desired-out-path determines the location for the resulting txt file
"""
import os
import re
import sys


def read_file(path):
    """
    Internal helper file that reads in the latex file
    It will drop all special elements that start with "\begin{"
    @parameters
        path (str): path to the tex file
    @returns:
        data (list): every line of the tex file is on item in the list
    """
    # Check if the file exists
    if not os.path.isfile(path):
        print(f"Filepath given: {path}")
        raise FileNotFoundError()

    # placeholder for the contet
    content = []
    # special flag that is used for ignoring special elements
    special_flag = True

    with open(path, mode="r", encoding="utf-8") as in_file:
        for line in in_file:
            # Skip comments
            if line.startswith("%"):
                continue

            # Check if a previously started figure/table etc. has ended
            if special_flag:
                if line.startswith("\\end{"):
                    special_flag = False
                continue

            # Check if a figure/table etc. starts
            # Note that all special items like equations, figures, enumerates etc.
            # will be skipped until the expression \end{ is found
            if line.startswith("\\begin{"):
                special_flag = True
                continue

            # save the content but drop all newline indicators
            content.append(line.replace("\n", ""))

    return content


def drop_expression(expression, replacer, data):
    """
    Internal helper function that substitutes a given expression
    @parameters:
        expression (str): the expression to match
        replacer (str): the replacing string/content
        data (list): the data list containing all the tex content
    @returns:
        list containing all the filtered tex content
    """
    return [line.replace(expression, replacer) for line in data]


def main(file_path, out_path):
    """
    Main entry point of the script
    @parameter:
        file_path (str): path to the tex file
        out_path (str): path to the desired location for the output txt file
    """
    # read the tex file in
    # while reading the file in all comments, tables, graphics etc.
    # will be already skipped
    data = read_file(file_path)

    # all the other expressions to remove
    expressions = [
        "\\ac{",
        "\\acs{",
        "\\enquote{",
        "\\chapter{",
        "\\section{",
        "\\subsection{",
        "}", # this is important to remove remaining open brackets
        "$"
    ]

    # replace references and labels
    data = [re.sub(r"\\ref{.*}", "<Referenz entfernt>", line) for line in data]
    data = [re.sub(r"\\label{.*}", "", line) for line in data]

    # replace cite and footnotes
    data = [re.sub(r"\\footcite\[.*\]{.*}", "", line) for line in data]
    data = [re.sub(r"\\footnotetext{.*}", "", line) for line in data]
    data = [re.sub(r"\\footnote{.*}", "", line) for line in data]
    data = [re.sub(r"\\cite{.*}", "", line) for line in data]
    data = [re.sub(r"\\cite\[.*\]{.*}", "", line) for line in data]

    # drop all other expressions
    for expression in expressions:
        data = drop_expression(expression, "", data)

    # save the file
    with open(out_path, mode="w", encoding="utf-8") as out_file:
        for line in data:
            out_file.write(line)
            out_file.write("\n")

if __name__ == "__main__":
    try:
        TEX_PATH = sys.argv[1]
    except KeyError as key_error:
        print("Missing path to file as first argument!")
        raise key_error

    try:
        txt_out_path = sys.argv[2]
    except KeyError as key_error:
        print("Missing saving path to file as second argument!")
        raise key_error

    main(TEX_PATH, txt_out_path)
