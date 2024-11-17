import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
baseurl = "https://statutes.capitol.texas.gov/"
example_url = "https://statutes.capitol.texas.gov/Docs/CN/htm/CN.1/CN.1.1.htm"

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# def text_from_html(body):
#     soup = BeautifulSoup(body, 'html.parser')
#     texts = soup.findAll(string=True)
#     visible_texts = filter(tag_visible, texts)
#     return u" ".join(t.strip() for t in visible_texts)
            
# # Set the User-Agent header to mimic a web browser
# req = Request(
#     url=baseurl, #this is where the variable needs to go
#     headers={'User-Agent': 'Mozilla/5.0'}
# )
# webpage = urlopen(req).read() #making it a readable format for text_from_html
# article_str = text_from_html(webpage) #string from the entire webpage
# #print(article_str)

# def get_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     links = []

#     for link in soup.find_all('a', href=True):
#         links.append(link['href'])

#     return links

# links = get_links(baseurl)

# for link in links:
#     print(link)

#This is where you will click on the links
options = Options()
options.headless = True

# Path to your ChromeDriver
service = Service(executable_path='C:\\Users\\Owner\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get(baseurl)

time.sleep(4)
codeNames = []
titleNames = []
chapterNames = []
sectionNames = []
driver.find_element(By.XPATH, "//a[text()='Texas Statutes']").click()
time.sleep(2)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.parentNode.treeNode"))  
)

dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CODE')]")  #loads all the code names

# Iterate through the options
for option in dropdown_options:
    codeNames.append(option.text)
    option.click()
    time.sleep(2)
    title_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'TITLE')]")
    for title in title_dropdown_options:
        titleNames.append(title.text)
        time.sleep(2)
        chapter_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CHAPTER')]")
        for chapter in chapter_dropdown_options:
            chapterNames.append(chapter.text)
            WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "HTMLicon"))  
            )

            htmlicon_elements = driver.find_elements(By.CLASS_NAME, "HTMLicon")
            for htmlicon in htmlicon_elements:
                href = htmlicon.get_attribute("href")
                if href:
                    sectionNames.append(href)

            


print("Code Names: ", codeNames,
"Title Names: ", titleNames,
"Chapter Names: ", chapterNames)

driver.quit()
# for code in selectStatute:
#     codeText = code.text
#     codeNames.append(codeText)
#     code.click()
#     time.sleep(1)

#     selectTitle = driver.find_element(By.CSS_SELECTOR, "a.parentNode.treeNode")
#     for title in selectTitle:
#         modelText = title.text
#         modelNames.append(modelText)
    
# # Step 2: Find and click the link (modify this according to the link you want to click)
# try:
#     link = driver.find_element(By.TAG_NAME, 'a') # Example: Find link by text
#     link.click()

#     # Wait for the page to load after the click
#     time.sleep(3)  # Adjust based on how long the page takes to load

#     # Step 3: Get the page source after clicking
#     page_source = driver.page_source

#     # Step 4: Parse the page with BeautifulSoup
#     soup = BeautifulSoup(page_source, 'html.parser')

#     # Do something with the parsed HTML (e.g., extract data)
#     print(soup.prettify())  # Pretty-print the HTML

# finally:
#     # Close the WebDriver
#     