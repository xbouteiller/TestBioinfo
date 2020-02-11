# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:57:18 2020

@author: Xavier Bouteiller
@email: bouteiller.xavier@gmail.com


"""

import os
os.chdir('/home/xav/Documents/test_python')


#function for downloading files
from bioinfo.downloadFiles import get_file_links, download_files_series
import vcf
import sqlalchemy



#%% Download useful files
url = "https://molgenis26.target.rug.nl/downloads/gonl_public/variants/release5/"
# getting all video links 
file_links = get_file_links(archive_url = url)

# download all videos 
download_files_series(file_links=file_links,file_to_select='chr22')

#%% analysis

'''
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
InputFile="file//"+"gonl.chr22.snps_indels.r5.vcf.gz"

vcf_reader = vcf.Reader(filename=InputFile)
for record in vcf_reader:
    print(record)
    
vcf_reader = vcf.Reader(filename=InputFile)
for record in vcf_reader:
    print(record.POS, record.ID) 
    
vcf_reader = vcf.Reader(filename=InputFile)
for record in vcf_reader:
    print(record.ID)   
   
    

# %% data base
from sqlalchemy import create_engine, MetaData

# initialize db    
# Define an engine to connect to chapter5.sqlite: engine
engine = create_engine('sqlite:///chr22.sqlite')

# Initialize MetaData: metadata
metadata = MetaData()


# Import Table, Column, String, and Integer
from sqlalchemy import Table, Column, String, Integer, Float

# Build a census table: census
chr22 = Table('chr22', metadata,
               Column('position', Integer()),
               Column('alternative', String()),
               Column('total_number_of_allele', Integer()),
               Column('variant_frequency', Float()),
               Column('ID', String()),
               Column('reference', String()))

# Create the table in the database
metadata.create_all(engine)
print(engine.table_names())

# populate db
# Create an empty list: values_list
#values_list = []


## Iterate over the rows
#vcf_reader = vcf.Reader(filename=InputFile)
#for record in vcf_reader:
#    # Create a dictionary with the values
#    data = {'position':record.POS,
#            'alternative':str(record.ALT)[1:-1],
#            'total_number_of_allele': record.INFO['AN'],
#            'variant_frequency': float(str(record.INFO['AF'])[1:-1]),
#            'ID':record.ID,
#            'reference':record.REF}
#    
#    # Append the dictionary to the values list
#    values_list.append(data)
#
#print(len(values_list))#279493
#print(values_list[0:1])


values_list = []
# Iterate over the rows
inacess=0
vcf_reader = vcf.Reader(filename=InputFile)
for record in vcf_reader:
    if record.FILTER == ['Inaccessible']:
        inacess+=1
        continue
    else:
        # Create a dictionary with the values
        data = {'position':record.POS,
                'alternative':str(record.ALT)[1:-1],
                'total_number_of_allele': record.INFO['AN'],
                'variant_frequency': float(str(record.INFO['AF'])[1:-1]),
                'ID':record.ID,
                'reference':record.REF}
        
        # Append the dictionary to the values list
    values_list.append(data)

print(inacess)#16215
print(len(values_list))#263278
print(inacess+len(values_list))#279493
print(values_list[0:1])

# Import insert
from sqlalchemy import insert
from sqlalchemy import select, func
#https://stackoverflow.com/questions/9706059/setting-a-default-value-in-sqlalchemy

# Build insert statement: stmt
stmt=insert(chr22)

# Use values_list to insert data: results
connection=engine.connect()
results=connection.execute(stmt, values_list)

# Print rowcount
print(results.rowcount)








from sqlalchemy import select
stmt=select([chr22])
results=connection.execute(stmt).fetchmany(1000)

print(chr22.columns.keys())
for res in results:
    print(res['position'],res['alternative'], res['total_number_of_allele'], res['variant_frequency'],res['ID'], res['reference'] )
    
# Print the column names
print(chr22.columns.keys())

# Print full metadata of census
print(repr(chr22))

for res in results:
    print(res['alternative'], res['total_number_of_allele'], res['variant_frequency'])









'''
Conceive an SQL database schema, which will permit you to store the variant data, such
as genomic position, nucleotide changes, alternative allele count, total number of alleles,
variant frequency, a unique variant ID (identifier) and the dbSNP reference (rsid).

The data scheme should be optimised for queries based on genomic intervals (e.g. find
all of the variants present in chromosome 22 between genomic positions n and m).
Write a program in Python (or another programming language you are more comfortable
with) to populate this database from the VCF file from GoNL (SNVs and indels). Exclude
variants "Inaccessible"

'''















import tabix
import vcfpy
import sqlalchemy


reader = vcfpy.Reader.from_path("file//"+"gonl.chr22.snps_indels.r5.vcf.gz")

i=0
for rec in reader:
    print(rec)
    i+=1

import vcfpy
# Open file, this will read in the header
reader = vcfpy.Reader.from_path(InputFile)
# Build and print header
header = ['#CHROM', 'POS', 'REF', 'ALT'] + reader.header.samples.namesprint('\t'.join(header))











# tabix
# Open a remote or local file.
tb = tabix.open("file//"+"gonl.chr22.snps_indels.r5.vcf.gz")

# These queries are identical. A query returns an iterator over the results.
records = tb.query("19", 1000000, 1250000)
records = tb.queryi(19, 1000000, 1250000)
records = tb.querys("1:1000000-1250000")

# Each record is a list of strings.
for record in reader:
    print(record)

#vcfpy
# Open input, add FILTER header, and open output file
reader = vcfpy.Reader.from_path("file//"+"gonl.chr22.snps_indels.r5.vcf.gz")
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

