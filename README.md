there are 2 input files.

1.  is the main shopify export.
2.  is a single file with urls only. (i think i should change the name of this column reference in the script so that it matches the shopify export)
    or i could make the script reference the first colmn only.

add both of these files to a folder called excel-files on the root of the project. Call each file "products.xlsx" and "urls.xlsx"


To get started run the following commands

1.`python3 -m venv env` - this will create an virutal env

2.`source env/bin/activate` - this will activate the venv in the shell

3.`pip install -r requirements.txt` - this will install lib modules 

`python format.py` - this will run the script. make sure that the correct excel files are in the appropriate folder



