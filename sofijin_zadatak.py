#napravi skriptu koja sa standardnog imputa kao argument prima putanju do nekog foldera
#i onda pretrazi sve fajlove i podfoldere koliko god duboko da ima
#i sacuva putanje do svih fajlova koje nadje, i grupise ih po ekstenziji
#i sacuva to u json fajl
import os,json

print("Unesite putanju do foldera za pretrazivanje")
input_folder = input()
os.chdir(input_folder)
mydic={}

for file in os.listdir(input_folder):
    ext = file.split(".")
    current_key_item = mydic.get(ext[-1])
    if (current_key_item == None):
        mydic[ext[-1]] = [file]
    else:
        list_of_files = []
        for files in current_key_item:
            list_of_files.append(files)
        list_of_files.append(file)
        mydic[ext[-1]] = list_of_files

# Serializing json
json_object = json.dumps(mydic, indent=4)
 
# Writing to json file
with open("zadatak1.json", "w") as outfile:
    outfile.write(json_object)
