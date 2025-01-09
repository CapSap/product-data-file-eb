# Product data file

## Intro

This python scrip will take in 2 x excel files and add in image urls for products. It will also create a parent sku row for each product

## Prerequisites

there are 2 input files that the script needs. Both come from shopfy. I should label each export and put the details here

1.  is the main shopify export. The filename must be "products.xlsx"
2.  is a single file with urls in one column only. The column name must be "Image Src", and the filename must be urls.xlsx

add both of these files to a folder called excel-files on the root of the project.

### To get started run the following commands

1.`python3 -m venv env` - this will create an virutal env

2.`source env/bin/activate` - this will activate the venv in the shell

3.`pip install -r requirements.txt` - this will install lib modules

`python format.py` - this will run the script. make sure that the correct excel files are in the appropriate folder. on laptop script takes about 35mins
