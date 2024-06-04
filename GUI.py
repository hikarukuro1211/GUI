import streamlit as st
import pandas as pd

import tarfile
import os 
from os import listdir 
import tempfile 
import subprocess 
import urllib
from oct2py import Oct2Py

import matplotlib.pyplot as plt
from io import BytesIO

import requests
from bs4 import BeautifulSoup
#import urllib2  # the lib that handles the url stuff
import base64
import json 

#defining .txt file locations 
rf_image_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/rf_image.txt'
rdataread_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/rdataread.txt'
ReadClariusYML_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/ReadClariusYML.txt'
hilbert_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/hilbert.txt'

st.title('Data Visualizer')
st.sidebar.subheader('Upload a file')

uploaded_file = st.sidebar.file_uploader("Upload a file", type = "tar")
original_dir = os.getcwd()

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
				st.write(original_dir)

				head_tail = os.path.split(temp_lzo_path)
				tail = head_tail[1]
				st.write(temp_dir)
				os.chdir(temp_dir)
				decompressed_path = tail.replace('.lzo', '')


				command_str = 'lzop -d '+ str(tail) + ' -o ' + str(decompressed_path)
				os.system(command_str)							
				os.system('ls')

				#clear up the tempfolder once done 
				

				rf_image_content_web = requests.get(rf_image_url, stream = True).text

				with open("rf_image.m","w+") as f:
					f.write(rf_image_content_web)

				rdataread_content_web = requests.get(rdataread_url, stream = True).text

				with open("rdataread.m","w+") as f:
					f.write(rdataread_content_web)

				ReadClariusYML_content_web = requests.get(ReadClariusYML_url, stream = True).text

				with open("ReadClariusYML.m","w+") as f:
					f.write(ReadClariusYML_content_web)

				hilbert_content_web = requests.get(hilbert_url, stream = True).text

				with open("hilbert.m","w+") as f:
					f.write(hilbert_content_web)
					
				#os.system('pwd')

				#os.system('ls')


				oc = Oct2Py()
				cur_dir = temp_dir
				file_mame = decompressed_path
				st.write(file_mame)
				x,y,z = oc.rf_image(file_mame, nout = 3)
				st.write(x,y,z)

				os.remove(tail)
				os.remove(decompressed_path)

			#plt.imshow(z, extent=[15, 70, 15, 70], cmap = 'gray')
			#plt.show()



		os.chdir(temp_dir)
