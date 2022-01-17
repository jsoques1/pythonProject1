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

def start_logging():
    try:
        os.remove(LOGGING_FILE)
        logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG,
                            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

    except Exception as error:
        print("Unexpected exception: {}".format(error))

def make_html_parser(url, source_file=HTML_CONTENT_FILE):
    logging.debug("make_html_parser")

    # extract the main page of the website
    main_page = requests.get(url)
    soup = BeautifulSoup(main_page.content, SCRAP_PARSER)

    # writing the html content prettified into a file
    with open(source_file, "w") as html_file:
        try:
            html_file.write(soup.prettify())

        except Exception as error:
            print("Unexpected exception: {}".format(error))

    with open(source_file) as fp:
        soup = BeautifulSoup(fp, SCRAP_PARSER)

    return(soup)

def get_all_books(soup):
    logging.debug("get_all_books")

    for a in soup.find_all('div', class_="side_categories"):
        print(a.ul.a.get('href'))
        print(a.ul.a.contents[0].strip())
        print("======================================")

def get_all_books_category(soup):
    logging.debug("get_all_books_category")

    all_books_category = {}
    for a in soup.find_all('div', class_="side_categories"):
        for b in a.ul.ul.descendants:
            if isinstance(b, element.Tag):
                if len(b) == 1:
                    url = URL_TO_SCRAP + b.get('href')
                    category = b.contents[0].text.strip()
                    all_books_category[category]=url

    print(f'all books category={all_books_category}')
    print("============================")
    return(all_books_category)

def get_page_number_out_of_total(soup):
    logging.debug("get_page_number_out_of_total")

    for li in soup.find('li', class_='current'):
        current_page = li.text.strip()
        print(f'current page={current_page}')
        print("============================")

def get_next_page(soup):
    logging.debug("get_next_page")

    li=soup.find('li', class_='next')
    if li != None:
        url = URL_TO_SCRAP + li.a.get('href')
        print(f'next page is at {url}')
        print("============================")
    return(url)

def get_all_products_in_page_details(soup):
    logging.debug("get_all_products_in_page_details")

    all_products_details = []
    for h3 in soup.find_all('h3'):
        title = h3.a.get('title').strip()
        url = URL_TO_SCRAP + h3.a.get('href')
        print(f'the book "{title}" is at {url}')
        print("============================")
        all_products_details.append(get_a_product_details(title, url))
    print(f'all product details={all_products_details}')
    return(all_products_details)

def get_a_product_details(title, url, html_product_file=HTML_PRODUCT_FILE):
    logging.debug("get_a_product_details")

    soup = make_html_parser(url, html_product_file)
    a = soup.find('div', class_='item active')
    image_url = URL_TO_SCRAP + a.img.get('src').replace("../", "")
    table_data = [i.text for i in soup.find_all('td')]
    universal_product_code = table_data[0].strip()
    category = table_data[1].strip()
    price_including_tax = table_data[2].strip()
    price_excluding_tax = table_data[3].strip()
    number_available = table_data[5].strip()
    # product_description_head = soup.find_all('h2')[0].get_text()
    # product_description = soup.find_all('p')[3].get_text()
    review_rating = table_data[6].strip()

    star_rating = soup.find('p', class_='star-rating')['class'][1]

    # print(f'image_url={image_url}')
    # print(f'universal_product_code={universal_product_code}')
    # print(f'category={category}')
    # print(f'price_including_tax={price_including_tax}')
    # print(f'price_excluding_tax={price_excluding_tax}')
    # print(f'number_available={number_available}')
    # print(f'review_rating={review_rating}')
    # print(f'star_rating={star_rating}')
    # print("==============================")

    return([title, image_url, universal_product_code, category, price_including_tax, price_excluding_tax,
            number_available, review_rating, star_rating ])

def scrap_all_pages_collecting_books_details(category, all_books_category):
    pass

if __name__ == "__main__":
    start_logging()
    soup = make_html_parser(URL_TO_SCRAP, HTML_CONTENT_FILE)
    get_all_books(soup)
    all_books_category = get_all_books_category(soup)
    all_products_details = get_all_products_in_page_details(soup)
    get_page_number_out_of_total(soup)
    get_next_page(soup)
    sys.exit(0)


