

import pandas as pd

# Read the first Excel file
df1 = pd.read_excel('excel-files/products.xlsx')

# Read the second Excel file
df2 = pd.read_excel('excel-files/urls.xlsx')

# Print basic information about the dataframes
print("First file info:")
print(df1.info())

print("\nSecond file info:")
print(df2.info())

# Step 1: Transform the text in the column (e.g., 'Product Name')
# Use a regex to remove the last "word" and trailing dash (e.g., xxx-xxxx-xxxx -> xxx-xxxx)
df1['search'] = df1['Variant SKU'].str.replace(r'-\w+$', '', regex=True).astype(str)

# testing file
print(df1.info())
print(df1.head(15))
