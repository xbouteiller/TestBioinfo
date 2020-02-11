#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:57:18 2020

@author: Xavier Bouteiller
@email: bouteiller.xavier@gmail.com

Download files corresponding to a chromosome from web page
https://www.geeksforgeeks.org/downloading-files-web-using-python/
"""

import requests 
from bs4 import BeautifulSoup 
#import wget
import os
''' 
URL of the archive web-page which provides link to 
all video lectures. It would have been tiring to 
download each video manually. 
In this example, we first crawl the webpage to extract 
all the links and then download videos. 
'''



def get_file_links(archive_url): 	
    # create response object 
    r = requests.get(archive_url) 	
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html5lib') 	
    # find all links on web-page 
    links = soup.findAll('a')
#    print(links)
    # filter the link sending with .mp4 
    file_links = [archive_url + link['href'].split('/')[-1] for link in links if link['href'].endswith('tbi') or link['href'].endswith('gz') or link['href'].endswith('md5')] 
    return file_links 


def download_files_series(file_links, file_to_select):
    if file_to_select=='all':
        file_links=file_links
    else:   
        #select file to download
        file_links=[file for file in file_links if file_to_select in file]
        if len(file_links)==0:
            raise ValueError('no file corresponding found')
    for link in file_links:
        # obtain filename by splitting url and getting 
        # last string 
        file_name = link.split('/')[-1] 
        print("Downloading file:{}".format(file_name))
        # create response object 
#        wget.download(link, file_name)
        r = requests.get(link, stream = True)
        
        if not os.path.exists('file'):
            os.makedirs('file')
            print('file folder created')
            
        # download started 
        with open('file//'+file_name, 'wb') as f: 
            f.write(r.content) 		
            print("{} downloaded!\n".format(file_name))
            

    print("All files downloaded!")
    return




