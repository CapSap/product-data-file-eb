import pandas as pd


def test_find_html_description():
    # Create sample test data
    test_data = {
        "Variant SKU": [
            "1025979-35",  # Should match
            "1025979-36",  # Should match
            "1025979-37",  # Should match
            "different-sku",  # Should not match
        ],
        "Body HTML": [
            "",  # Empty, should be filled
            "<p>Original</p>",  # Has content, should keep original
            None,  # None, should be filled
            "<p>Other</p>",  # Different SKU, should keep original
        ],
    }

    test_df = pd.DataFrame(test_data)

    # Create HTML map with sample data
    html_map = {"1025979": "<p>Test Description</p>"}

    # Test function
    def find_html_description(row):
        sku_prefix = row["Variant SKU"].split("-")[0]
        return html_map.get(sku_prefix, row["Body HTML"])

    # Apply the function
    test_df["Body HTML"] = test_df.apply(find_html_description, axis=1)

    # Assertions
    assert (
        test_df.loc[0, "Body HTML"] == "<p>Test Description</p>"
    ), "Failed to fill empty HTML"
    assert (
        test_df.loc[1, "Body HTML"] == "<p>Original</p>"
    ), "Incorrectly overwrote existing HTML"
    assert (
        test_df.loc[2, "Body HTML"] == "<p>Test Description</p>"
    ), "Failed to fill None HTML"
    assert (
        test_df.loc[3, "Body HTML"] == "<p>Other</p>"
    ), "Incorrectly modified non-matching SKU"

    print("All tests passed!")
    return test_df


# Run the test
if __name__ == "__main__":
    result_df = test_find_html_description()
    print("\nResulting DataFrame:")
    print(result_df)
