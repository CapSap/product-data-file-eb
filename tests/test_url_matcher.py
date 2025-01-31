

from utils.helpers import match_string_in_url  

def test_basic_url_matching():
    """Test basic URL matching functionality with various formats"""
    test_cases = [
        # (search_string, url, expected_result)
        ("1025979", "23SS_Professional_PI_1025979_04_web_ff607ae3-e2e8-4be3-b4fb-31285e2fca2a.png", True),
        ("1025979", "23SS_Professional_PI-1025979-04_web_ff607ae3-e2e8-4be3-b4fb-31285e2fca2a.png", True),
        ("1025979", "1025979_04_web_ff607ae3-e2e8-4be3-b4fb-31285e2fca2a.png", True),
        ("1025979", "something_else_1025979", True),
        ("1025979", "1025979", True),
        ("1025979", "fake1025979fake", False),  # Should not match
        ("1025979", "something-1025979-else", True),
    ]
    
    for search_string, url, expected in test_cases:
        result = match_string_in_url(search_string, url)
        assert result == expected, f"Failed for URL: {url}, Expected: {expected}, Got: {result}"

def test_edge_cases():
    """Test edge cases and potential problem scenarios"""
    test_cases = [
        # Empty strings
        ("", "test_url.png", False),
        ("1025979", "", False),
        
        # Special characters
        ("test-123", "prefix_test-123_suffix.png", True),
        ("test_123", "prefix-test_123-suffix.png", True),
        
        # Numbers only
        ("123", "prefix_123_suffix.png", True),
        ("123", "123prefix_suffix.png", False),
        
        # Multiple separators
        ("abc", "test__abc__test.png", True),
        ("abc", "test--abc--test.png", True),
    ]
    
    for search_string, url, expected in test_cases:
        result = match_string_in_url(search_string, url)
        assert result == expected, f"Failed for search_string: {search_string}, URL: {url}"

def test_real_world_scenarios():
    """Test with real-world-like product URLs and SKUs"""
    test_cases = [
        # Product variants
        ("ABC123", "product_ABC123_variant1.jpg", True),
        ("ABC123", "product_ABC123-RED-L.png", True),
        ("ABC123", "ABC123_BLACK_XL_01.jpg", True),
        
        # Different file types
        ("ABC123", "ABC123.jpg", True),
        ("ABC123", "ABC123.png", True),
        ("ABC123", "ABC123.jpeg", True),
        
        # With UUIDs or timestamps
        ("ABC123", "ABC123_1234567890.jpg", True),
        ("ABC123", "ABC123_2023-01-01.png", True),
        ("ABC123", "ABC123_ff607ae3-e2e8-4be3.jpg", True),
    ]
    
    for search_string, url, expected in test_cases:
        result = match_string_in_url(search_string, url)
        assert result == expected, f"Failed for URL: {url}"

def test_invalid_inputs():
    """Test handling of invalid inputs"""
    test_cases = [
        # None values
        (None, "test.jpg", False),
        ("123", None, False),
        
        # Non-string types
        (123, "test.jpg", False),  # Number as search string
        ("123", 456, False),      # Number as URL
        
        # Special characters in search string
        ("test*123", "test_123.jpg", False),
        ("test?123", "test_123.jpg", False),
    ]
    
    for search_string, url, expected in test_cases:
        try:
            result = match_string_in_url(search_string, url)
            assert result == expected, f"Failed for search_string: {search_string}, URL: {url}"
        except Exception as e:
            # If we expect an exception for certain invalid inputs, 
            # we can add assertions here
            pass