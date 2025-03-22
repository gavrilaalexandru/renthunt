import requests
import utils
import parser
from config import BASE_URL, HEADERS, MIN_DELAY, MAX_DELAY


def scrape_olx():
    utils.create_dirs()
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

    while True:
        format_choice = input("Save as (1) CSV, (2) Excel, (3) Both: ").strip()
        if format_choice in ["1", "2", "3"]:
            break
        else:
            print("Invalid choice, please enter 1, 2 or 3")

    timestamp = utils.generate_timestamp()
    csv_filename = f"Data/olx_listings_{timestamp}.csv"
    excel_filename = f"Data/olx_listings_{timestamp}.xlsx"

    if format_choice in ["1", "3"]:
        utils.save_to_csv(all_listings, csv_filename)
        print(f"Saved {len(all_listings)} ads in {csv_filename}")

    if format_choice in ["2", "3"]:
        utils.save_to_excel(all_listings, excel_filename)
        print(f"Saved {len(all_listings)} ads in {excel_filename}")

    print(f"SCRAPING COMPLETED! Processed {len(all_listings)} ads.")


if __name__ == "__main__":
    scrape_olx()
