import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_images(url, output_folder):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags in the HTML
        img_tags = soup.find_all('img')

        # Download each image
        for img_tag in img_tags:
            # Get the source (src) attribute of the image tag
            img_url = img_tag.get('src')

            # Create an absolute URL by joining the base URL and the image URL
            img_url = urljoin(url, img_url)

            # Send a request to the image URL
            img_response = requests.get(img_url)

            # Check if the request was successful (status code 200)
            if img_response.status_code == 200:
                # Get the image content and save it to a file
                img_data = img_response.content
                img_name = img_url.split("/")[-1]
                img_path = f"{output_folder}/{img_name}"

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Image '{img_name}' downloaded successfully.")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Example usage
url_to_scrape = 'https://example.com'
output_directory = 'downloaded_images'

scrape_images(url_to_scrape, output_directory)
