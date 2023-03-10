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

jbeamfilename = jbeamfilename.strip('.jbeam')

def JBeamToJSON(j):
    
    j = re.sub(r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$',
               lambda m: m.group(1) or '', j, flags=re.MULTILINE)
    j = re.sub(r'(\]|})\s*?(\{|\[)', r'\1,\2', j)
    j = re.sub(r'(}|])\s*"', r'\1,"', j)
    j = re.sub(r'"{', r'", {', j)
    j = re.sub(r'"\s+("|\{)', r'",\1', j)
    j = re.sub(r'(false|true)\s+"', r'\1,"', j)
    j = re.sub(r',\s*,', r',', j)
    j = re.sub(r'("[a-zA-Z0-9_]*")\s(\[|[0-9])', r'\1, \2', j)
    j = re.sub(r'(\d\.*\d*)\s*{', r'\1, {', j)
    j = re.sub(r'([0-9]\n)', r'\1,', j)
    j = re.sub(r',\s*?(]|})', r'\1', j)
    j = re.sub(r'(-?[0-9])\s+(-?[0-9])', r'\1,\2', j)
    j = re.sub(r'([0-9])\s*("[a-zA-Z0-9_]*")', r'\1, \2', j)
    j = re.sub(r'("[a-zA-Z0-9_]*")("[a-zA-Z0-9_]*")', r'\1, \2', j)
    j = re.sub(
        r'("[a-zA-Z0-9_]+"):(\s*"[a-zA-Z0-9_]+:)(\n\s*"[a-zA-Z]+")', r'\1:\2",\n\3', j)
    j = re.sub(r':(false|true)("[a-zA-Z_]+")', r':\1, \2', j)
    j = re.sub(r'(["[a-zA-Z_0-9.?]+")\s(\["[a-zA-Z_]+"\]])', r'\1, \2', j)
    j = re.sub(r'("[a-zA-Z0-9]+"):(-?[0-9])\.,\s?"', r'\1:\2.0,"', j)
    if j.endswith(','):
        j = j[:-1]
    if not j.count('{') == j.count('}'):
        j = j[:-1]
    return j

def remove_trailing_commas(json_str,filename):
    lines = json_str.split('\n')
    result_lines = []
    nextlinedelete = False
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if i < len(lines) - 1:
            if ',,' in stripped_line:
                line = line.replace(',,',',')
            if '[,' in stripped_line:
                line = line.replace('[,','[')
            if '{,' in stripped_line:
                line = line.replace('{,','{')
            if ',:' in stripped_line:
                line = line.replace(',:', ':') 
            if ',}' in stripped_line:
                line = line.replace(',}', '}')
            if ',]' in stripped_line:
                line = line.replace(',]', ']')
        if i == len(lines) - 2:
           next_line = lines[i+1]
           if stripped_line.endswith('}'):
              if '}' in next_line and '},' not in next_line: 
               nextlinedelete = True
        if i == len(lines) - 1:
           previous_line = lines[i-1]
           if '}}' in stripped_line:
              line = line.replace('}}', '}')
           if nextlinedelete == True:
              if '}' in stripped_line:
                 line = line.replace('}', ',')  
                 nextlinedelete = False           
                 if line.endswith('],'):
                    line = line.replace('],',']}')


        result_lines.append(line)
    return '\n'.join(result_lines)

def jbeamtojsonfinal(jbeamfilename2,fp):
   with open(fp, "r") as file:
    data2 = file.read()
   formatedfile2 = JBeamToJSON(data2)
   pattern = r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$'
   cinfo = []
   clist = []
   with open(fp, 'r') as f:
       for line_num, line in enumerate(f, 1):
           if re.search(pattern, line):
               cinfo.append('"'+line.strip()+'"')
               cinfo.append(line_num)
               clist.append(cinfo)
               cinfo = []
   with open(jbeamfilename2.strip('.jbeam')+'.json', 'w') as f:
       f.write(JBeamToJSON(formatedfile2))
   with open(jbeamfilename2.strip('.jbeam')+'.json', 'w') as f:
       f.write(remove_trailing_commas(formatedfile2,jbeamfilename2))
   with open(jbeamfilename2.strip('.jbeam')+'.json', 'r+') as f:
       f.write('\n')
       last_line = f.readlines()[-1]
       if last_line == ',':
          f.write('"comments":{')
       else:
          f.write(',"comments":{')
       for i,item in enumerate(clist):
          if i < len(clist)-1 :
             if '"' not in str(item[0]):
                f.write("\n"+"    "+'"'+'commentline'+str(item[1])+'":'+str(item[0])+",")
             else:
                item[0]= item[0].replace('"',"'")
                if item[0].startswith("'") and item[0].endswith("'"):
                    item[0] = item[0][1:-1]       
                    item[0]= item[0].replace('\t',"")        
                f.write("\n"+"    "+'"'+'commentline'+str(item[1])+'":'+'"'+str(item[0])+'"'+",")
          elif i == len(clist)-1:
             if '"' not in str(item[0]):
                f.write("\n"+"    "+'"'+'commentline'+str(item[1])+'":'+str(item[0]))
             else:
                item[0]= item[0].replace('"',"'")
                item[0]= item[0].replace('\t',"")
                if item[0].startswith("'") and item[0].endswith("'"):
                    item[0] = item[0][1:-1]               
                f.write("\n"+"    "+'"'+'commentline'+str(item[1])+'":'+'"'+str(item[0])+'"')
       f.write('\n'+'}')
       f.write('\n'+'}')
    
for file_name in os.listdir(dir_path):
    if file_name.endswith(".jbeam"):
        file_path = os.path.join(dir_path, file_name)
        jbeamtojsonfinal(file_name,file_path)
local_path = os.path.dirname(os.path.abspath(__file__))
goodfiles = 0
failedfiles = 0
for file_name in os.listdir(local_path):
    # Check if the file is a jbeam file
    if file_name.endswith(".json"):
        # Construct the full path to the file
        file_path = os.path.join(local_path, file_name)
        # Call the function to process the jbeam file
        try:
          with open(file_path, 'r') as file:
            json_data = file.read()
          json.loads(json_data)
          goodfiles = goodfiles + 1
        except:
          print(file_name + " is not valid.")
          failedfiles = failedfiles+1

print("Total Valid JSONS: "+str(goodfiles))
print("Total Failed JSONS: "+str(failedfiles))
        