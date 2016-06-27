import sys
import urllib2
from bs4 import BeautifulSoup
import pdb
import time


def url_append():
    try:
        keyword = sys.argv[2]
        page_num = sys.argv[1]
        if sys.argv[1].isdigit() and int(sys.argv[1]):
            return True, '~PG-{}?KW={}'.format(page_num, keyword)
        else:
            return False, 'Invalid page number.'
    except IndexError:
        if not len(sys.argv) == 2:
            return False, 'No argument provided.'
        keyword = sys.argv[1]
        return True, '?KW={}'.format(keyword)


def output_format(products):

    for product in products:
        print unicode("Product Title: {}\nProduct Price: {}\nVendor Name: {}\nShipping Charge: {}\n\n").format(
            product.get('product_title'), product.get('product_price'), product.get('vendor'), product.get('shipping_charge'))


def run():
    print 'Processing...'
    url = 'http://www.shopping.com/products'
    url_check, url_val = url_append()
    if not url_check:
        print url_val
        return
    url += url_val
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    if soup.find('span', {'class': 'nomatch'}):
        print 'No Match Found.'
        return
    index = 1
    if len(sys.argv) == 2:
        print 'Total results found: {}'.format(soup.find('span', {'class': 'numTotalResults'}).get_text().split('of ')[1])
        return
    results = soup.find_all('div', {'class': 'gridBox'})
    all_products = []
    for result in list(results):
        product = {}
        itemID = "nameQA" + str(index)
        item = soup.find('span', {'id': itemID})
        if not item:
            item = soup.find('a', {'id': itemID})
        product_title = item['title']
        product_price = soup.find(
            'span', {'class': 'productPrice'}).get_text().replace('\n', '')
        vendor = soup.find('a', {'class': 'newMerchantName'}).get_text()
        ql_id = 'quickLookItem-'+str(index)
        ql_item = soup.find('div', {'id': ql_id})
        free_shipping = ql_item.find('span', {'class': 'freeShip'})
        if not free_shipping:
            shipping_charge_div = ql_item.find(
                'div', {'class': 'taxShippingArea'})
            if not shipping_charge_div:
                shipping_charge = "Multiple Options Available"
            else:
                shipping_charge = shipping_charge_div.get_text().replace(
                    '\n', '')
        else:
            shipping_charge = free_shipping.get_text()
        product = {'product_title': product_title, 'product_price':
                   product_price, 'vendor': vendor, 'shipping_charge': shipping_charge}
        all_products.append(product)
        index += 1
    output_format(all_products)

run()
