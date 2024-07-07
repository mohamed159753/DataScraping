import requests
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_price_from_aziza(product_id):
    
    url = f'https://aziza.tn/fr/{product_id}.html'
    
    # Make a request to the URL
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the product price meta tag
        meta_tag = soup.find('meta', itemprop='price')
        
        if meta_tag:
            price = meta_tag['content']
            return float(price) * 1000  
        else:
            return None  
    else:
        return None  

# you can test with this id 10004518 which is has the price of 3100 you can check in this page https://aziza.tn/fr/10004518.html"
product_id = input("give the id of the product : ")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
price = get_price_from_aziza(product_id)
if price is not None:
    print(f'The price of product ID {product_id} on Aziza is: {price} millimes.')
else:
    print(f'Failed to retrieve price for product ID {product_id} from Aziza.')

