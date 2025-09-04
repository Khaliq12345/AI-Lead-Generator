from playwright.sync_api import sync_playwright, Page
import os

# from datetime import datetime
import pandas as pd
from src.core import config

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
outputs_dir = os.path.join(project_root, "outputs")
file_path = os.path.join(outputs_dir, "output_beta.csv")
TIMEOUT = 60000


def get_existing_property_links() -> list[str]:
    if not os.path.isfile(file_path):
        print(f"Fichier introuvable : {file_path}")
        return []
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        if "Property Link" not in df.columns:
            print("Colonne 'Property Link' absente dans le fichier.")
            return []
        return df["Property Link"].dropna().unique().tolist()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return []


def save_data(extracted_data_list) -> str | None:
    if not extracted_data_list:
        return None
    # Convertir la nouvelle data en DataFrame
    new_df = pd.DataFrame(extracted_data_list)

    if os.path.isfile(file_path):
        # Charger l'ancien fichier
        old_df = pd.read_csv(file_path, encoding="utf-8")

        # Concaténer et réaligner les colonnes (remplit NaN pour colonnes manquantes)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)

        # Réécrire le fichier complet avec nouveau header
        combined_df.to_csv(file_path, index=False, encoding="utf-8")
    else:
        # Première écriture
        new_df.to_csv(file_path, index=False, encoding="utf-8")
    return file_path


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
            and (
                ("School" in title_c)
                or ("High" in title_c)
                or ("Elementary" in title_c)
            )
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
    try:
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
            for j in range(1, 4):  # cells.count()):
                key = f"Buildable SF {row_title} {header_texts[j]}"
                value = cells.nth(j).inner_text().strip()
                data[key] = value
    except Exception as e:
        print(f"Errorr getting table : {e}")

    return data


def get_all_properties(page: Page):
    property_lst = []  # ["https://www.rel.network/property/1005930036", "https://www.rel.network/property/1017540155"]
    next_btn = page.locator("button[title='Next page']", has_text="Next")
    next_disabled = next_btn.first.get_attribute("disabled")
    print(f"Next Disabled : {next_disabled}")
    i = 0
    # page.pause()
    while not next_disabled:
        print("Got Next Btn")
        next_btn = None
        page.wait_for_selector("div.truncate > a")
        properties_rows = page.query_selector_all("div.truncate > a")
        print(f"Got {len(properties_rows)} rows for page")
        for pr in properties_rows:
            link = pr.get_attribute("href")
            property_lst.append(f"https://www.rel.network{link}")
        try:
            next_btn = page.locator("button[title='Next page']", has_text="Next")
            next_disabled = next_btn.first.get_attribute("disabled")
            if next_btn:
                next_btn.first.click()
                i += 1
        except Exception as e:
            print(f"No More Next Btn {e}")
            break
    return property_lst


def run(headless: bool):
    os.makedirs(outputs_dir, exist_ok=True)
    with sync_playwright() as p:
        try:
            main_url = "https://www.rel.network/account/my-lists"
            browser = p.firefox.launch(headless=headless)
            context = browser.new_context(storage_state=config.REL_PATH)
            page = context.new_page()
            page.goto(main_url, timeout=TIMEOUT)
            page.wait_for_load_state("load", timeout=TIMEOUT)
            final_list = []
            property_lst = get_all_properties(page)
            already_done_links = get_existing_property_links()
            #
            # For each Property
            #
            for index, p in enumerate(property_lst):
                print(f"Scraping link {index + 1} / {len(property_lst)}")
                if p in already_done_links:
                    print("deja fait ")
                    continue
                try:
                    page.goto(p, timeout=TIMEOUT)
                    page.wait_for_load_state("load", timeout=TIMEOUT)
                except Exception as e:
                    print(f"Unable to load {e}")
                    continue
                #
                # Common Data from the first page
                try:
                    common_data = get_main_data(page)
                    common_data["Property Link"] = p
                except Exception as e:
                    print(f"Unable to get_main_data {e}")
                    continue
                # print(f"Common data : {common_data}")
                span = page.locator("nav[aria-label='Tabs'] span", has_text="Ownership")
                # Ownership Button
                if span.count() < 0:
                    print("No Ownership Btn")
                    save_data([common_data.copy()])
                    final_list.append(common_data.copy())
                    continue
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
                if len(rows) == 0:
                    save_data([common_data.copy()])
                    final_list.append(common_data.copy())
                    continue
                print(f"Got {len(rows)} Ownership Rows !")
                for row in rows[1:]:
                    cols = row.query_selector_all("> div")
                    here_data = common_data.copy()
                    # Owner Name
                    here_data["Owner Name"] = cols[0].text_content()
                    # Company
                    here_data["Company"] = " -- ".join(
                        [
                            (tmp.text_content() or "").strip()
                            for tmp in (cols[1].query_selector_all("> div") or [])
                        ]
                    )
                    # Phone
                    phone_lst = (
                        [
                            (tmp.text_content() or "").strip()
                            for tmp in (cols[2].query_selector_all("a") or [])
                        ]
                        if cols[2].text_content() != "Search"
                        else []
                    )
                    for i, ph in enumerate(phone_lst):
                        here_data[f"Phone {i + 1}"] = ph
                    # Email
                    emails_lst = (
                        [
                            (tmp.text_content() or "").strip()
                            for tmp in (cols[3].query_selector_all("a") or [])
                        ]
                        if cols[3].text_content() != "Search"
                        else []
                    )
                    for i, em in enumerate(emails_lst):
                        here_data[f"Email {i + 1}"] = em
                    #
                    here_data["Adresses"] = cols[4].text_content()
                    # print(f"Got {len(cols)} Cols : {here_data}")
                    save_data([here_data])
                    final_list.append(here_data)
            print("Process ended !!!")
            # print(final_list)
            # save_data(final_list)
            # page.pause()
            context.storage_state(path=config.REL_PATH)
            browser.close()
            return final_list
        except Exception as e:
            print(f"Error {e}")
            return []


if __name__ == "__main__":
    run(False)
