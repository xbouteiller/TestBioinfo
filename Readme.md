# Test Bioinfo

## Authors

**Xavier Bouteiller**

*bouteiller.xavier@gmail.com* 

## Program description

This program allows to download vcf files from http://www.nlgenome.nl/
The variant data are then extracted and used for populate a sqllite database.

This program consists in 5 main steps:

1. download .gz .gz.tbi .md5 files from the http://www.nlgenome.nl/ for a specific chromosome defined by the user
2. load & extract values from vcf
3. instantiate a sqllite db
4. populate the db
5. test the created db

Need to define the working folder as input (should contains the bioinfo folder with the __init__.py)

## script execution
Program is contained within file: **main_script.py**

It can be executed from the console:
'''
python main_script.py
'''
or by using interactive environment
