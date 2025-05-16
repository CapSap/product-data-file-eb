from utils.helpers import get_parent_sku


def test_get_parent_sku():
    test_cases = [
        ("ABC-123", "ABC"),
        ("SKU-456-BLU", "SKU"),
        ("ONLYONEPART", "ONLYONEPART"),
        ("123-456-789", "123"),
        ("-STARTSWITHDASH", ""),  # Splitting will return "" as the first element
        (None, ""),  # Should return empty string on None
        ("", ""),  # Empty string input should return ""
        (12345, "12345"),  # Non-string input should be stringified
        ("   ", ""),  # Just whitespace
    ]

    for input_sku, expected in test_cases:
        result = get_parent_sku(input_sku)
        assert result == expected, f"Failed for input: {input_sku}, Got: {result}"
