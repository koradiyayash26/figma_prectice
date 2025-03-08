import requests
from bs4 import BeautifulSoup
import time
import random
import fake_useragent  # You'll need to install this: pip install fake-useragent

def get_random_user_agent():
    try:
        ua = fake_useragent.UserAgent()
        return ua.random
    except:
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def scrape_amazon_iphones():
    # Try different Amazon domains and search queries
    urls = [
        "https://www.amazon.com/s?k=iphone+13",
        "https://www.amazon.com/s?k=iphone+14",
        "https://www.amazon.com/s?k=iphone+unlocked"
    ]
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'DNT': '1',
        'Referer': 'https://www.google.com/'
    }
    
    for url in urls:
        try:
            print(f"\nTrying URL: {url}")
            # Add a longer delay between requests
            time.sleep(random.uniform(3, 7))
            
            session = requests.Session()
            
            # First, get the main Amazon page to set cookies
            session.get("https://www.amazon.com", headers=headers, timeout=30)
            time.sleep(2)
            
            # Now make the search request
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if 'To discuss automated access to Amazon data please contact' in response.text:
                print("Amazon is blocking our request. Trying next URL...")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try different product container selectors
            products = soup.find_all('div', {'data-component-type': 's-search-result'})
            if not products:
                products = soup.find_all('div', {'class': 's-result-item'})
            if not products:
                products = soup.select('div.s-result-item[data-asin]')
            
            if not products:
                print("No products found on this URL. Trying next...")
                continue
            
            print("\nFound iPhone Results:")
            print("-" * 50)
            
            success = False
            # Process only first 5 products
            for product in products[:5]:
                try:
                    # Try different selectors for product name
                    name = None
                    name_elements = [
                        product.find('span', {'class': 'a-text-normal'}),
                        product.find('h2', {'class': 'a-size-mini'}),
                        product.select_one('h2 .a-text-normal')
                    ]
                    for elem in name_elements:
                        if elem:
                            name = elem.text.strip()
                            break
                    
                    # Try different selectors for price
                    price = None
                    price_elements = [
                        product.find('span', {'class': 'a-price'}),
                        product.find('span', {'class': 'a-offscreen'}),
                        product.select_one('.a-price .a-offscreen')
                    ]
                    for elem in price_elements:
                        if elem:
                            price = elem.text.strip()
                            break
                    
                    # Try different selectors for image
                    img_url = None
                    img_elements = [
                        product.find('img', {'class': 's-image'}),
                        product.select_one('.s-image'),
                        product.find('img', {'class': 'a-dynamic-image'})
                    ]
                    for elem in img_elements:
                        if elem and 'src' in elem.attrs:
                            img_url = elem['src']
                            break
                    
                    # Only print if we have all the information
                    if name and price and img_url:
                        success = True
                        print(f"Product: {name}")
                        print(f"Price: {price}")
                        print(f"Image URL: {img_url}")
                        print("-" * 50)
                
                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue
            
            # If we successfully got products, break the loop
            if success:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
        except Exception as e:
            print(f"Error scraping data: {e}")

if __name__ == '__main__':
    print("Starting scraper...")
    print("(This might take a few moments...)")
    scrape_amazon_iphones()
    print("\nIf no results appeared, try:")
    print("1. Using a VPN or proxy")
    print("2. Waiting a few minutes before trying again")
    print("3. Using Amazon's official API instead of scraping")