"""
LICENSE: MIT
> https://github.com/art-r/tex-to-txt

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
import argparse
import os
import re


def read_file(path):
    """
    Internal helper file that reads in the latex file.
    It will drop all special elements that start with "\\begin{".

    :param path: path to the tex file
    :type path: str

    :return: every line of the tex file is on item in the list
    :rtype: list[str]
    """
    # Check if the file exists
    if not os.path.isfile(path):
        print(f"Filepath given: {path}")
        raise FileNotFoundError()

    # placeholder for the contet
    content = []
    # special flag that is used for ignoring special elements
    special_flag = False

    with open(path, mode="r", encoding="utf-8") as in_file:
        for line in in_file.readlines():
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


def define_expressions(args):
    """
    Loads the defined expressions.

    :param args: contains variables tex_path, out_path, expressions, additional
    :var str args.tex_path:  path to the tex file
    :var str args.out_path: path to the desired location for the output txt file
    :var str args.expressions: path to a txt file containing additional expressions
    :var bool args.additional: whether or not the expressions provided in the expressions file should be used as
        additional or as the only expressions
    """
    # load defaults
    try:
        with open('./defaults.txt', 'r') as reader:
            defaults = [line.rstrip('\n') for line in reader.readlines()]
    except FileNotFoundError as fnf:
        print(f"An error occurred: {str(fnf)}")

    # use only defaults
    if args.expressions == 'default':
        return defaults

    # expressions file does not exist
    if not os.path.isfile(args.expressions):
        raise FileNotFoundError

    # loads additional expressions
    with open(args.expressions, 'r') as reader:
        # as additionals
        if args.additional:
            return [line for line in reader.readlines()] + defaults
        # as all expressions used
        else:
            return [line for line in reader.readlines()] + ["}"]


def drop_expression(expression, replacer, data):
    """
    Internal helper function that substitutes a given expression

    :param str expression: the expression to match
    :param str replacer: the replacing string/content
    :param list data: the data list containing all the tex content

    :returns list: list containing all the filtered tex content

    """
    return [line.replace(expression, replacer) for line in data]


def main(args):
    """
    Main entry point of the script

    :param args: contains variables tex_path, out_path, expressions, additional
    :var str args.tex_path:  path to the tex file
    :var str args.out_path: path to the desired location for the output txt file
    :var str args.expressions: path to a txt file containing additional expressions
    :var bool args.additional: whether or not the expressions provided in the expressions file should be used as
        additional or as the only expressions
    """
    # read the tex file in
    # while reading the file in all comments, tables, graphics etc.
    # will be already skipped
    if not os.path.isfile(args.tex_path):
        raise FileNotFoundError

    data = read_file(args.tex_path)

    # all the other expressions to remove
    expressions = define_expressions(args)

    # replace cite and footnotes
    data = [re.sub(r"\\footcite\[.*?\]{.*?}", "", line) for line in data]
    data = [re.sub(r"\\footnotetext{.*?}", "", line) for line in data]
    data = [re.sub(r"\\footnote{.*?}", "", line) for line in data]
    data = [re.sub(r"\\cite{.*?}", "", line) for line in data]
    data = [re.sub(r"\\cite\[.*?\]{.*?}", "", line) for line in data]
    data = [re.sub(r"\\input{.*?}", "", line) for line in data]

    # replace references and labels
    data = [re.sub(r"\\ref{.*}", "<Referenz entfernt>", line) for line in data]
    data = [re.sub(r"\\label{.*}", "", line) for line in data]

    # drop all other expressions
    for expression in expressions:
        data = drop_expression(expression, "", data)

    # if the directory to the save file does not exist, it is created
    if not os.path.exists(os.path.dirname(args.out_path)):
        os.makedirs(os.path.dirname(args.out_path))
    # save the file
    with open(args.out_path, mode="w", encoding="utf-8") as out_file:
        for line in data:
            out_file.write(line)
            out_file.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_path', help='the path to the tex file')
    parser.add_argument('out_path', help='path to the ouput text file')
    parser.add_argument('-e', '--expressions', dest='expressions', help='path containing expressions',
                        default='default')
    parser.add_argument('-a', '--additional', dest='additional',
                        help='use the provided file in addition to the default expressions', action='store_true')

    main(parser.parse_args())
