#napravi skriptu koja sa standardnog imputa kao argument prima putanju do nekog foldera
#i onda pretrazi sve fajlove i podfoldere koliko god duboko da ima
#i sacuva putanje do svih fajlova koje nadje, i grupise ih po ekstenziji
#i sacuva to u json fajl
# novi komentar
#3. Zadatak da se vratiš na prethodni commit (iz prvog zadatka) i napraviš tu novu granu justina-dev2.
# I onda tu dodas u kod da se napravi pandas dataframe sa kolonama [file_name, extension, creation_date]
# i da se sortira prvo po kolonama ovim redom [extension, creation_date, name] I da se ispiše dataframe.

import os
import json
import argparse
import random
import shutil
import pandas
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List all the files from the directory recursively and group them by the "
                    "extension")
    parser.add_argument("--dir-path", type=str, default='',
                        help="Path to the directory with the files")
    parser.add_argument("--out-json", type=str, default='',
                       help="Path where to save the json with the file paths")
    parser.add_argument("--rand-files-folder", type=str, default='', help="Path to the directory with rand files")
    args = parser.parse_args()

    if not os.path.exists(args.dir_path):
        print(f'The path {args.dir_path} does not exist!')
        exit(1)

    if not os.path.isdir(args.dir_path):
        print(f'The path {args.dir_path} is not a directory!')
        exit(1)

    if not os.path.exists(args.rand_files_folder):
        print(f'The path {args.rand_files_folder} does not exist')
        exit(1)

    if not os.path.isdir(args.rand_files_folder):
        print(f'The path {args.rand_files_folder} is not directory')
        exit(1)

    dirs_to_inspect = [args.dir_path]
    grouped_files = {}

    while True:
        if len(dirs_to_inspect) == 0:
            # no more directories to look into
            break
        inspected_dirs = []
        for dir_path in dirs_to_inspect:
            files = os.listdir(dir_path) # list files in the directory
            for file_name in files:
                file_path = os.path.join(dir_path, file_name) # create full path
                if os.path.isdir(file_path):
                    # path is directory
                    dirs_to_inspect.append(file_path) # add for inspection later
                else:
                    # path is a file
                    extension = file_name.split('.')[-1] # get extension
                    if extension not in grouped_files: # check whether the key is in the dict
                        grouped_files[extension] = [] # add new key to the dict
                    grouped_files[extension].append(file_path) # add the file path
            inspected_dirs.append(dir_path) # the dir was inspected

        for dir_path in inspected_dirs:
            dirs_to_inspect.remove(dir_path) # remove inspected directory

    # save the json file
    with open(args.out_json, "w") as outfile:
        json.dump(grouped_files, outfile, indent=2)


    list_of_dict = []
    for ext in grouped_files.keys():
        for file_name in grouped_files.get(ext):
            creation_date = time.ctime(os.path.getctime(file_name))
            list_of_dict.append({'file_name':file_name,'extension':ext,'creation_date':creation_date})
    pd = pandas.DataFrame.from_dict(list_of_dict)
    pd.sort_values( by = ["extension", "creation_date", "file_name"],         #rows and column names to sort by
                    axis = 0,           # sort row, axis = 0
                    ascending = [True,True,True])    #for ascending or descending


    print(pd)
