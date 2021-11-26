import json
from os import listdir
from os.path import isfile, join


def merge_JsonFiles(filename, outfile):
    for f1 in filename:
        with open(f1, 'r') as infile:
            result = json.load(infile)
            with open(outfile, 'ab+') as f:
                f.seek(0, 2)  # Go to the end of file
                if f.tell() == 0:  # Check if file is empty
                    # If empty, write an array
                    f.write(json.dumps(result).encode())
                else:
                    f.seek(-1, 2)
                    f.truncate()  # Remove the last character, open the array
                    f.write(' , '.encode())  # Write the separator
                    # Dump the dictionary and remove the first and last character of the input (i.e. "[" and "]")
                    f.write(json.dumps(result)[1:-1].encode())
                    f.write(']'.encode())


IN_PARTIAL_JSON_PATH = './Partials/Outputs'
FINAL_JSON_FILE = './Outputs/final_giveaways.json'

partial_files = [IN_PARTIAL_JSON_PATH+'/'+f for f in listdir(IN_PARTIAL_JSON_PATH) if isfile(
    join(IN_PARTIAL_JSON_PATH, f))]


print(partial_files)
merge_JsonFiles(partial_files, FINAL_JSON_FILE)
