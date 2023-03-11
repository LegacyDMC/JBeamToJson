import json
import tkinter as tk
from tkinter import filedialog
import re
import os

def glbgetpath():                
 root = tk.Tk()
 root.withdraw()
 
 filepath = filedialog.askdirectory()
 return str(filepath)
def glbgetfpath():                
 root = tk.Tk()
 root.withdraw()
 
 filepath2 = filedialog.askopenfilename()
 return str(filepath2)


def getbeampath():
 file = glbgetfpath()
 filename = os.path.basename(file)
 vector = [file,filename]
 return(vector)

fileinfo = getbeampath()
jbeamfilepath = fileinfo[0]
jbeamfilename = fileinfo[1]
dir_path = jbeamfilepath.strip(jbeamfilename)

jbeamfilename = jbeamfilename.strip('.json')

def JSONToJBeam(j):
    return j
def jsontojbeamfinal(json_filename, fp):
    with open(fp, "r") as file:
        data = file.read()
    formatted_file = JSONToJBeam(data)
    with open(json_filename.strip('.json')+'converted'+'.jbeam', 'w') as f:
        f.write(formatted_file)
    
local_path = os.path.dirname(os.path.abspath(__file__))

for file_name in os.listdir(local_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(local_path, file_name)
        try:
          with open(file_path, 'r') as file:
            json_data = file.read()
          json.loads(json_data)
          jsontojbeamfinal(file_name,file_path)
        except:
          print(file_name + " is not valid, please fix it before converting back to JBeam.")