import requests
import utils
import parser
import sys
import signal
import os
from config import BASE_URL, HEADERS, MIN_DELAY, MAX_DELAY


all_listings = []
format_choice = ""


def get_project_dir():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    return project_root


def signal_handler(signal, frame):
    print("Program interrupted, saving the data that has been collected so far")

    if all_listings:
        utils.create_dirs()

        project_root = get_project_dir()
        data_dir = os.path.join(project_root, "Data")

        timestamp = utils.generate_timestamp()
        csv_filename = os.path.join(data_dir, f"Data/olx_listings_{timestamp}.csv")
        excel_filename = os.path.join(data_dir, f"Data/olx_listings_{timestamp}.xlsx")

        if format_choice == "1":
            utils.save_to_csv(all_listings, csv_filename)
            print(
                f"SCRAPING INTERRUPTED! Processed {len(all_listings)} ads | Saved as CSV in {csv_filename}"
            )

        if format_choice == "2":
            utils.save_to_excel(all_listings, excel_filename)
            print(
                f"SCRAPING INTERRUPTED! Processed {len(all_listings)} ads | Saved as EXCEL in {excel_filename}"
            )

        if format_choice == "3":
            utils.save_to_excel(all_listings, excel_filename)
            utils.save_to_csv(all_listings, csv_filename)
            print(
                f"SCRAPING INTERRUPTED! Processed {len(all_listings)} ads | Saved as CSV in {csv_filename} and as EXCEL in {excel_filename}"
            )
    else:
        print("No data has been collected so far, nothing to save")

    sys.exit(0)


def scrape_olx():
    global all_listings

    signal.signal(signal.SIGINT, signal_handler)

    utils.create_dirs()
    project_root = get_project_dir()
    data_dir = os.path.join(project_root, "Data")
    all_listings = []

    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error trying to acces the BASE_URL")
        return

    max_pages = parser.extract_pagination_info(response.text)
    print(f"Total no pages: {max_pages}")

    while True:
        try:
            user_pages = int(
                input(f"How many pages do you want to scrape? (max {max_pages}): ")
            )
            if 1 <= user_pages <= max_pages:
                break
            else:
                print(f"Please enter a value between 1 and {max_pages}")
        except ValueError:
            print("Invalid input, please enter a valid integer")

    while True:
        global format_choice
        format_choice = input("Save as (1) CSV, (2) Excel, (3) Both: ").strip()
        if format_choice in ["1", "2", "3"]:
            break
        else:
            print("Invalid choice, please enter 1, 2 or 3")
    try:
        for page in range(1, user_pages + 1):
            url = f"{BASE_URL}?page={page}"
            print(f"Trying to access page {page}: {url}")

            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Error accessing page {page}")
                continue

            listings_html = parser.extract_flat_listings(response.text)
            if not listings_html:
                print("Can't parse the listings")
                return None
            for listing in listings_html:
                details = parser.extract_flat_details(listing)
                all_listings.append(details)

            utils.random_delay(MIN_DELAY, MAX_DELAY)

        timestamp = utils.generate_timestamp()
        csv_filename = os.path.join(data_dir, f"Data/olx_listings_{timestamp}.csv")
        excel_filename = os.path.join(data_dir, f"Data/olx_listings_{timestamp}.xlsx")

        if format_choice == "1":
            utils.save_to_csv(all_listings, csv_filename)
            print(
                f"SCRAPING COMPLETED! Processed {len(all_listings)} ads | Saved as CSV in {csv_filename}"
            )

        if format_choice == "2":
            utils.save_to_excel(all_listings, excel_filename)
            print(
                f"SCRAPING COMPLETED! Processed {len(all_listings)} ads | Saved as EXCEL in {excel_filename}"
            )

        if format_choice == "3":
            utils.save_to_excel(all_listings, excel_filename)
            utils.save_to_csv(all_listings, csv_filename)
            print(
                f"SCRAPING COMPLETED! Processed {len(all_listings)} ads | Saved as CSV in {csv_filename} and as EXCEL in {excel_filename}"
            )
    except Exception as e:
        print(f"An error has occured: {e}")
        signal_handler(None, None)


if __name__ == "__main__":
    scrape_olx()
