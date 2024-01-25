import requests
from bs4 import BeautifulSoup
url="https://www.istockphoto.com/search/2/image-film?family=creative&phrase=headshots"
response=requests.get(url)
print(f"Status code: {response.status_code}")
if response.status_code==200:
  
  soup=BeautifulSoup(response.content,'html.parser')
  images=soup.find_all("img")
  for image in images:
    print(image.get("src"))
else:
  print("Couldn't download the image")
