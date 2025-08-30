from datetime import datetime
from playwright.sync_api import sync_playwright, Page
import os
import pandas as pd
from selectolax.parser import HTMLParser

TIMEOUT = 60000


def get_main_data(page: Page):
    data = {}
    #
    # Simple Data
    #
    all_to_map = page.query_selector_all(
        "div.px-5.py-4.text-sm > div.grid.grid-flow-col"
    )
    print(f"Got To Map {len(all_to_map)}")
    for i, to_map in enumerate(all_to_map):
        title = to_map.query_selector("> span")
        title_c = title.text_content() if title else None
        value = to_map.query_selector("> span.text-right")
        value_c = value.text_content() if value else None
        # For Local Representatives
        if title_c == "Local Representatives" and value:
            value = value.query_selector("> a")
            value_c = value.get_attribute("href") if value else ""
        # For Sub Units
        if title_c == "Residential Units (DOF)" or title_c == "Rent Stabilized Units":
            title_c = f"Units {title_c}"
        # For Schools
        if (
            title_c
            and value_c
            and ("School" in title_c)
            and (title_c != "School District")
        ):
            data["Schools"] = (
                f"{data['Schools']} ; {value_c}" if ("Schools" in data) else value_c
            )
            continue
        # For Normals
        if title_c and value_c:
            data[title_c] = value_c
    #
    # Table
    #
    table = page.locator("div.px-5.py-4 table.text-right.w-full")
    headers = table.locator("thead tr th")
    header_texts = [
        headers.nth(i).inner_text().strip().replace("\n", " ")
        for i in range(4)  # headers.count())
    ]
    print("headers texte : ", header_texts)
    rows = table.locator("tbody tr")

    for i in range(3):  # rows.count()):
        row = rows.nth(i)
        cells = row.locator("td")
        print(f"Row {i} -- cells {len(cells.all())}")
        row_title = cells.nth(0).inner_text().strip()
        for j in range(1, cells.count()):
            key = f"Buildable SF {row_title} {header_texts[j]}"
            value = cells.nth(j).inner_text().strip()
            data[key] = value

    return data


def save_data(extracted_data_list) -> str | None:
    uid = str(int(datetime.now().timestamp()))
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(project_root, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    filename = f"output_{uid}.csv"
    output_file = os.path.join(outputs_dir, filename)
    if not extracted_data_list:
        return None
    df = pd.DataFrame(extracted_data_list)
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
        final_list = []
        #
        # Common Data from the first page
        common_data = get_main_data(page)
        # print(f"Common data : {common_data}")
        span = page.locator("nav[aria-label='Tabs'] span", has_text="Ownership")

        # Ownership Button
        if span.count() > 0:
            print("Got Ownership Btn")
            span.first.click()
            print("Clicked")
            try:
                page.wait_for_selector(
                    "div.flex.flex-col.flex-grow.h-full > div.grid.grid-flow-col"
                )
            except Exception as e:
                print(e)
            print("Waited")
            rows = page.query_selector_all(
                "div.flex.flex-col.flex-grow.h-full > div.grid.grid-flow-col"
            )
            print(f"Got {len(rows)} Ownership Rows !")
            for row in rows[1:]:
                cols = row.query_selector_all("> div")
                here_data = common_data.copy()
                here_data["Owner_Name"] = cols[0].text_content()
                here_data["Company"] = cols[1].text_content()
                here_data["Phone"] = (
                    cols[2].text_content() if cols[2].text_content() != "Search" else ""
                )
                here_data["Email"] = (
                    cols[3].text_content() if cols[3].text_content() != "Search" else ""
                )
                here_data["Adresses"] = cols[4].text_content()
                # print(f"Got {len(cols)} Cols : {here_data}")
                final_list.append(here_data)
        print("Process ended !!!")
        result = save_data(final_list)
        print("Output Wrote")
        context.storage_state(path=json_path)
        browser.close()
        return result


if __name__ == "__main__":
    run("")
