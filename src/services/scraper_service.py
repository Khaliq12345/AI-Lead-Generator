from playwright.sync_api import (
    sync_playwright,
)
import os
import pandas as pd
from selectolax.parser import HTMLParser

TIMEOUT = 60000


def save_data(extracted_data: dict) -> str | None:
    output_file = "output.csv"
    if not extracted_data:
        return None
    df = pd.DataFrame([extracted_data])
    if os.path.isfile(output_file):
        df.to_csv(output_file, mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv(output_file, mode="w", header=True, index=False, encoding="utf-8")
    return output_file


def extract_data(
    html_source: str,
) -> str | None:
    extracted_data = {}
    tree = HTMLParser(html_source)
    if not tree:
        return None
    #
    # Extract Needed Data
    #
    # Save Data
    result = save_data(extracted_data)
    return result


def run(
    url: str,
) -> str | None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'test.csv')
    return csv_path
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        if os.path.exists("rel.json"):
            context = browser.new_context(storage_state="rel.json")
        else:
            return None
        page = context.new_page()
        page.goto(url, timeout=TIMEOUT)
        page.wait_for_load_state("load", timeout=TIMEOUT)
        html_source = page.content()
        # Extract Data
        result = extract_data(html_source)
        context.storage_state(path="rel.json")
        browser.close()
        return result


if __name__ == "__main__":
    run("")
