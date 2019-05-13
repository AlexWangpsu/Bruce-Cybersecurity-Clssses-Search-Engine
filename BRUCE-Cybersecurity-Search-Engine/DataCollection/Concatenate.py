import pandas as pd
import glob
import os

#Ths script is to concatenate all csv under the same folder

path =r'/Users/andywang/Desktop/course' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f,header = None,error_bad_lines=False,encoding='utf-8') for f in all_files)
#concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
list1 = []

for i in df_from_each_file:

	for j in range(len(i)):
		if i[0][j] == 'colummn' or i[0][j] == 'URL':
			continue
		print(j)
		list1.append(i[0][j])

	print(i)

df = pd.DataFrame(list1, columns=["URL"])
df.to_csv('10courses.csv', index=False)
while i <len(df):
	