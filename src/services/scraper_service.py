from datetime import datetime
from playwright.sync_api import (
    sync_playwright,
)
import os
import pandas as pd
from selectolax.parser import HTMLParser

TIMEOUT = 60000


def save_data(extracted_data: dict) -> str | None:
    uid = str(int(datetime.now().timestamp()))
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(project_root, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    filename = f"output_{uid}.csv"
    output_file = os.path.join(outputs_dir, filename)
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
    extracted_data = {
        "title": "hello",
        "content": "world",
    }
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
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, "rel.json")
        context = browser.new_context(storage_state=json_path)
        page = context.new_page()
        page.goto(url, timeout=TIMEOUT)
        page.wait_for_load_state("load", timeout=TIMEOUT)
        html_source = page.content()
        # Extract Data
        result = extract_data(html_source)
        context.storage_state(path=json_path)
        browser.close()
        return result


if __name__ == "__main__":
    run("")
