import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def download_image_local(image_url, folder_path, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join(folder_path, file_name), 'wb') as file:
            file.write(response.content)

def scrape_images_from_url(url, folder_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Folder path for downloading images
    folder_path = './' + folder_name
    os.makedirs(folder_path, exist_ok=True)

    driver.get(url)
    image_elements = driver.find_elements(By.TAG_NAME, 'img')

    for i, image_element in enumerate(image_elements):
        image_url = image_element.get_attribute('src')
        if image_url:
            file_name = f"image_{i}.jpg"
            download_image_local(image_url, folder_path, file_name)
            print(f"Downloaded {file_name} from {folder_name}")
    driver.quit()

# Base URL and page range
base_url = "https://www.istockphoto.com/search/2/image-film"
start_page = 2
end_page = 200

# Generate URL for each page and scrape using a while loop
current_page = start_page
while current_page <= end_page:
    url = f"{base_url}?page={current_page}&phrase=headshot"
    folder_name = f"page_{current_page}_images"
    scrape_images_from_url(url, folder_name)
    current_page += 1
