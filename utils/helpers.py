"""Helper functions"""

import re

# func that matches a sku with url text
def match_string_in_url(search_string, url):
    """
    # Pattern explanation:
    # (?:^|[_-]) - Match either start of string or a separator (non-capturing)
    # ({}) - Our search string
    # (?=[_-]|$) - Positive lookahead for either a separator or end of string
    """

    pattern = r'(?:^|[._-])({})(?=[._-]|$)'.format(re.escape(search_string))
    
    match = re.search(pattern, url, re.IGNORECASE)
    return match is not None
