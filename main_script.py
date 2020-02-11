# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:57:18 2020

@author: Xavier Bouteiller
@email: bouteiller.xavier@gmail.com

"""

import os
os.chdir('/home/xav/Documents/test_python')

from downloadFiles import get_file_links, download_files_series




#%% Download useful files
url = "https://molgenis26.target.rug.nl/downloads/gonl_public/variants/release5/"
# getting all video links 
file_links = get_file_links(archive_url = url)

# download all videos 
download_files_series(file_links=file_links,file_to_select='chr22')

#%% analysis


https://molgenis26.target.rug.nl/downloads/gonl_public/variants/release5/gonl.chr1.snps_indels.r5.vcf.gz.tbi