#napravi skriptu koja sa standardnog imputa kao argument prima putanju do nekog foldera
#i onda pretrazi sve fajlove i podfoldere koliko god duboko da ima
#i sacuva putanje do svih fajlova koje nadje, i grupise ih po ekstenziji
#i sacuva to u json fajl
# novi komentar
import os
import json
import argparse
import random
import shutil

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

    #print(type(grouped_files['doc']))
    random_file = ''
    only_file_name = ''
    for ext in grouped_files.keys():
        random_file = random.choice(grouped_files.get(ext)) #get random file from specific key
        file_path = os.path.join(args.rand_files_folder, random_file.split("\\")[-1]) #join file name of random file and path to new folder
        shutil.copy(random_file,file_path)


