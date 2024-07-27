import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import aiohttp
from fake_useragent import UserAgent 

class AdvancedWebScraper:
    def __init__(self):
        self.results = {
            "Headings": [],
            "Text": [],
            "Images": [],ds
            "Links": []
        }
        # Initialize logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize User-Agent rotator
        self.ua = UserAgent()

    async def fetch_url(self, session, url):
        # Asynchronous URL fetching with retry logic and User-Agent rotation
        max_retries = 3
        for retry in range(max_retries):
            try:
                headers = {'User-Agent': self.ua.random}
                async with session.get(url, headers=headers, allow_redirects=True, timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        self.logger.warning(f"Failed to fetch {url}. HTTP Status Code: {response.status}. Retrying in {2 ** retry} seconds...")
                        await asyncio.sleep(2 ** retry)
            except Exception as e:
                self.logger.error(f"Error during request to {url}: {e}")
                if retry == max_retries - 1:
                    return None
        return None

    async def extract_data(self, url):
        async with aiohttp.ClientSession() as session:
            html_content = await self.fetch_url(session, url)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract headings (h1 to h6)
                self.results["Headings"] = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

                # Extract all text content from the page
                self.results["Text"] = [paragraph.text.strip() for paragraph in soup.find_all("p")]

                # Extract all image URLs from the page
                self.results["Images"] = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]

                # Extract all links from the page, handling relative URLs
                self.results["Links"] = [urljoin(url, link.get("href")) for link in soup.find_all("a") if link.get("href")]

                self.logger.info(f"Successfully scraped data from {url}")
            else:
                self.logger.error(f"Failed to fetch content from {url}")

    def save_to_csv(self, filename):
        """ Save the results to a CSV file. """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write headers and data for each category
            for category, data in self.results.items():
                csvwriter.writerow([category])
                for item in data:
                    csvwriter.writerow([item])
                csvwriter.writerow([])  # Blank row between categories

        self.logger.info(f"Data saved to {filename}")

    def display_results(self):
        print("Scraped Data:")
        for category, data in self.results.items():
            print(f"\n{category}:")
            if data:
                for item in data[:5]:  # Display only first 5 items for brevity
                    print(item)
                if len(data) > 5:
                    print(f"... and {len(data) - 5} more items")
            else:
                print(f"No {category.lower()} found based on the specified criteria.")

    async def scrape_multiple_urls(self, urls):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                tasks.append(self.extract_data(url))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    scraper = AdvancedWebScraper()

    # User input validation
    urls = []
    while True:
        url = input("Please enter a URL (or press Enter to finish): ")
        if url:
            urls.append(url)
        else:
            if urls:
                break
            else:
                print("Please enter at least one URL.")

    print(f"Extracting data from {len(urls)} URL(s)...")
    
    # Run the asynchronous scraping
    asyncio.run(scraper.scrape_multiple_urls(urls))

    scraper.display_results()

    # Save results to CSV
    filename = 'scraped_data.csv'
    scraper.save_to_csv(filename)