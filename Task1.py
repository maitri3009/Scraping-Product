'''
Python Assignment
Part 1
In this assignment you are required to scrape all products from this URL:
https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2
C283&ref=sr_pg_1
Need to scrape atleast 20 pages of product listing pages
Items to scrape
• Product URL
• Product Name
• Product Price
• Rating
• Number of reviews
'''

import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"

def scrape_product_details(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_details = []
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        product_name_elem = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        product_name = product_name_elem.text if product_name_elem else "N/A"
        
        product_price_elem = product.find('span', {'class': 'a-price-whole'})
        product_price = product_price_elem.text if product_price_elem else "N/A"
        
        product_rating_elem = product.find('span', {'class': 'a-icon-alt'})
        product_rating = product_rating_elem.text if product_rating_elem else "N/A"
        
        num_reviews_elem = product.find('span', {'class': 'a-size-base'})
        num_reviews = num_reviews_elem.text if num_reviews_elem else "N/A"
        
        product_url_elem = product.find('a', {'class': 'a-link-normal s-no-outline'})
        product_url = "https://www.amazon.in" + product_url_elem['href'] if product_url_elem else "N/A"
            
        product_details.append([product_name, product_price, product_rating, num_reviews, product_url])
    
    return product_details

all_product_details = []

for page_number in range(1, 21):
    page_url = base_url.format(page_number)
    product_details = scrape_product_details(page_url)
    all_product_details.extend(product_details)

with open('product_listings.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Product Price", "Rating", "Number of Reviews", "Product URL"])
    writer.writerows(all_product_details)
