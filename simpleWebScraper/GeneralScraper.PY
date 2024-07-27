import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

class AdvancedWebScraper:
    def __init__(self):
        self.results = {
            "Text": [],
            "Images": [],
            "Links": []
        }

    def extract_data(self, url):
        try:
           
            max_retries = 3
            for retry in range(max_retries):
                response = requests.get(url, allow_redirects=True, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    print(f"Failed to fetch the page. HTTP Status Code: {response.status_code}. Retrying in {2 ** retry} seconds...")
                    time.sleep(2 ** retry)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Extract all text content from the page
                self.results["heading"] = [paragraph.text.strip() for paragraph in soup.find_all("h")]
                self.results["Text"] = [paragraph.text.strip() for paragraph in soup.find_all("p")]

                # Extract all image URLs from the page
                self.results["Images"] = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]

                # Extract all links from the page, handling relative URLs
                self.results["Links"] = [urljoin(url, link.get("href")) for link in soup.find_all("a") if link.get("href")]

            else:
                print(f"Failed to fetch the page. HTTP Status Code: {response.status_code}")
                return

        except requests.RequestException as e:
            print(f"Error during request: {e}")
            return

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

        print(f"Data saved to {filename}")

    def display_results(self):
        print("Scraped Data:")
        for category, data in self.results.items():
            print(f"\n{category}:")
            if data:
                for item in data:
                    print(item)
                    print()
            else:
                print(f"No {category.lower()} found based on the specified criteria.")

if __name__ == "__main__":
    scraper = AdvancedWebScraper()

    # User input validation
    while True:
        url = input("Please enter the URL: ")
        if url:
            break
        else:
            print("Invalid URL. Please try again.")

    print(f"Extracting data from {url}...")
    scraper.extract_data(url)

    scraper.display_results()

    # Save results to CSV
    filename = 'scraped_data.csv'
    scraper.save_to_csv(filename)
