from bs4 import BeautifulSoup


def extract_flat_listings(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    listings = soup.select("a.css-qo0cxu")
    return listings


def extract_flat_details(listings):
    try:
        name = listings.select_one("h4.css-1g61gc2").text.strip()
    except (AttributeError, TypeError):
        name = "N/A"

    try:
        price = listings.select_one('p[data-testid="ad-price"]').text.strip()
    except (AttributeError, TypeError):
        price = "N/A"

    try:
        link = listings.get("href")
        if not link.startswith("http"):
            link = "https://www.olx.ro" + link
    except (AttributeError, TypeError):
        link = "N/A"

    print(f"Extracted {name}, {price}, {link}")
    return {"name": name, "price": price, "link": link}


def extract_pagination_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    page_numbers = []

    # li tag
    pagination_items = soup.select("li[data-testid='pagination-list-item']")
    for item in pagination_items:
        aria_label = str(item.get("aria-label", ""))
        try:
            page_number = int(aria_label.replace("Page ", "").strip())
            page_numbers.append(page_number)
        except ValueError:
            continue

    # a tag
    pagination_links = soup.select("a[data-testid^='pagination-link-']")
    for link in pagination_links:
        try:
            page_number = int(link.text.strip())
            page_numbers.append(page_number)
        except ValueError:
            continue

    return max(page_numbers) if page_numbers else 1
