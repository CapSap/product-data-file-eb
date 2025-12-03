"""Helper functions"""

import re

import pandas as pd


# func that matches a sku with url text
def match_string_in_url(search_string, url):
    """
    Match a multi-part SKU in a URL, handling different separators.
    For example, "AHN05-BLU" should match "ahn05_blu_s_v3_hr.jpg"

    Args:
        search_string: The SKU to search for (e.g., "AHN05-BLU")
        url: The URL/filename to search in (e.g., "ahn05_blu_s_v3_hr.jpg")

    Returns:
        bool: True if both parts of the SKU are found in sequence, False otherwise
    """
    try:
        # Convert inputs to strings and handle None
        search_string = str(search_string) if search_string is not None else ""
        url = str(url) if url is not None else ""

        if not search_string or not url:
            return False

        # Split the search string into parts
        sku_parts = search_string.split("-")
        if len(sku_parts) < 2:
            # If there's no hyphen, treat the whole string as one part
            pattern = r"(?:^|[._-])({})(?=[._-]|$)".format(re.escape(search_string))
        else:
            # Create pattern that matches both parts with any separator between them
            part1 = re.escape(sku_parts[0])
            part2 = re.escape(sku_parts[1])
            pattern = r"(?:^|[._-]){}[._-]{}(?=[._-]|$)".format(part1, part2)

        match = re.search(pattern, url, re.IGNORECASE)
        return match is not None
    except Exception:
        return False


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


# get the base sku from parent
def get_parent_sku(sku):
    return str(sku).strip().split("-")[0] if pd.notna(sku) else ""


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
    "XXL",
    "XS",
    "XXS",
}
