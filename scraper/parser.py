from bs4 import BeautifulSoup


def extract_flat_listings(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    listings = soup.select("div.css-j0t2x2 > div.css-l9drzq")
    return listings


def extract_flat_details(listings):
    try:
        name = listings.select_one("h4.css-1g61gc2").text.strip()
    except (AttributeError, TypeError):
        name = "N/A"

    try:
        # price_element = listings.find("p", {"data-testid": "ad-price"})
        # price = price_element.text.strip()
        # price = listings.select_one('p[data-testid="ad-price"]').text.strip()
        price_element = listings.select_one("p.css-6j1qjp")
        if price_element:
            negotiable_span = price_element.select_one("span.css-1hc4lz9")
            if negotiable_span:
                negotiable_span.extract()
                negotiable = True
            else:
                negotiable = False
            price = price_element.get_text(strip=True)
        else:
            price = "N/A"
            negotiable = False
    except (AttributeError, TypeError):
        price = "N/A"
        negotiable = False

    try:
        link_tag = listings.select_one("a.css-qo0cxu")
        if link_tag and link_tag.has_attr("href"):
            link = link_tag["href"]
            if not link.startswith("http"):
                link = "https://www.olx.ro" + link
        else:
            link = "N/A"
    except (AttributeError, TypeError):
        link = "N/A"

    print(f"Extracted {name}, {price}, {negotiable}, {link}")
    return {"name": name, "price": price, "negotiable": negotiable, "link": link}


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
