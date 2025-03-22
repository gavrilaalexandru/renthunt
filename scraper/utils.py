import time
import random
import os
import csv
from datetime import datetime
import pandas as pd


def create_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    os.makedirs(os.path.join(root_dir, "Data"), exist_ok=True)


def random_delay(min_seconds=1, max_seconds=3):
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def save_to_csv(data, filename):
    if not data:
        print("No data found")
        return

    fieldnames = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        w = csv.DictWriter(csvfile, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data)


def save_to_excel(data, filename):
    if not data:
        print("No data found")
        return

    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="OLX Listings")

    workbook = writer.book
    worksheet = writer.sheets["OLX Listings"]

    header_format = workbook.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    price_format = workbook.add_format({"num_format": "€#,##0"})
    if "price" in df.columns:
        price_col_idx = df.columns.get_loc("price")
        worksheet.set_column(price_col_idx, price_col_idx, None, price_format)

    if "link" in df.columns:
        link_col_idx = df.columns.get_loc("link")
        for row_num, link in enumerate(df["link"]):
            if link != "N/A" and isinstance(link, str):
                # row_num+1 because we're skipping the header row
                worksheet.write_url(row_num + 1, link_col_idx, link, string=link)

    for column_idx, column in enumerate(df.columns):
        column_len = max(df[column].astype(str).map(len).max(), len(column))
        worksheet.set_column(column_idx, column_idx, column_len + 2)

    writer.close()


def generate_timestamp():
    return datetime.now().strftime("%d%m%Y_%H%M%S")
