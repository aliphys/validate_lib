import argparse
import os
#prevents look behind requires fixed width pattern error
#import regex as re
import re
import subprocess
import csv
import pkg_resources
from io import StringIO

__version__ = '0.dev'

def arduinoKeywords():
    data_stream = pkg_resources.resource_stream(__name__, 'arduino_keywords.csv')
    data_text = data_stream.read().decode('utf-8')
    data_file = StringIO(data_text)
    reader = csv.reader(data_file)
    keywords = []
    # iterate over the rows in the CSV
    for row in reader:
        keywords.append(row)
    return keywords

# read the library.properties file. Location of the file is assumed to be in the same directory as the script
def read_library_properties():
    try:
        with open('library.properties', 'r') as file:
            return file.read()
    except Exception as e:
        print(e)

# Rule 01: determine the C++ version based on the library properties
def determine_cpp_version(library_properties):
    try:
        if "architectures=\\*" in library_properties:
            print("✅ Supported architecture compliant with up to C++11")
            return "C++11"
        elif "renesas_portenta" in library_properties:
            print("✅ Supported architecture compliant with up to C++17")
            return "C++17"
        elif "mbed_opta" in library_properties:
            print("✅ Supported architecture compliant with up to C++14")
            return "C++14"
        elif "mbed_portenta" in library_properties:
            print("✅ Supported architecture compliant with up to C++14")
            return "C++14"
        else:
            raise Exception(f"❌Rule 01 Error: The architecture is not specified.")
    except Exception as e:
        print(e)

# Rule 01: check for illegal #define statements
def check_rogue_define_statements():
    keywords = arduinoKeywords()
    found_bad_words = False  # Flag to track if any Arduino reserved keywords are found
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ino'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    try:
                        matches = re.findall(r"(?<=\W)#define\s+(\w+)", content)
                        for match in matches:
                            if match in keywords:
                                found_bad_words = True  # Set the flag if any Arduino reserved keywords are found
                                line_number = content[:content.find(match)].count('\n') + 1
                                raise Exception(f"❌Rule 01 Error: Found an illegal #define statement in {file_path} at line {line_number}")
                    except Exception as e:
                        print(e)
    if not found_bad_words:
        print("✅ #define statements do not overwrite Arduino keywords")


# Rule 02: Check if the line length is less than 120 characters
def check_line_length():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ino'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    line_length_over = False
                    for line_number, line in enumerate(f, start=1):
                        if len(line) > 120:
                            line_length_over = True
                            print(f"❌Rule 02 Error: Line {line_number} in file {file_path} exceeds 120 characters:")
                    if not line_length_over:
                        print(f"✅ All lines in {file_path} are less than 120 characters.")

# Rule 03: Correct brace wrapping
def check_brace_wrapping():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ino'):
                file_path = os.path.join(root, file)
                brace_wrapping_broken = False
                #TODO Fix the style options so that it only affects the brace wrapping
                style_options = '{BraceWrapping: {AfterClass: false, AfterControlStatement: false, AfterEnum: false, AfterFunction: false, AfterNamespace: false, AfterStruct: false, AfterUnion: false, AfterExternBlock: false, BeforeCatch: false, BeforeElse: false, IndentBraces: false}, AllowShortBlocksOnASingleLine: true, AllowShortIfStatementsOnASingleLine: true, AllowShortLoopsOnASingleLine: true, CommentPragmas: "/\*(.+\n.+)+\*/", ReflowComments: false}'
                result = subprocess.run(['clang-format', f'-style={style_options}', file_path], capture_output=True, text=True)
                try:
                    if result.stdout != open(file_path).read():
                        brace_wrapping_broken = True
                        raise Exception(f"❌Rule 03 Error: File {file_path} does not not have correct brace wrapping.")
                except Exception as e:
                    print(e)
                if not brace_wrapping_broken:
                    print("✅ All braces are good.")

        

# Rule 05: Check if there are any casts without a comment
def check_cast_comments():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ino'):
                file_path = os.path.join(root, file)
                cast_comments_present = True  # Variable to track if there are missing cast comments
                with open(file_path, 'r') as f:
                    content = f.read()
                    try:
                        #TODO emumerate() to get the line number
                        if re.search(r"(static_cast<.*?>|reinterpret_cast<.*?>|\(.*?\)).*(?<!//.*)", content):
                            cast_comments_present = False  # Set the variable to False if a cast without a comment is found
                            raise Exception(f"❌Rule 05 Error: Found a cast without a comment in {file_path}")
                    except Exception as e:
                        print(e)
                if cast_comments_present:
                    print("✅ All casts have comments.")

# Rule 07: Check if protected keywords are used
def check_variable_initialization():
    with open('arduino_keywords.csv', 'r') as csv_file:
        keywords = set(row[0] for row in csv.reader(csv_file))
    found_bad_words = False  # Flag to track if any Arduino reserved keywords are found
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ino'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    try:
                        matches = re.findall(r"(?<!//\s*)\b(\w+)\b\s*=", content)
                        for match in matches:
                            if match in keywords:
                                found_bad_words = True  # Set the flag if any Arduino reserved keywords are found
                                line_number = content[:content.find(match)].count('\n') + 1
                                raise Exception(f"❌Rule 07 Error: Found an initialized variable that matches an Arduino keyword in {file_path} at line {line_number}")
                    except Exception as e:
                        print(e)
    if not found_bad_words:
        print("✅ No initialized variables match Arduino keywords")


def check_general_rules():
    library_properties = read_library_properties()
    cpp_version = determine_cpp_version(library_properties)
    print(f"C++ Version is {cpp_version}")
    check_line_length()
    check_cast_comments()
    check_rogue_define_statements()
    check_brace_wrapping()


def check_file_exists(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"Error: {file_path} not found.")
    except Exception as e:
        print(e)

def check_string_in_file(file_path, string):
    with open(file_path, 'r') as file:
        contents = file.read()
        try:
            if string not in contents:
                raise Exception(f"Error: {string} not found in {file_path}")
        except Exception as e:
            print(e)

def check_comment_rules():
    # Check for Main README.md
    check_file_exists('README.md')

    # Check for docs/README.md
    check_file_exists('docs/README.md')

    # Check for docs/assets folder and docs/api.md
    check_file_exists('docs/assets')
    check_file_exists('docs/api.md')

    # Check String in Main README.md
    check_string_in_file('README.md', '📖 For more information about this library please read the documentation [here](./docs/)')

    # Check Headers in docs/README.md
    check_string_in_file('docs/README.md', '# Features')
    check_string_in_file('docs/README.md', '# Usage')
    check_string_in_file('docs/README.md', '# API')
    check_string_in_file('docs/README.md', '# License')


def main():
    parser = argparse.ArgumentParser(description='Select check.')
    parser.add_argument('--general-rules', dest='check_general_rules', action='store_true',
                    help='run the hello_world function')
    parser.add_argument('--comment-rules', dest='check_comment_rules', action='store_true',
                    help='run the hello_world function')
    
    args = parser.parse_args()

    if args.check_general_rules:
        check_general_rules()
    elif args.check_comment_rules:
        check_comment_rules()


if __name__ == "__main__":
    main()