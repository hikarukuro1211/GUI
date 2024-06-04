import streamlit as st
import pandas as pd

import tarfile
import os 
from os import listdir 
import tempfile 
import subprocess 
import urllib
#from oct2py import Oct2Py

import matplotlib.pyplot as plt
from io import BytesIO

import requests
from bs4 import BeautifulSoup
#import urllib2  # the lib that handles the url stuff
import base64
import json 

rf_image_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/rf_image.txt'


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

	#create .m files for each matlab function text 
	#rf_image_content_web = json.loads(requests.get(rf_image_url, stream = True).text)
	rf_image_content_web = requests.get(rf_image_url, stream = True).text
	#rf_image_content = ''
	#for line in rf_image_content_web:
	#	rf_image_content += line

	#with open("rf_image.m","w+") as f:
	#	f.write(rf_image_content_web)
	#os.system('pwd')

	#os.system('ls')
