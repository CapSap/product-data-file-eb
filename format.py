import os
import glob
import cProfile
import re
import time
import numpy as np
import pandas as pd
from tqdm import tqdm

from utils.helpers import match_string_in_url


def main():
    """transform excel file into another csv file"""
    # set for the get wo size function
    KNOWN_SIZES = {  # pylint: disable=invalid-name
        "0",
        "26",
        "28",
        "30",
        "32",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "50",
        "52",
        "54",
        "56",
        "58",
        "60",
        "62",
        "64",
        "66",
        "68",
        "2XL",
        "3XL",
        "4XL",
        "5XL",
        "6XL",
        "7XL",
        "8XL",
        "L",
        "LXL",
        "M",
        "S",
        "SM",
        "XL",
        "XS",
        "XXS",
    }

    # Function to remove size from sku
    def get_sku_wo_size(sku):
        sku = str(sku)  # Ensure it's a string
        parts = sku.split("-")

        if len(parts) >= 2 and parts[-1] in KNOWN_SIZES:
            return "-".join(parts[:-1])  # Remove the last part if it's a known size

        return sku  # Keep everything if no size is detected

    # function to create parent rows
    def create_parent_rows(df):
        parent_rows = (
            df.groupby(df["Variant SKU"].apply(get_sku_wo_size))
            .agg(
                {
                    "Option1 Value": "first",
                    "Title": "first",
                    "Vendor": "first",
                    "Body HTML": "first",
                    "image_alt": "first",
                }
            )
            .reset_index()
        )

        parent_rows.rename(columns={"index": "Variant SKU"}, inplace=True)
        parent_rows["Option2 Value"] = None
        parent_rows["Variant Inventory Item ID"] = None
        parent_rows["Variant ID"] = None
        parent_rows["Variant Weight"] = None
        parent_rows["Variant Price"] = None

        # identify url column names
        url_columns = [col for col in df.columns if col.startswith("url_")]

        # Initialize URL columns in parent_rows with an empty value
        for col in url_columns:
            parent_rows[col] = None

        # Copy URL columns from the first matching child
        for idx, parent_row in parent_rows.iterrows():
            sku_prefix = get_sku_wo_size(parent_row["Variant SKU"])
            matching_rows = df[df["Variant SKU"].apply(get_sku_wo_size) == sku_prefix]
            if not matching_rows.empty:
                for col in url_columns:
                    if col in matching_rows.columns:
                        parent_rows.at[idx, col] = matching_rows.iloc[0][col]

        return parent_rows

        # main function

    def process_data(df_input):
        print("Starting data processing...")

        start_time = time.time()
        # Enable tqdm for pandas apply
        tqdm.pandas()

        # add in the sku without size as image_alt
        print("  Processing SKUs...")
        df_input["image_alt"] = tqdm(
            df_input["Variant SKU"].apply(get_sku_wo_size),
            total=len(df_input),
            desc="  Generating image_alt",
        )
        print("  Done!")

        # Remove rows where the column is blank (NaN or empty)
        df_cleaned = df_input.dropna(subset=["Variant SKU"])

        # Define the base columns to keep
        columns_to_keep = [
            "ID",
            "Title",
            "Body HTML",
            "Vendor",
            "Variant Inventory Item ID",
            "Option1 Value",
            "Option2 Value",
            "Variant SKU",
            "Variant Barcode",
            "Variant Weight",
            "Variant Weight Unit",
            "Variant Price",
            "image_alt",
        ]

        # Identify dynamically generated URL columns
        url_columns = [col for col in df_cleaned.columns if col.startswith("url_")]

        # Combine base columns with URL columns
        final_columns = columns_to_keep + url_columns

        # Keep only the whitelisted columns
        df_cleaned = df_cleaned[final_columns]

        # Optionally, reset the index after dropping rows
        df_cleaned = df_cleaned.reset_index(drop=True)

        # HTML Description Matching Logic
        print("\nMatching HTML descriptions...")
        # create a dictionary that is { first sku word : html body }
        html_map = (
            df_all[df_all["Body HTML"].notna()]
            .groupby(df_all["Variant SKU"].str.split("-").str[0])["Body HTML"]
            .first()
            .to_dict()
        )

        # this func accepts a row, and matches it with the dictionary { first sku word : html body }
        # if nothing is found in the map, return the html body that already exists on the row
        def find_html_description(row):
            sku_prefix = row["Variant SKU"].split("-")[0]
            return html_map.get(sku_prefix, row["Body HTML"])

        # Apply the HTML matching function to each row in the df
        # df_cleaned["Body HTML"] = df_cleaned.apply(find_html_description, axis=1)
        df_cleaned["Body HTML"] = df_cleaned.progress_apply(
            find_html_description, axis=1
        )
        # Step 2: Function to process each row and match

        def process_row(index, row):
            # Get the search string from image_alt column
            parent_id = row["ID"]
            search_string = (
                str(row["image_alt"]) if not pd.isna(row["image_alt"]) else ""
            )

            if not search_string:  # Skip empty search strings
                return

            filtered_images = df_images[df_images["ID"] == parent_id]

            if not filtered_images.empty:

                # Create a mask for matching rows using our new function
                mask = filtered_images["Trimmed Src"].apply(
                    lambda x: match_string_in_url(search_string, str(x))
                )
                match = filtered_images[mask]
            else:
                # add a log to display when the ID search fails
                print(f"Fallback triggered for SKU: {search_string} (ID: {parent_id})")
                mask = df_images["Trimmed Src"].apply(
                    lambda x: match_string_in_url(search_string, str(x))
                )
                match = df_images[mask]
            # If matches are found, append them to the row in separate columns
            if not match.empty:
                for i, value in enumerate(match["Image Src"].values):
                    column_name = f"url_{i+1}"
                    df_cleaned.at[index, column_name] = value

        # Apply the function to each row with tqdm progress bar
        print("\nMatching images...")
        with tqdm(total=len(df_cleaned), desc="  Processing image matches") as pbar:
            for index, row in df_cleaned.iterrows():
                process_row(index, row)
                pbar.update(1)
        print("  Done!")

        # Create parent rows and merge with cleaned data
        print("\nCreating parent rows...")
        parent_rows = create_parent_rows(df_cleaned)
        print("  Done!")

        print("\nFinalizing data...")
        with tqdm(total=3, desc="Saving files") as pbar:
            final_df = (
                pd.concat([df_cleaned, parent_rows], ignore_index=True)
                .drop_duplicates(subset=["Variant SKU"], keep="first")
                .sort_values(by="Variant SKU")
            )
            pbar.update(1)

            # Get current date and time formatted as 'YYYY-MM-DD_HH-MM-SS'
            timestamp = time.strftime("%H-%M%p on %A %B %dth")

            # Save to CSV
            timestamp = time.strftime("%H-%M%p on %A %B %dth")
            final_df.to_csv(
                os.path.join("output", f"product_data_{timestamp}.csv"),
                index=False,
                quoting=1,
            )
            pbar.update(1)

            # Save to Excel
            with pd.ExcelWriter(
                os.path.join("output", f"product_data_{timestamp}.xlsx"),
                engine="xlsxwriter",
            ) as writer:
                final_df.to_excel(writer, index=False, sheet_name="Sheet1")
                # [Excel formatting code remains the same]
                # Get the workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets["Sheet1"]

                # Define text format
                # "@" forces text format in Excel
                text_format = workbook.add_format({"num_format": "@"})

                # Apply text format to specific columns
                worksheet.set_column("A:A", None, text_format)  # Column A (ID)
                # Column I (Variant Barcode)
                worksheet.set_column("I:I", None, text_format)
            pbar.update(1)

        # Display completion message
        print("Script completed successfully!")

        # Calculate the elapsed time and display it
        elapsed_time = time.time() - start_time
        minutes = elapsed_time // 60  # Get the integer part of minutes
        seconds = elapsed_time % 60  # Get the remaining seconds
        print(f"Total execution time: {int(minutes)} minutes {seconds:.2f} seconds.")

    # LOAD THE EXCEL FILES
    print("Loading Excel files...")
    # Read the single export file from shopify matrixify
    # Get all matching files
    files = glob.glob(os.path.join("excel-files", "Export_*.xlsx"))
    # define df_all in the top level  main func
    df_all = None
    # Find the most recently created file
    if files:
        latest_file = max(files, key=os.path.getmtime)
        print("  Most recent file:", latest_file)
    else:
        print("  No matching files found.")

    df_all = pd.read_excel(latest_file)
    df_all = df_all[
        df_all["Status"].str.lower() != "archived"
    ]  # Filter out archived rows
    df_all_first_few = df_all.head(1000)

    # Create a URL df
    print("\nProcessing image URLs and creating data frame...")
    df_images = (
        df_all[["ID", "Image Src"]].drop_duplicates().dropna().reset_index(drop=True)
    )
    # trim extra words
    df_images["Trimmed Src"] = df_images["Image Src"].str.extract(
        r"https://cdn\.shopify\.com/s/files/1/0799/3953/5165/[^/]+/(.*)"
    )

    print("  Done!")

    # call the main function
    process_data(df_all)


# Run the main function with cProfile
if __name__ == "__main__":

    cProfile.run("main()", "profile_output.prof")
