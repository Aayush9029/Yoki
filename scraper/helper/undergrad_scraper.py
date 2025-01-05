import requests
from bs4 import BeautifulSoup
import csv

class YorkProgramScraper:
    def __init__(self):
        self.directory_url = "https://futurestudents.yorku.ca/program-search"
        self.programs = []
        self.output_file = "yorku_programs.csv"

    def fetch_page(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    def extract_programs(self):
        html_content = self.fetch_page(self.directory_url)
        if not html_content:
            return

        soup = BeautifulSoup(html_content, "html.parser")
        program_links = soup.find_all("a", href=True)
        for link in program_links:
            href = link['href']
            if "/program/" in href: 
                program_name = href.split("/program/")[-1]
                self.programs.append({"name": program_name, "url": f"https://futurestudents.yorku.ca/program/{href}"})

    def save_to_csv(self):
        if not self.programs:
            print("No programs discovered.")
            return

        with open(self.output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "url"])
            writer.writeheader()
            writer.writerows(self.programs)

        print(f"Program data saved to {self.output_file}")


if __name__ == "__main__":
    scraper = YorkProgramScraper()
    scraper.extract_programs()
    print(f"Found {len(scraper.programs)} programs")
    scraper.save_to_csv()
    