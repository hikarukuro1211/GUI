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

import plotly.express as px
import numpy as np

#defining .txt file locations 
rf_image_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/rf_image.txt'
rdataread_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/rdataread.txt'
ReadClariusYML_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/ReadClariusYML.txt'
hilbert_url = 'https://raw.githubusercontent.com/hikarukuro1211/GUI/main/hilbert.txt'

st.title('Data Visualizer')
st.sidebar.subheader('Upload a file')

uploaded_files = st.sidebar.file_uploader("Upload a file", type = "tar", accept_multiple_files=True)
original_dir = os.getcwd()

if uploaded_files is not None:  
	for uploaded_file in uploaded_files:
		#tar = tarfile.open("prac.tar")
		bytes_data = uploaded_file.getvalue()
		with tarfile.open(fileobj = BytesIO(bytes_data)) as tf:
			for entry in tf:
				extract = tf.extractfile(entry)
				if entry.name.endswith('.lzo'):
					#st.write(entry.name)
					with tempfile.NamedTemporaryFile(delete=False, suffix='.lzo') as temp_lzo:
						temp_lzo.write(extract.read())
						temp_lzo_path = temp_lzo.name
						temp_dir = os.path.dirname(temp_lzo_path) #get directory of the temp files 

						if 'rf' in entry.name:
							temp_lzo_name_rf = temp_lzo_path
						



					# Save the current working directory
					#st.write(original_dir)

					head_tail = os.path.split(temp_lzo_path)
					tail = head_tail[1]
					#st.write(temp_dir)
					os.chdir(temp_dir)
					decompressed_path = tail.replace('.lzo', '')


					command_str = 'lzop -d '+ str(tail) + ' -o ' + str(decompressed_path)
					os.system(command_str)							
				if entry.name.endswith('rf.yml'):
					with tempfile.NamedTemporaryFile(delete=False, suffix = '.yml') as temp_lzo:
						temp_lzo.write(extract.read())
						temp_lzo_name_env = temp_lzo.name


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
				
			oc = Oct2Py()
			cur_dir = temp_dir
			file_name = decompressed_path

			temp_lzo_name_rf = temp_lzo_name_rf.replace('.lzo', '')
			#temp_lzo_name_env = temp_lzo_name_env.replace('.yml', '')

			x,y,z = oc.rf_image(temp_lzo_name_rf, temp_lzo_name_env, nout = 3)

			#for filename in os.listdir(os.path.dirname(temp_lzo_path)):
			#	if filename.is_file():
			#		os.remove(filename)

			os.remove(tail)
			os.remove(decompressed_path)

			#fig = go.Figure(data=go.Heatmap(z))
			#fig.layout.height = 500
			#fig.layout.width = 500
			

			x_min = x.min()
			x_max = x.max()
			x_val = np.linspace(x_min, x_max, num = z.shape[1])

			y_min = y.min()
			y_max = y.max()
			y_val = np.linspace(y_min, y_max, num = z.shape[0])

			

			label_dict = {'x': 'width (cm)', 'y': 'depth (cm)'}

			fig = px.imshow(z, labels = label_dict, color_continuous_scale="gray_r", aspect="auto", width=600, height=600, zmin=15, zmax=70, x = x_val, y = y_val)
			fig.update_layout(coloraxis_showscale=False)
			#fig.update_xaxes(range=[x_min, x_max])
			#fig.update_yaxes(range=[y_min, y_max])

			#plt.show()
			st.plotly_chart(fig)

			st.cache_data.clear()

			os.chdir(temp_dir)
