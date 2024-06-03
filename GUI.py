import streamlit as st
import pandas as pd

import tarfile
import os 
from os import listdir 
import tempfile 
import subprocess 

#from oct2py import Oct2Py

import matplotlib.pyplot as plt
from io import BytesIO

import requests


rf_image_url = 'https://github.com/hikarukuro1211/GUI/blob/main/rf_image.txt'


st.title('Data Visualizer')
st.sidebar.subheader('Upload a file')

uploaded_file = st.sidebar.file_uploader("Upload a file", type = "tar")

if uploaded_file is not None:  
	#tar = tarfile.open("prac.tar")
	bytes_data = uploaded_file.getvalue()
	with tarfile.open(fileobj = BytesIO(bytes_data)) as tf:
		for entry in tf:
			if entry.name.endswith('.lzo') and "rf" in entry.name:
				st.write(entry.name)
				extract = tf.extractfile(entry)
				with tempfile.NamedTemporaryFile(delete=False, suffix='.lzo') as temp_lzo:
					temp_lzo.write(extract.read())
					temp_lzo_path = temp_lzo.name
					temp_dir = os.path.dirname(temp_lzo_path)

					st.write(temp_lzo_path)
				# Save the current working directory
				original_dir = os.getcwd()
				st.write(original_dir)

				head_tail = os.path.split(temp_lzo_path)
				tail = head_tail[1]

				os.chdir(temp_dir)
				decompressed_path = tail.replace('.lzo', '')


				command_str = 'lzop -d '+ str(tail) + ' -o ' + str(decompressed_path)
				os.system(command_str)							

				os.system('ls')

				os.remove(tail)
				os.remove(decompressed_path)

				os.system('ls')

	os.chdir(original_dir)
	os.system('ls')
	os.system('pwd')


	#create .m files for each matlab function text 
	rf_image_content_web =  requests.get(rf_image_url).text
	st.write(rf_image_content_web)

	with open(rf_image_content_web, 'r') as file:
		rf_image_content = ''
		line = file.readline()
		
		while line:
			rf_image_content += line
			line = file.readline()

	with open("rf_image.m","w+") as f:
		f.write(rf_image_content)



'''
	script = 'rf_image.txt'

	with open(script, 'r') as file:
		rf_image_content = ''
		line = file.readline()
		
		while line:
			rf_image_content += line
			line = file.readline()

	with open("rf_image.m","w+") as f:
		f.write(rf_image_content)

	script = 'rdataread.txt'

	with open(script, 'r') as file:
		rdataread_content = ''
		line = file.readline()
		
		while line:
			rdataread_content += line
			line = file.readline()

	with open("rdataread.m","w+") as f:
		f.write(rdataread_content)

	script = 'ReadClariusYML.txt'

	with open(script, 'r') as file:
		ReadClariusYML_content = ''
		line = file.readline()
		
		while line:
			ReadClariusYML_content += line
			line = file.readline()

	with open("ReadClariusYML.m","w+") as f:
		f.write(ReadClariusYML_content)

	script = 'hilbert.txt'

	with open(script, 'r') as file:
		hilbert_content = ''
		line = file.readline()
		
		while line:
			hilbert_content += line
			line = file.readline()

	with open("hilbert.m","w+") as f:
		f.write(hilbert_content)

'''
	



	#st.write("File content as bytes:", bytes_data)

'''
	currentpath = os.path.abspath(os.getcwd())
	
	directory = 'files'
	path = os.path.join(currentpath, directory)


	#sort file into a new file, 'files'
	if not os.path.exists(path):
		os.makedirs(path)
		tar.extractall(path)
		tar.close()

	#filter out .lzo file 
	onlylzo = [f for f in listdir(path) if f.endswith('.lzo')]

	#for each lzo file, extract content 
	os.chdir(path)

	#need xcode and octave installation (homebrew)
	os.system('lzop -d *.lzo')
	os.chdir(currentpath)


	#create .m files for each matlab function text 
	script = 'rf_image.txt'

	with open(script, 'r') as file:
		rf_image_content = ''
		line = file.readline()
		
		while line:
			rf_image_content += line
			line = file.readline()

	with open("rf_image.m","w+") as f:
		f.write(rf_image_content)

	script = 'rdataread.txt'

	with open(script, 'r') as file:
		rdataread_content = ''
		line = file.readline()
		
		while line:
			rdataread_content += line
			line = file.readline()

	with open("rdataread.m","w+") as f:
		f.write(rdataread_content)

	script = 'ReadClariusYML.txt'

	with open(script, 'r') as file:
		ReadClariusYML_content = ''
		line = file.readline()
		
		while line:
			ReadClariusYML_content += line
			line = file.readline()

	with open("ReadClariusYML.m","w+") as f:
		f.write(ReadClariusYML_content)

	script = 'hilbert.txt'

	with open(script, 'r') as file:
		hilbert_content = ''
		line = file.readline()
		
		while line:
			hilbert_content += line
			line = file.readline()

	with open("hilbert.m","w+") as f:
		f.write(hilbert_content)


	#pass in currentfolder and file name as arguments 
	cur_dir = path 
	print(cur_dir)
	file = [f for f in listdir(path) if f.endswith('.raw') and 'rf' in f]
	file_name = file[0]

	oc = Oct2Py()

	x,y,z = oc.rf_image(cur_dir, file_name, nout = 3)

	plt.imshow(z, extent=[15, 70, 15, 70], cmap = 'gray')
	plt.show()
'''
'''
				files = os.listdir(temp_dir)
				for file in files:
					file_path = os.path.join(temp_dir, file)
					if os.path.isfile(file_path) and '.log' not in file_path:
						os.remove(file_path)

'''