import cProfile
import re
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import os


def main():
    # Function to remove size from sku
    def get_sku_wo_size(sku):
        # This will match formats like 'asd123-asd123'
        valid_format = r"^[\w]+-[\w]+$"
        sku = str(sku)  # Ensure it's a string
        # If SKU is already in valid format (exactly two words separated by one dash), keep it as is
        if re.match(valid_format, sku):
            return sku
        else:
            # Otherwise, remove the last part after the last dash
            return re.sub(r"-\w+$", "", sku)

    # function to create parent rows

    def create_parent_rows(df):
        parent_rows = df.groupby(df['Variant SKU'].apply(get_sku_wo_size)).agg({
            'Option1 Value': 'first',
            'Title': 'first',
            'Smart Collections': 'first',
            'Option1 Name': 'first',
            'Vendor': 'first',
            'Body HTML': 'first',
            'image_alt': 'first'
        }).reset_index()

        parent_rows.rename(columns={'index': 'Variant SKU'}, inplace=True)
        parent_rows['Option2 Value'] = None
        parent_rows['Variant Inventory Item ID'] = None
        parent_rows['Variant ID'] = None
        parent_rows['Variant Weight'] = None
        parent_rows['Variant Price'] = None

        # identify url column names
        url_columns = [col for col in df.columns if col.startswith('url_')]

        # Initialize URL columns in parent_rows with an empty value
        for col in url_columns:
            parent_rows[col] = None

        # Copy URL columns from the first matching child
        for idx, parent_row in parent_rows.iterrows():
            sku_prefix = get_sku_wo_size(parent_row['Variant SKU'])
            matching_rows = df[df['Variant SKU'].apply(
                get_sku_wo_size) == sku_prefix]
            if not matching_rows.empty:
                for col in url_columns:
                    if col in matching_rows.columns:
                        parent_rows.at[idx, col] = matching_rows.iloc[0][col]

        return parent_rows

        # main function

    def process_data(df_input):
        start_time = time.time()
        # Enable tqdm for pandas apply
        tqdm.pandas()

        # add in the sku without size as image_alt
        df_input["image_alt"] = df_input["Variant SKU"].apply(get_sku_wo_size)

        # Remove rows where the column is blank (NaN or empty)
        df_cleaned = df_input.dropna(subset=["Variant SKU"])

        # Optionally, reset the index after dropping rows
        df_cleaned = df_cleaned.reset_index(drop=True)

       # HTML Description Matching Logic

       # create a dictionary that is { first sku word : html body }
        html_map = df1[df1['Body HTML'].notna()].groupby(
            df1['Variant SKU'].str.split('-').str[0]
        )['Body HTML'].first().to_dict()

        # this func accepts a row, and matches it with the dictionary { first sku word : html body }
        # if nothing is found in the map, return the html body that already exists on the row
        def find_html_description(row):
            sku_prefix = row['Variant SKU'].split('-')[0]
            return html_map.get(sku_prefix, row['Body HTML'])

        # Apply the HTML matching function to each row in the df
        df_cleaned['Body HTML'] = df_cleaned.apply(
            find_html_description, axis=1)

        # Step 2: Function to process each row and match

        def process_row(index, row):
            # Access the 'search' column value in df1
            search_string = row["image_alt"]

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
                    df_cleaned.at[index, column_name] = value

        # Apply the function to each row with tqdm progress bar
        df_cleaned.progress_apply(
            lambda row: process_row(row.name, row), axis=1)
        print(df_cleaned)

        # Create parent rows and merge with cleaned data
        parent_rows = create_parent_rows(df_cleaned)
        print(parent_rows)
        final_df = pd.concat([df_cleaned, parent_rows], ignore_index=True).drop_duplicates(
            subset=['Variant SKU'], keep='first').sort_values(by='Variant SKU')

        # Get current date and time formatted as 'YYYY-MM-DD_HH-MM-SS'
        timestamp = time.strftime("%H-%M%p on %A %B %dth")
        output_filename = f"product data file created at {timestamp}.xlsx"
        final_df.to_excel(os.path.join("output", output_filename), index=False)

        # Display completion message
        print("Script completed successfully!")

        # Calculate the elapsed time and display it
        elapsed_time = time.time() - start_time
        minutes = elapsed_time // 60  # Get the integer part of minutes
        seconds = elapsed_time % 60   # Get the remaining seconds
        print(f"Total execution time: {
              int(minutes)} minutes {seconds:.2f} seconds."
              )

    # LOAD THE EXCEL FILES
    # img url excel file. needs a column called "Image Src" with urls. Get report from shopify
    df2 = pd.read_excel("excel-files/urls.xlsx")
    # Read the products file from shopify
    df1 = pd.read_excel("excel-files/products.xlsx")

    # smaller DF for testing purposes
    df1_test = df1.sample(
        n=200,
        # random_state=42
    )  # n=15 specifies the number of rows to select, random_state is optional for reproducibility

    df1_first200 = df1.head(200)

    # call the main function
    process_data(df1)


# Run the main function with cProfile
if __name__ == "__main__":

    cProfile.run('main()', 'profile_output.prof')
