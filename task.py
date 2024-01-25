import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://www.pexels.com/search/headshot/"

# Send an HTTP request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Extract information from the parsed HTML
for quote in soup.find_all("span", class_="text"):
    print(quote.get_text())
    print("---")
