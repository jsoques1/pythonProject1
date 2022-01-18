"""
    Version 1.0 basic source with lots of print
    todo:
    * add specific exceptions and replace variables/functions with explicit names
    * add comments
    * check contents vs text
"""
import sys
import os
import logging
import requests
from bs4 import (BeautifulSoup, element)

URL_TO_SCRAP = "http://books.toscrape.com/"
LOGGING_FILE = "c:/temp/log.txt"
HTML_CONTENT_FILE = "c:/temp/html_contents.txt"
HTML_PRODUCT_FILE = "c:/temp/html_product.txt"
SCRAP_PARSER = "html.parser"
# SCRAP_PARSER = "lxml"


def start_logging():
    """add comment"""
    try:
        os.remove(LOGGING_FILE)
        logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG,
                            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

    except Exception as error:
        print("Unexpected exception: {}".format(error))


def make_html_parser(url, source_file=HTML_CONTENT_FILE):
    """add comment"""
    logging.debug("make_html_parser")

    # extract the main page of the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, SCRAP_PARSER)

    # # writing the html content prettified into a file
    # with open(source_file, "w") as html_file:
    #     try:
    #         html_file.write(soup.prettify())
    #
    #     except Exception as error:
    #         print("Unexpected exception: {}".format(error))
    #
    # with open(source_file) as fp:
    #     soup = BeautifulSoup(fp, SCRAP_PARSER)

    return soup


def get_all_books(soup):
    """add comment"""
    logging.debug("get_all_books")

    a = soup.find('div', class_="side_categories")
    return [a.ul.a.contents[0].strip(), a.ul.a.get('href')]


def get_all_books_category(soup):
    """add comment"""
    logging.debug("get_all_books_category")

    all_books_category = {}
    for a in soup.find_all('div', class_="side_categories"):
        for b in a.ul.ul.descendants:
            if isinstance(b, element.Tag):
                if len(b) == 1:
                    url = URL_TO_SCRAP + b.get('href')
                    category = b.contents[0].text.strip()
                    all_books_category[category] = url

    return all_books_category


def get_page_number_out_of_total(soup):
    """add comment"""
    logging.debug("get_page_number_out_of_total")

    li = soup.find('li', class_='current')
    current_page = li.text.strip()

    return current_page


def get_next_page(soup):
    """add comment"""
    logging.debug("get_next_page")

    li = soup.find('li', class_='next')
    url = None

    if li is not None:
        if li.a.get('href').startswith('catalogue'):
            url = URL_TO_SCRAP + li.a.get('href')
        else:
            url = URL_TO_SCRAP + 'catalogue/' + li.a.get('href')
    return url


def get_all_products_in_page_details(soup):
    """add comment"""
    logging.debug("get_all_products_in_page_details")

    all_products_details = []
    for h3 in soup.find_all('h3'):
        title = h3.a.get('title').strip()
        if h3.a.get('href').startswith('catalogue'):
            url = URL_TO_SCRAP + h3.a.get('href')
        else:
            url = URL_TO_SCRAP + 'catalogue/' + h3.a.get('href')
        all_products_details.append(get_a_product_details(title, url))
    return all_products_details


def get_a_product_details(title, url, html_product_file=HTML_PRODUCT_FILE):
    """add comment"""
    logging.debug("get_a_product_details")

    soup = make_html_parser(url, html_product_file)
    a = soup.find('div', class_='item active')
    if a is None:
        sys.exit(0)
    image_url = URL_TO_SCRAP + a.img.get('src').replace("../", "")
    table_data = [i.text for i in soup.find_all('td')]
    universal_product_code = table_data[0].strip()
    category = table_data[1].strip()
    price_including_tax = table_data[2].strip()
    price_excluding_tax = table_data[3].strip()
    number_available = table_data[5].strip()
    review_rating = table_data[6].strip()

    star_rating = soup.find('p', class_='star-rating')['class'][1]

    # uncomment those lines in stable source
    # return([title, image_url, universal_product_code, category, price_including_tax, price_excluding_tax,
    #         number_available, review_rating, star_rating])

    return [title]


def scrap_all_pages_collecting_books_details(soup, url, all_products_details=[], total_length=0):
    """add comment"""
    try:
        products_details = get_all_products_in_page_details(soup)
        current_page = get_page_number_out_of_total(soup)
        next_page_url = get_next_page(soup)

        print(f'examining current page={current_page} url={url}')
        length = len(products_details)
        total_length += length
        print(f'found {length} items total {total_length} items : {products_details}')
        all_products_details += products_details

        print(f'type(next_page_url)={type(next_page_url)}')
        print(f'next_page_url={next_page_url}')

        if next_page_url is not None:
            next_soup = make_html_parser(next_page_url, HTML_CONTENT_FILE)
            scrap_all_pages_collecting_books_details(next_soup, next_page_url,
                                                     all_products_details, total_length)

    except Exception as error:
        print("Unexpected exception: {}".format(error))

    return all_products_details


if __name__ == "__main__":
    """add comment"""
    start_logging()
    url = URL_TO_SCRAP
    soup = make_html_parser(url, HTML_CONTENT_FILE)
    get_all_books(soup)
    all_books_category = get_all_books_category(soup)
    scrap_all_pages_collecting_books_details(soup, url)

    sys.exit(0)
