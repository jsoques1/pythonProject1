"""
    Version 1.0 basic source with lots of print
    todo:
    * add specific exceptions and replace variables/functions with explicit names
    * add comments
    * check contents vs text
"""

import os
import re
import shutil
import sys
import time
import csv
import logging
import requests
from bs4 import (BeautifulSoup, element)

URL_TO_SCRAP = 'http://books.toscrape.com/'
SCRAP_PARSER = 'html.parser'
DEFAULT_LOGGING_DIR = 'c:/temp/P2/log/'
DEFAULT_LOGGING_FILE_NAME = 'log.txt'
DEFAULT_IMG_DIR = 'c:/temp/P2/img/'
DEFAULT_CSV_DIR = 'c:/temp/P2/csv/'
DEFAULT_CSV_HEADER = ['title', 'image_url', 'universal_product_code', 'category', 'price_including_tax',
                      'price_excluding_tax', 'number_available', 'review_rating', 'star_rating']


def clean_up_previous_results():
    try:
        if os.path.isdir(DEFAULT_LOGGING_DIR):
            shutil.rmtree(DEFAULT_LOGGING_DIR)
        if os.path.isdir(DEFAULT_CSV_DIR):
            shutil.rmtree(DEFAULT_CSV_DIR)
        if os.path.isdir(DEFAULT_IMG_DIR):
            shutil.rmtree(DEFAULT_IMG_DIR)

        os.makedirs(DEFAULT_LOGGING_DIR)
        os.makedirs(DEFAULT_CSV_DIR)
        os.makedirs(DEFAULT_IMG_DIR)

    except Exception as error:
        print(f'Unexpected exception in clean_up_previous_results(): {error}')


