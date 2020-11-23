import datetime
import os
import re
import sys
from matplotlib import pyplot

file_regex=r"First level_\d{2}-\d{2}-\d{4}.txt"

filelist=[file for file in os.listdir(os.getcwd()) if re.match(file_regex, file)]
if len(filelist)==0:
    print("NO VALID FILES FOUND")
    print("PLEASE ENSURE FILES ARE NAMED 'First Level_dd-mm-yyyy.txt'")
    sys.exit()
print(f"Analysing {', '.join(filelist)}")

#this will be a dict in structure of {folder1:{date1:size1, date2:size2...},folder2:{date1:size1, date2:size2...}...}
data_dict={}

for file in filelist:
    date=file.split("_")[1].strip(".txt")
    date=datetime.datetime.strptime(date, "%d-%m-%Y")
    for line in open(file,"r"):
        if line[0]=="G":
            line=line.lstrip("G:\\").rstrip("\n")
            line=line.split()
            department=" ".join(line[:-1])
            size=line[-1].strip("[]")
            #normalises MB and KB to GB
            if size[-2:]=="KB":
                size=float(size[:-2])/1000/1000
            elif size[-2:]=="MB":
                size=float(size[:-2])/1000
            else:
                size=float(size[:-2])
            if department not in data_dict.keys():
                data_dict[department]={}
            data_dict[department][date]=size

#Creates the single graphs, one for each department
for department, data in data_dict.items():
    print(f"Generating Usage Over Time for {department}")
    dates=[d for d in data_dict[department].keys()]
    values=[val for val in data_dict[department].values()]
    pyplot.figure(figsize=(20,10))
    pyplot.title(f"Directory Sizes - {department}")
    pyplot.ylabel("Folder Size (in GB)")
    pyplot.xlabel("Date")
    pyplot.bar(dates,values, width=5)
    for x,y in zip(dates,values):
        pyplot.annotate(f"{y}GB",
        (x,y),
        textcoords="offset points", 
        xytext=(0,10), 
        ha='center')
    pyplot.savefig(f"Space Usage Over Time for {department}")

#Creates combined graph (can only, easilly, make one graph at a time with pyplot)
print("Creating Combined Summary Graph")
pyplot.figure(figsize=(20,10))
max=0
for department, data in data_dict.items():
    dates=[date for date, val in sorted(data_dict[department].items(), key=lambda item: item[0])]
    values=[val for date, val in sorted(data_dict[department].items(), key=lambda item: item[0])]
    for value in values:
        if value>max:
            max=value
    pyplot.plot(dates, values, '-o', label=department)
pyplot.legend(title='title', loc='best', fontsize='x-small')
pyplot.title("Directory Sizes")
pyplot.ylabel("Folder Size (in GB)")
pyplot.xlabel("Date")
pyplot.ylim(0,max+100)
pyplot.savefig("All Folder Sizes Over Time")