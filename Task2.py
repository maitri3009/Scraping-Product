'''
Part 2
With the Product URL received in the above case, hit each URL, and add below items:
• Description
• ASIN
• Product Description
• Manufacturer
Need to hit around 200 product URL’s and fetch various information.
'''

import requests
from bs4 import BeautifulSoup
import csv

def scrape_additional_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    description_elem = soup.find('div', {'id': 'productDescription'})
    description = description_elem.find('p').get_text(strip=True) if description_elem else "N/A"
        
    asin_elem = soup.find('th', string='ASIN')
    asin = asin_elem.find_next('td').get_text(strip=True) if asin_elem else "N/A"
        
    product_description_elem = soup.find('div', {'id': 'feature-bullets'})
    product_description = product_description_elem.find('ul').get_text(strip=True) if product_description_elem else "N/A"
        
    manufacturer_elem = soup.find('th', string='Manufacturer')
    manufacturer = manufacturer_elem.find_next('td').get_text(strip=True) if manufacturer_elem else "N/A"
    
    return [description, asin, product_description, manufacturer]

product_urls = []

with open('product_listings.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_urls.append(row['Product URL'])

product_details = []

for url in product_urls[:200]:
    details = scrape_additional_details(url)
    product_details.append(details)

with open('product_details.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Description", "ASIN", "Product Description", "Manufacturer"])
    writer.writerows(product_details)
