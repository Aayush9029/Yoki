# might merge this with the undergraduate scraper later on, prompt between undergraduate and/or graduate programs
import requests
from bs4 import BeautifulSoup
import csv

class YorkGraduateProgramScraper:
    def __init__(self):
        self.directory_url = "https://futurestudents.yorku.ca/graduate/programs"
        self.programs = []
        self.output_file = "yorku_graduate_programs.csv"

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
            if href.startswith("/graduate/programs/") and href != "/graduate/programs":
                program_name = href.split("/graduate/programs/")[-1].strip()
                program_url = f"https://futurestudents.yorku.ca{href}"
                self.programs.append({"name": program_name, "url": program_url})

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
    scraper = YorkGraduateProgramScraper()
    scraper.extract_programs()
    print(f"Found {len(scraper.programs)} graduate programs")
    scraper.save_to_csv()