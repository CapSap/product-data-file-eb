import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a product data file for distribution to EB customers, including url link to images"
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="in the product description, html tags will be removed",
    )
    return parser.parse_args()
