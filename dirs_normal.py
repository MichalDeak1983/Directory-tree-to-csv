#!/usr/bin/env python3

# Python script to get from Table 2 to Table 1

# Importing necessary libraries
import pandas as pd
import numpy as np

# Read the directories.py output csv
d_frame=read_csv("./out.csv",sep=",",index=True)

# Filter for directories and files and store in new dataframes
dirs=d_frame[d_frame['type']=='D']
files=d_frame[d_frame['type']=='F']

# Copy only the part of the files dataframe with numeric columns
d_frame_files=files[[i for i in range(1,files.shape[1]-1)]]
# Sum the columns of d_frame_files to get one column
d_frame_files=pd.DataFrame(d_frame_files.sum(axis=1))
# Add a column with mother information
d_frame_files.insert(0,'mother',files['mother'],True)

# Copy only the part of the dirs dataframe with numeric columns
d_frame_dirs=dirs[[i for i in range(1,dirs.shape[1]-1)]]
# Sum the columns of d_frame_dirs to get one column
d_frame_dirs=pd.DataFrame(d_frame_dirs.sum(axis=1))
# Add a column with mother information
d_frame_dirs.insert(0,'mother',dirs['mother'],True)

# We store the paths in list paths
paths=[]
# Loop over files row to extract the path information 
for i in range(0,d_frame_files.shape[0]):
# Get the mother index from d_frame_files
    mother_index=d_frame_files.iloc[i,0]
# Add the directory to the path
    file_path=d_frame_dirs.loc[int(mother_index),0]
# Loop over mother_index
    while int(mother_index)>0:
# Get the mother_index from d_frame_dirs
        mother_index=d_frame_dirs.loc[int(mother_index),'mother']
# Add the directory to the path
        file_path=d_frame_dirs.loc[int(mother_index),0]+'/'+file_path
# Store the path for the file in paths and remove 's
    paths.append(''.join([x for x in file_path if x!="'"]))

# New dataframe with the normal tree structure
df_tree=pd.DataFrame({'path':paths,'file':list(d_frame_files[0])})

# Print part of the dataframe
print(df_tree[:60])

