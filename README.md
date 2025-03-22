# RentHunt Documentation

## Overview
RentHunt is a web scraping tool designed to extract apartment rental listings from OLX Romania. It collects essential details such as the apartment name, price, negotiability status, and the listing link. The extracted data can be saved in CSV or Excel formats for further analysis.

## Features
- Scrapes apartment listings from OLX Romania
- Extracts essential details including name, price, negotiability, and link
- Supports pagination to scrape multiple pages
- Saves data in CSV and Excel formats
- Handles interruptions and saves collected data before exit
- Implements random delays to mimic human-like browsing behavior

## Project Structure
```
RentHunt/
│-- config.py
│-- parser.py
│-- utils.py
│-- olx_scraper.py
│-- Data/ (output directory for scraped data)
```

## Files and Their Functions
### 1. `config.py`
This file contains configuration settings for the scraper, including:
- `BASE_URL`: URL of the OLX rental listings page.
- `HEADERS`: HTTP headers for making requests.
- `MIN_DELAY` & `MAX_DELAY`: Random delay range between requests.
- `OUTPUT_FILE`: Default output file name.

### 2. `parser.py`
This module handles HTML parsing using BeautifulSoup:
- `extract_flat_listings(html_content)`: Extracts all apartment listings from a webpage.
- `extract_flat_details(listings)`: Extracts name, price, negotiability, and link from a single listing.
- `extract_pagination_info(html_content)`: Determines the total number of available pages.

### 3. `utils.py`
Utility functions for handling data and delays:
- `create_dirs()`: Ensures the output directory exists.
- `random_delay(min_seconds, max_seconds)`: Introduces a random delay between requests.
- `save_to_csv(data, filename)`: Saves extracted data to a CSV file.
- `save_to_excel(data, filename)`: Saves extracted data to an Excel file.
- `generate_timestamp()`: Generates a timestamp for file naming.

### 4. `olx_scraper.py`
The main script that executes the web scraping process:
- Handles user input for selecting the number of pages to scrape and output format.
- Iterates through the listings and extracts apartment details.
- Saves data in the selected format (CSV, Excel, or both).
- Implements a signal handler to ensure data is saved if the script is interrupted.

## How to Use
1. **Install Dependencies**
   Ensure you have Python and the required libraries installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Scraper**
   Execute the scraper by running:
   ```bash
   python olx_scraper.py
   ```
   The script will prompt you to enter the number of pages to scrape and the preferred output format.

3. **View the Extracted Data**
   The scraped data is saved in the `Data/` directory in CSV and/or Excel formats.

## Example Output

| Name                      | Price   | Negotiable      | Link                                         |
|---------------------------|---------|----------------|----------------------------------------------|
| Apartament 2 camere Titan | 450 EUR | Negotiable     | [View Listing](https://www.olx.ro/d/oferta/123456789/) |
| Garsonieră Militari       | 300 EUR | Non-negotiable | [View Listing](https://www.olx.ro/d/oferta/987654321/) |
| Studio Central            | 500 EUR | Negotiable     | [View Listing](https://www.olx.ro/d/oferta/135792468/) |


## Error Handling & Interruption
- If the script is interrupted (CTRL+C), it will save the collected data before exiting.
- If a page request fails, it will display an error message and continue with the next page.
- If no listings are found, the script will terminate with an appropriate message.

## Disclaimer
RentHunt is intended for personal and educational use only. Users must comply with OLX's Terms of Service and avoid excessive requests that may violate their policies.