def start_logging():
    """add comment"""
    try:
        logging_file_path = DEFAULT_LOGGING_DIR + DEFAULT_LOGGING_FILE_NAME
        if os.path.isfile(logging_file_path):
            os.remove(logging_file_path)

        if not os.path.isdir(DEFAULT_LOGGING_DIR):
            os.makedirs(DEFAULT_LOGGING_DIR)

        open(logging_file_path, 'w').close()

        logging.basicConfig(filename=logging_file_path, level=logging.DEBUG,
                            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
        logging.debug("start_logging")

    except Exception as error:
        print(f'Unexpected exception in start_logging(): {error}')


def make_html_parser(url):
    """add comment"""
    logging.debug("make_html_parser")

    # extract the main page of the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, SCRAP_PARSER)
    return soup


def get_all_books(soup):
    """add comment"""
    logging.debug("get_all_books")

    a = soup.find('div', class_="side_categories")
    books = a.ul.a.contents[0].strip()
    books_url = URL_TO_SCRAP + 'catalogue/' + a.ul.a.get('href')
    return {books: books_url}


def get_all_books_category(soup):
    """add comment"""
    logging.debug("get_all_books_category")

    all_books_category = {}
    for a in soup.find_all('div', class_="side_categories"):
        for b in a.ul.ul.descendants:
            if isinstance(b, element.Tag):
                if len(b) == 1:
                    url = URL_TO_SCRAP + 'catalogue/' + b.get('href')
                    category = b.contents[0].text.strip()
                    all_books_category[category] = url

    return all_books_category


def get_page_number_out_of_total(soup):
    """add comment"""
    logging.debug("get_page_number_out_of_total")

    current_page = None
    li = soup.find('li', class_='current')
    if li is not None:
        current_page = li.text.strip()

    return current_page


def get_next_page(soup, url):
    """add comment"""
    logging.debug("get_next_page")

    li = soup.find('li', class_='next')
    next_url = None

    if li is not None:
        next_url = url[:url.rfind("/")] + '/' + li.a.get('href')

    return next_url


def get_all_products_in_page_details(soup, product_category='Books'):
    """add comment"""
    logging.debug("get_all_products_in_page_details")

    all_products_details = []
    for h3 in soup.find_all('h3'):
        title = h3.a.get('title').strip()
        #print(f"h3 title={title} {h3.a.get('href')}")
        if h3.a.get('href').startswith('catalogue'):
            url = URL_TO_SCRAP + h3.a.get('href')
        elif h3.a.get('href').startswith('../'):
            url = URL_TO_SCRAP + 'catalogue/' + h3.a.get('href').replace('../', '')
        else:
            url = URL_TO_SCRAP + 'catalogue/' + h3.a.get('href')
        all_products_details.append(get_a_product_details(title, url, product_category))
    return all_products_details


def get_a_product_details(title, url, product_category='Books'):
    """add comment"""
    logging.debug("get_a_product_details")

    soup = make_html_parser(url)
    a = soup.find('div', class_='item active')
    if a is None:
        # lever une exception
        # todo
        return []

    image_url = URL_TO_SCRAP + a.img.get('src').replace("../", "")
    table_data = [i.text for i in soup.find_all('td')]
    universal_product_code = table_data[0].strip()
    category = product_category
    price_including_tax = table_data[2].strip()
    price_excluding_tax = table_data[3].strip()
    number_available = table_data[5].strip()
    review_rating = table_data[6].strip()
    star_rating = soup.find('p', class_='star-rating')['class'][1]

    return [title, image_url, universal_product_code, category, price_including_tax, price_excluding_tax,
            number_available, review_rating, star_rating]


def scrap_all_pages_collecting_books_details(soup, url, all_products_details=[], total_length=0, product_category='Books'):
    """add comment"""
    logging.debug("scrap_all_pages_collecting_books_details")

    try:
        products_details = get_all_products_in_page_details(soup, product_category)
        current_page = get_page_number_out_of_total(soup)
        next_page_url = get_next_page(soup, url)

        if current_page is None:
            trace_info = f'examining Page 1 of 1 url={url}'
        else:
            trace_info = f'examining {current_page} url={url}'
        print(trace_info)
        logging.info(trace_info)
        length = len(products_details)
        total_length += length
        trace_info = f'found {length} items total {total_length} items : {products_details}'
        logging.info(trace_info)
        all_products_details += products_details

        if next_page_url is not None:
            next_soup = make_html_parser(next_page_url)
            scrap_all_pages_collecting_books_details(next_soup, next_page_url,
                                                     all_products_details, total_length, product_category)

    except Exception as error:
        print(f'Unexpected exception in scrap_all_pages_collecting_books_details(): {error}')

    return all_products_details


def write_to_csv(csv_dir=DEFAULT_CSV_DIR, csv_header=DEFAULT_CSV_HEADER, csv_contents=[], product_category='Books'):
    """add comment"""
    logging.debug("write_to_csv")

    csv_file = csv_dir + product_category.replace(' ', '_') + '.csv'

    try:
        with open(csv_file, "w", newline='') as fopen:  # Open the csv file.
            csv_writer = csv.writer(fopen, delimiter='\t')
            csv_writer.writerow(csv_header)
            for csv_row in csv_contents:
                csv_writer.writerow(csv_row)

    except Exception as error:
        print(f'Unexpected exception in write_to_csv(): {error}')
        return False

    return True


def extract_images_from_all_products_details(all_product_details, img_dir=DEFAULT_IMG_DIR, product_category='Books'):
    img_dir += product_category.replace(' ', '_') + '/'
    try:
        number_of_images = len(all_product_details)
        print(f'extracting {number_of_images} image files into {img_dir}')

        os.makedirs(img_dir)
    except Exception as error:
        print(f'Unexpected exception in extract_images_from_all_products_details(): {error} raised for {img_dir}')
        return False
    
    try:    
        for product_details in all_product_details:
            product_url = product_details[1]
            request = requests.get(product_url, allow_redirects=True)
            img_name_file = img_dir + product_url.rsplit('/', 1)[-1]
            open(img_name_file, 'wb').write(request.content)

    except Exception as error:
        print(f'Unexpected exception in extract_images_from_all_products_details(): {error}')
        return False
    
    return True

if __name__ == "__main__":
    """add comment"""

    clean_up_previous_results()
    start_logging()
    # url = URL_TO_SCRAP
    url = 'http://books.toscrape.com/catalogue/page-49.html'
    soup = make_html_parser(url)
    all_books = get_all_books(soup)
    all_books_category = all_books | get_all_books_category(soup)

    for books_category in all_books_category.keys():
        all_products_details = []
        url = all_books_category[books_category]
        print(f'processing books_category={books_category} url={url}')
        soup = make_html_parser(url)
        all_products_details = scrap_all_pages_collecting_books_details(soup, url, all_products_details=[], product_category=books_category)
        write_to_csv(csv_contents=all_products_details, product_category=books_category)
        extract_images_from_all_products_details(all_products_details, product_category=books_category)
        print()

    sys.exit(0)
