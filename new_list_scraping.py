from playwright.sync_api import sync_playwright, Page
import os
import pandas as pd


TIMEOUT = 120000
ALREADY_DONE = "already.txt"
INPUTS_FILE = "inputs.csv"
OUTPUT_FILE = "willsburg_output.csv"


def make_inputs(data_list, filename=INPUTS_FILE):
    df = pd.DataFrame(data_list, columns=["link"])
    df.to_csv(filename, index=False)
    print(f"{filename} créé avec {len(data_list)} liens.")


def load_inputs(filename=INPUTS_FILE):
    try:
        df = pd.read_csv(filename)
        return df["link"].dropna().tolist()
    except FileNotFoundError:
        print(f"Fichier {filename} introuvable.")
        return []


def load_already_processed(filename=ALREADY_DONE):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
        return list(set(links))
    except FileNotFoundError:
        print(f"Fichier {filename} introuvable.")
        return []


def save_data(extracted_data_list) -> str | None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(project_root, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    # filename = f"willsburg_output_{uid}.csv"
    output_file = os.path.join(outputs_dir, OUTPUT_FILE)
    if not extracted_data_list:
        return None
    df = pd.DataFrame(extracted_data_list)
    if os.path.isfile(output_file):
        df.to_csv(output_file, mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv(output_file, mode="w", header=True, index=False, encoding="utf-8")
    return output_file


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
                f"{data['Schools']} ; {value_c}"
                if (
                    ("Schools" in value_c)
                    or ("Elementary" in value_c)
                    or ("Junior High" in value_c)
                )
                else value_c
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
    page.wait_for_selector("div.truncate > a")
    property_lst = []
    next_btn = page.locator("button[title='Next page']")
    i = 0
    while next_btn:
        print("Got Next Btn")
        next_btn = None
        page.wait_for_selector("div.truncate > a")
        properties_rows = page.query_selector_all("div.truncate > a")
        print(f"Got {len(properties_rows)} rows for page")
        for pr in properties_rows:
            link = pr.get_attribute("href")
            property_lst.append(f"https://www.rel.network{link}")
        try:
            next_btn = page.locator("button[title='Next page']")
            if next_btn:
                next_btn.first.click(timeout=TIMEOUT)
                i += 1
        except Exception as e:
            print(f"No More Next Btn {e}")
            break
    return property_lst


def making_inputs(url: str, headless: bool):
    with sync_playwright() as p:
        try:
            browser = p.firefox.launch(headless=headless)
            context = browser.new_context(storage_state="rel.json")
            page = context.new_page()
            page.goto(url, timeout=TIMEOUT)
            page.wait_for_load_state("load", timeout=TIMEOUT)
            #
            page.click("button:has-text('View All Lists')", timeout=TIMEOUT)
            page.click("input[id='ListWilliamsburg ']", timeout=TIMEOUT)
            #
            property_lst = get_all_properties(page)
            #
            make_inputs(property_lst)
            #
            print("Input Made !!!")
            context.storage_state(path="rel.json")
            browser.close()
        except Exception as e:
            print(f"Error Making inputs{e}")


def run(url: str, headless: bool):
    with sync_playwright() as p:
        try:
            browser = p.firefox.launch(headless=headless)
            context = browser.new_context(storage_state="rel.json")
            page = context.new_page()
            
            all_links = load_inputs()
            print("Liens dans le fichier :", len(all_links))

            already_done = load_already_processed()
            print("Liens déjà traités :", len(already_done))

            new_links = [link for link in all_links if link not in already_done]
            print("Nouveaux liens à traiter :", len(new_links))
            #
            # For each Property
            #
            for ip, p in enumerate(new_links):
                page.goto(p, timeout=TIMEOUT)
                page.wait_for_load_state("load", timeout=TIMEOUT)
                #
                # Common Data from the first page
                common_data = get_main_data(page)
                # print(f"Common data : {common_data}")
                span = page.locator("nav[aria-label='Tabs'] span", has_text="Ownership")
                # Ownership Button
                if span.count() < 0:
                    return []
                print("Got Ownership Btn")
                span.first.click(timeout=TIMEOUT)
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
                for ir, row in enumerate(rows[1:]):
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
                    here_data["Adresses"] = cols[4].text_content()
                    # print(f"Got {len(cols)} Cols : {here_data}")
                    save_data([here_data])
                    print(
                        f" ------------ Saved {ir + 1} / {len(rows[1:])} --  {ip + 1} / {len(new_links)} Property"
                    )
                    with open("log.txt", "a+") as f:
                        f.write(
                            f" ------------ Saved {ir + 1} / {len(rows[1:])} --  {ip + 1} / {len(new_links)} Property"
                        )

                with open(ALREADY_DONE, "a+") as f:
                    f.write(f"{p}\n")

            print("Process ended !!!")
            context.storage_state(path="rel.json")
            browser.close()
        except Exception as e:
            print(f"Error {e}")


if __name__ == "__main__":
    # making_inputs("https://www.rel.network/account/my-lists", False)
    # run("https://www.rel.network/account/my-lists", False)
    ok = load_already_processed()
    print(ok)
