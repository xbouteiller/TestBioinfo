# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:57:18 2020

@author: Xavier Bouteiller
@email: bouteiller.xavier@gmail.com

This program contains 4 main steps:
    1. download .gz .gz.tbi .md5 files from the http://www.nlgenome.nl/ for a specific chromosome defined by the user    
    2. load & extract values from vcf
    3. instantiate a sqllite db
    4. populate the db
    5. test the created db

Need to define the working folder as input (should contains the bioinfo folder with the __init__.py)

"""

# %% Dependencies 

# Generic import
import vcf
import os
# Import Table, Column, String, and Integer
from sqlalchemy import Table, Column, String, Integer, Float
from sqlalchemy import create_engine, MetaData
from sqlalchemy import insert
from sqlalchemy import select, and_
import pandas as pd

# specific import
# Enter the path to working folder (should contains bioinfo folder with the __init__.py)
path = input("Enter path to working folder (should contains bioinfo folder with the __init__.py): ") or '/home/xav/Documents/test_python'
print('path is: {}'.format(path))

# change the path to the folder where the bioinfo folder (with __init__.py)  is located
os.chdir(path) 
# user defined functions : functions for downloading file
from bioinfo.downloadFiles import get_file_links, download_files_series

#%% step 1: Download useful files
url = "https://molgenis26.target.rug.nl/downloads/gonl_public/variants/release5/"
# getting all .gz, .tbi, .md5 download links 
file_links = get_file_links(archive_url = url)

# download  all .gz, .tbi, .md5 download links
filetoselect='chr22'
download_files_series(file_links=file_links,file_to_select=filetoselect)


#%% step 2a: load vcf

'''
Documentation:
http://alimanfoo.github.io/2017/06/14/read-vcf.html
https://www.internationalgenome.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-40
https://pypi.org/project/PyVCF/

* ``Record.CHROM``
* ``Record.POS``
* ``Record.ID``
* ``Record.REF``
* ``Record.ALT``
* ``Record.QUAL``
* ``Record.FILTER``
* ``Record.INFO`
    
'''

InputFile="file//"+"gonl."+filetoselect+".snps_indels.r5.vcf.gz" # name of the vcf file
vcf_reader = vcf.Reader(filename=InputFile) # readthe vcf file

# extract number of observations (number of rows) within vcf file
rec=[]
nrow_vcf=len([rec.extend([record.CHROM]) for record in vcf_reader])
print('\nvcf contains {} rows'.format(nrow_vcf))

# few tests 
DoTest=False
if DoTest:
    for record in vcf_reader:
        print(record)
        
    vcf_reader = vcf.Reader(filename=InputFile)
    for record in vcf_reader:
        print(record.POS, record.ID) 
        
    vcf_reader = vcf.Reader(filename=InputFile)
    for record in vcf_reader:
        print(record.ID)          
    

#%% step 2b: extract data from vcf

# Empty list of values
values_list = []
inaccess=0

# Iterate over the rows
vcf_reader = vcf.Reader(filename=InputFile)
for record in vcf_reader:
    # filter the inaccessible records
    if record.FILTER == ['Inaccessible']:
        inaccess+=1
        continue
    else:
        # Create a dictionary with the values
        data = {'chromosome':record.CHROM,
                'position':record.POS,
                'alternative':str(record.ALT)[1:-1],
                'total_number_of_allele': record.INFO['AN'],
                'variant_frequency': float(str(record.INFO['AF'])[1:-1]),
                'ID':record.ID,
                'reference':record.REF}
        
    # Append the dictionary to the values list
    values_list.append(data)

print(inaccess) #16215
print(len(values_list)) #263278
print(inaccess+len(values_list)) #279493
print(values_list[0:1])

# Assessment
if nrow_vcf == (inaccess+len(values_list)):
    print('\ninitial n of observations {}\nn of inaccessible removed:{}\nfinal n of observations: {}\n'.format(inaccess+len(values_list),inaccess,len(values_list)))
else:
    raise ValueError('sum of removed n of obs and final obs dont equalize initial n of obs in the vcf')

# %% step 3: Instantiate the sqllite data base

# initialize db    
# Define an engine to connect to chr22.sqlite: engine
engine = create_engine('sqlite:///chr22.sqlite')

# Initialize MetaData: metadata
metadata = MetaData()

# Build a chr22 table: chr22
chr22 = Table('chr22', metadata,
               Column('chromosome', String()),
               Column('position', Integer()),
               Column('alternative', String()),
               Column('total_number_of_allele', Integer()),
               Column('variant_frequency', Float()),
               Column('ID', String()),
               Column('reference', String()))

# Create the table in the database
metadata.create_all(engine)

print(engine.table_names())

# %% step 4: insert to the database

# Build insert statement: stmt
stmt=insert(chr22)

# Use values_list to insert data: results
connection=engine.connect()
results=connection.execute(stmt, values_list)

# Print rowcount
print('\nn of inserted values: {}'.format(results.rowcount))

# %% step 5a: Check the data in db
stmt=select([chr22])
results=connection.execute(stmt).fetchmany(100)

# print columns names
print(chr22.columns.keys())

# Print the column names
print(chr22.columns.keys())

# Print full metadata of census
print(repr(chr22))

for res in results:
    print(res['alternative'], res['total_number_of_allele'], res['variant_frequency'])

for res in results:
    print(res['position'],res['alternative'], res['total_number_of_allele'],
          res['variant_frequency'],res['ID'], res['reference'] )
    
# %% step 5b: db extraction based on position
    
n=16054679 # lower boundary position
m=16218083 # upper boundary position
stmt = select([chr22]).where(and_(chr22.columns.position < m, 
                             chr22.columns.position > n)
    )


results=connection.execute(stmt).fetchall()

# return results within a pandas data frame
df_extracted = pd.DataFrame(results)
df_extracted.columns = results[0].keys()
df_extracted.head()


















