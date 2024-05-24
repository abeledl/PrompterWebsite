import requests
from bs4 import BeautifulSoup

base_url = "https://docs.blender.org/api/current/"
index_url = base_url + "index.html"

response = requests.get(index_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links to the API documentation pages
api_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith('.html') and 'bpy' in href:
        api_links.append(base_url + href)

# Function to fetch and parse the content of each page
def fetch_content(url):
    response = requests.get(url)
    page_soup = BeautifulSoup(response.text, 'html.parser')
    return page_soup.get_text()

# Fetch and consolidate the content of all API pages
api_content = ""
for link in api_links:
    api_content += fetch_content(link)
    api_content += "\n\n"

# Save the content to a text file
with open("blender_api.txt", "w", encoding='utf-8') as file:
    file.write(api_content)

print("Blender API documentation has been saved to blender_api.txt")