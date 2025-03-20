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

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?page={page}"
        print(f"Trying to access page {page}: {url}")

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error accessing page {page}")
            continue

        listings_html = parser.extract_flat_listings(response.text)
        for listing in listings_html:
            details = parser.extract_flat_details(listing)
            all_listings.append(details)

        utils.random_delay(MIN_DELAY, MAX_DELAY)

    timestamp = utils.generate_timestamp()
    filename = f"data/olx_listings_{timestamp}.csv"
    utils.save_to_csv(all_listings, filename)

    print(f"SCRAPING COMPLETED! Saved {len(all_listings)} ads in {filename}")


if __name__ == "__main__":
    scrape_olx()
