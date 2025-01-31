"""Helper functions"""

import re


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
