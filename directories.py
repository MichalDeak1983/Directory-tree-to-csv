#!/usr/bin/env python3

# Importing necessary libraries
import pandas as pd
import numpy as np
import os

# Obtaining the path into the directory form the user:
dir_path=input('Directory path:')

# if dir_path is not a valid path code does not crash but the result is useless

# Executing the tree command for the directory in dir_path and output out.xml
os.system('tree -X '+dir_path+' > out.xml')

# The output is createdin the current directory
# The path to the output:
path='./out.xml'

# Reading the output into a file:
with open(path) as f:
    lines = f.readlines()

# Next loop determines the depth of the directory tree by going through the xml file:
w_a=0
for i in range(2,len(lines)):
    lin=lines[i]
    w_p=lin.find('<')
    if w_p>w_a: w_a=w_p

# Setting up auxiliary variables:
# new is a list to store rows of the dataframe
new=[]
# dirs stores the mother directories
dirs=['']*int(w_a/2+1)
# fd_count counts number of files/directories
fd_count=0
# Number of lines in  the xml file:
num_lines=len(lines)

# Main loop running over the lines in the xml file:
for i in range(2,num_lines):
# Storing a line in a variable
    lin=lines[i]
# Find the position of the < symbol
    wedge_pos=lin.find('<')
# FInd the position of " symbol
    apo_pos=lin.find('"')
# If there is a " in lin apo_pos is bigger or equal to 0
# othewise the line does not contain information about a file/directory
    if apo_pos>=0:
# Taking the substring from the lin containing "s
        sub_line=lin[(apo_pos+1):]
# Locating the second "
        apo_pos2=sub_line.find('"')
# Now we have the name of the file/directory
        file="'"+sub_line[:apo_pos2]+"'"
# If file is a directory we keep its position for keeping the mother information:
        if lin[wedge_pos+1]=='d': dirs[int(wedge_pos/2-1)]=str(fd_count)
# Information about type of the file/directory/link:
        dir_file=lin[wedge_pos+1].upper()#+[dirs[int(wedge_pos/2)-2]]
# Strings containing parts of line record:
        empty1=[dir_file]+[dirs[int(wedge_pos/2)-2]]+(['']*(int(wedge_pos/2)-1))
        empty2=['']*(int(w_a/2-wedge_pos/2))
        aux=empty1+[file]+empty2
# Storing the list in a list of lists new
        new.append(aux)
# counting the fiels/directories/links
        fd_count+=1

# Removing the xml output
os.system('rm '+path)

# Creating the data frame where we store the tree structure:
d_frame=pd.DataFrame(np.array(new))
# Renaming a column
d_frame.rename(columns={0:'type'},inplace=True)

# Renaming and rearanging columns
first_two=list([list(d_frame.columns)[0],'mother'])
cols=first_two+(list(d_frame.columns)[1:-1])

d_frame.columns=cols
# Setting last empty value
d_frame.at[0,'mother']='..'

# Exporting the data frame into csv file:
d_frame.to_csv(path[:-3]+'csv', sep=",", index=True)

# Printing out a part of the data frame:
print(d_frame.head())
