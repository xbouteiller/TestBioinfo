# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:57:18 2020

@author: Xavier Bouteiller
@email: bouteiller.xavier@gmail.com

"""

import os
os.chdir('/home/xav/Documents/test_python')

from bioinfo.downloadFiles import get_file_links, download_files_series




#%% Download useful files
url = "https://molgenis26.target.rug.nl/downloads/gonl_public/variants/release5/"
# getting all video links 
file_links = get_file_links(archive_url = url)

# download all videos 
download_files_series(file_links=file_links,file_to_select='chr22')

#%% analysis
#tabix


import tabix
import vcfpy

# tabix
# Open a remote or local file.
tb = tabix.open("gonl.chr19.snps_indels.r5.vcf.gz")

# These queries are identical. A query returns an iterator over the results.
records = tb.query("19", 1000000, 1250000)
records = tb.queryi(19, 1000000, 1250000)
records = tb.querys("1:1000000-1250000")

# Each record is a list of strings.
for record in records:
    print(record[:3])

#vcfpy
# Open input, add FILTER header, and open output file
reader = vcfpy.Reader.from_path("gonl.chr19.snps_indels.r5.vcf.gz")
reader.header.add_filter_line(vcfpy.OrderedDict([
    ('ID', 'DP10'), ('Description', 'total DP < 10')]))
writer = vcfpy.Writer.from_path('/home/xbouteiller/Downloads/stout', reader.header)

# Add "DP10" filter to records having less than 10 reads
for record in reader:
    print(record)
    ad = sum(c.data.get('DP', 0) for c in record.calls)
    if ad < 10:
        record.add_filter('DP10')
    writer.write_record(record)
    
    help(vcfpy.Reader)

