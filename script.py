import zipfile
import os
from glob import glob
import sys
import re


C: int = len(sys.argv)

if C == 1:
    print("Specify Path to Home directory of files to compress")
    print("eg if this directory: python script.py .")
    
    path: str = "."

elif C == 2:
    path: str = sys.argv[1]

else:
    print("Usage: python script.py path_to_root")
    sys.exit(1)

os.chdir(path)

try:
    with open(".scriptignore", "r") as file:
        # getting all patterns from scriptignore
        lines = map(lambda x: x.strip(), file.readlines())

        patterns: list[str] = [line for line in lines if line]  # patterns

        to_ignore: set = set()  # all files/folders that match patterns in scriptignore
        for pattern in patterns:
            matches = glob(pattern, include_hidden=True)
            to_ignore.update(matches) 

        #compressed file
        compressed = zipfile.ZipFile("project.zip", "w")
        
        for i,(folder, subfolder, filename) in enumerate(os.walk(".")):
           
            if i != 0: #dont want a . folder among compressed
                if folder in to_ignore:
                    continue
                
                #for folders that in directory
                #get the first subdirectory with regex and see if in scriptignore

                folder_name = re.search(r"\.\\(\.?\w+)\.?(\w)*\\*", folder).group(1)

                if folder_name in to_ignore:
                    continue
                compressed.write(folder)

            for file in filename:
                if file in to_ignore or filename[-4:] == ".zip":
                    continue
                compressed.write(os.path.join(folder, file))
        
        compressed.close()

except FileNotFoundError:
    print(".scriptignore file not found")
    sys.exit(0)
