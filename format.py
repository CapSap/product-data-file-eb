import re
import time
import pandas as pd
from tqdm import tqdm

start_time = time.time()

# Enable tqdm for pandas apply
tqdm.pandas()

# Read the first Excel file
df1 = pd.read_excel("excel-files/products.xlsx")

# Read the second Excel file
df2 = pd.read_excel("excel-files/urls.xlsx")

# Print basic information about the dataframes
print("First file info:")
print(df1.info())

print("\nSecond file info:")
print(df2.info())

#  Transform the text in the column
valid_format = r"^[\w]+-[\w]+$"  # This will match formats like 'asd123-asd123'


def process_sku(sku):
    sku = str(sku)  # Ensure it's a string
    # If SKU is already in valid format (exactly two words separated by one dash), keep it as is
    if re.match(valid_format, sku):
        return sku
    else:
        # Otherwise, remove the last part after the last dash
        return re.sub(r"-\w+$", "", sku)


df1["image_alt"] = df1["Variant SKU"].apply(process_sku)


# Remove rows where the column is blank (NaN or empty)
df1_cleaned = df1.dropna(subset=["Variant SKU"])

# Optionally, reset the index after dropping rows
df1_cleaned = df1_cleaned.reset_index(drop=True)

df1_test = df1_cleaned.sample(
    n=20,
    #  random_state=42
)  # n=15 specifies the number of rows to select, random_state is optional for reproducibility


# Step 2: Function to process each row and match
def process_row(index, row):
    search_string = row["image_alt"]  # Access the 'search' column value in df1

    # Ensure search_string is a valid string (convert to string if it's not)
    if pd.isna(search_string):  # Check if it's NaN
        search_string = ""  # If NaN, skip or use an empty string for search

    # Step 3: Search for this string in df2
    match = df2[df2["Image Src"].str.contains(
        r"\b" + re.escape(str(search_string)) + r"\b", na=False, regex=True)]

    # Step 4: If matches are found, append them to the row in separate columns
    if not match.empty:
        # For each match, create a new column dynamically
        for i, value in enumerate(match["Image Src"].values):
            column_name = f"url_{i+1}"
            # Assign match value to the dynamic column
            df1.at[index, column_name] = value


# Apply the function to each row with tqdm progress bar
df1_cleaned.progress_apply(lambda row: process_row(row.name, row), axis=1)

"""
# Step 2: Iterate through each row in df1
for index, row in df1.iterrows():
    search_string = row["image_alt"]  # Access the 'search' column value in df1

    # Ensure search_string is a valid string (convert to string if it's not)
    if pd.isna(search_string):  # Check if it's NaN
        search_string = ""  # If NaN, skip or use an empty string for search

    # Step 3: Search for this string in df2
    match = df2[df2["Image Src"].str.contains(
        r"\b" + re.escape(str(search_string)) + r"\b", na=False, regex=True)]

    # Step 4: If matches are found, append them to the row in separate columns
    if not match.empty:
        # For each match, create a new column dynamically
        for i, value in enumerate(match["Image Src"].values):
            column_name = f"url_{i+1}"
            df1.at[index, column_name] = (
                value  # Assign match value to the dynamic column
            )
            
"""


# testing file
# print(df1_test.info())
# print(df1_test.head(15))

# df1_test.to_excel("modified_file_test.xlsx", index=False)

print(df1.info())
print(df1.head(15))

df1.to_excel("modified_file_test.xlsx", index=False)
# testing first line

# Display completion message
print("Script completed successfully!")

# Calculate the elapsed time and display it
elapsed_time = time.time() - start_time
print(f"Total execution time: {elapsed_time:.2f} seconds.")
