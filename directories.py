#!/usr/bin/env python3

# Importing necessary libraries
import pandas as pd
import numpy as np
import os
import sys

# Obtaining the path into the directory form the user:
dir_path=input('Directory path:')

# if dir_path is not a valid path code does not crash but the result is useless

# Executing the tree command for the directory in dir_path and output out.xml
os.system('tree -X '+dir_path+' > out.xml')

# The output is creating in the current directory
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
    lin=lines[i]
    wedge_pos=lin.find('<')
    apo_pos=lin.find('"')
    if apo_pos>=0:
        sub_line=lin[(apo_pos+1):]
        apo_pos2=sub_line.find('"')
        file="'"+sub_line[:apo_pos2]+"'"

        if lin[wedge_pos+1]=='d': dirs[int(wedge_pos/2-1)]=str(fd_count)
        dir_file=lin[wedge_pos+1].upper()#+[dirs[int(wedge_pos/2)-2]]

        empty1=[dir_file]+[dirs[int(wedge_pos/2)-2]]+(['']*(int(wedge_pos/2)-1))
        empty2=['']*(int(w_a/2-wedge_pos/2))
        aux=empty1+[file]+empty2
        new.append(aux)
        fd_count+=1

os.system('rm '+path)

d_frame=pd.DataFrame(np.array(new))
d_frame.rename(columns={0:'type'},inplace=True)

first_two=list([list(d_frame.columns)[0],'mother'])
cols=first_two+(list(d_frame.columns)[1:-1])

d_frame.columns=cols
d_frame.at[0,'mother']='..'

d_frame.to_csv(path[:-3]+'csv', sep=",", index=True)

print(d_frame.head())
