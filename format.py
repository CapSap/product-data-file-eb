import cProfile
import re
import time
import numpy as np
import pandas as pd
from tqdm import tqdm


def main():
    # Function to process SKU
    def process_sku(sku):
        # This will match formats like 'asd123-asd123'
        valid_format = r"^[\w]+-[\w]+$"
        sku = str(sku)  # Ensure it's a string
        # If SKU is already in valid format (exactly two words separated by one dash), keep it as is
        if re.match(valid_format, sku):
            return sku
        else:
            # Otherwise, remove the last part after the last dash
            return re.sub(r"-\w+$", "", sku)

    # global var. Read the img url Excel file
    df2 = pd.read_excel("excel-files/urls.xlsx")
    # Read the first Excel file
    df1 = pd.read_excel("excel-files/products.xlsx")

    df1_test = df1.sample(
        n=200,
        # random_state=42
    )  # n=15 specifies the number of rows to select, random_state is optional for reproducibility

    # main function

    def process_data(df_input):
        start_time = time.time()
        # Enable tqdm for pandas apply
        tqdm.pandas()

        # Apply SKU processing
        df_input["image_alt"] = df_input["Variant SKU"].apply(process_sku)

        # Remove rows where the column is blank (NaN or empty)
        df_cleaned = df_input.dropna(subset=["Variant SKU"])

        # Optionally, reset the index after dropping rows
        df_cleaned = df_cleaned.reset_index(drop=True)

       # HTML Description Matching Logic

        html_map = df1[df1['Body HTML'].notna()].groupby(
            df1['Variant SKU'].str.split('-').str[0]
        )['Body HTML'].first().to_dict()

        def find_html_description(row):
            sku_prefix = row['Variant SKU'].split('-')[0]
            return html_map.get(sku_prefix, row['Body HTML'])

        # Apply HTML matching before further processing
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

        df_cleaned.to_excel("modified_file_test.xlsx", index=False)

        print(df_cleaned)

        # Display completion message
        print("Script completed successfully!")

        # Calculate the elapsed time and display it
        elapsed_time = time.time() - start_time
        minutes = elapsed_time // 60  # Get the integer part of minutes
        seconds = elapsed_time % 60   # Get the remaining seconds
        print(f"Total execution time: {
              int(minutes)} minutes {seconds:.2f} seconds."
              )

    process_data(df1)


# Run the main function with cProfile
if __name__ == "__main__":

    cProfile.run('main()', 'profile_output.prof')
