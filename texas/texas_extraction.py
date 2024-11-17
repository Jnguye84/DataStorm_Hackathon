from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

baseurl = "https://statutes.capitol.texas.gov/"

options = Options()
options.headless = True

# Path to chromedriver
service = Service(executable_path='C:\\Users\\Owner\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)
driver.get(baseurl)

time.sleep(4)

codeNames = []

# Find the 'Texas Statutes' link and click it
driver.find_element(By.XPATH, "//a[text()='Texas Statutes']").click()
time.sleep(2)

# Wait for the page to load and ensure elements are present
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.parentNode.treeNode"))
)

# Now attempt to find the 'CODE' elements
dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CODE')]")

if not dropdown_options:
    print("No 'CODE' elements found.")
else:
    for i in range(len(dropdown_options)):
        dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CODE')]")
        
        if i >= len(dropdown_options):
            print(f"Index {i} is out of range. Skipping to next.")
            continue
        
        option = dropdown_options[i]
        print(f"Accessing CODE: {option.text}")

        try:
            # Wait until the element is visible and click it
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"//a[text()='{option.text}']"))
            )

            # You can also use JavaScript click if the normal click doesn't work:
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)

            # Try finding and processing the TITLE elements
            title_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'TITLE')]")
            if title_dropdown_options:
                for title in range(len(title_dropdown_options)):
                    title_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'TITLE')]")
                    if title < len(title_dropdown_options):
                        title_element = title_dropdown_options[title]
                        print(f"Accessing TITLE: {title_element.text}")
                        time.sleep(2)

                        # Try finding and processing the CHAPTER elements
                        chapter_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CHAPTER')]")
                        if chapter_dropdown_options:
                            for c in range(len(chapter_dropdown_options)):
                                chapter_dropdown_options = driver.find_elements(By.XPATH, "//a[contains(text(), 'CHAPTER')]")
                                if c < len(chapter_dropdown_options):
                                    chapter = chapter_dropdown_options[c]
                                    print(f"Accessing CHAPTER: {chapter.text}")

                                    # Process the sections for this chapter
                                    htmlicon_elements = driver.find_elements(By.CLASS_NAME, "HTMLicon")
                                    if htmlicon_elements:
                                        htmlicon = htmlicon_elements[0]  # Access the first element
                                        href = htmlicon.get_attribute("href")
                                        if href:
                                            print(f"Section URL: {href}")
                                            # Here you can continue processing as needed

        except Exception as e:
            print(f"Error accessing {option.text}: {e}")
            continue  # Skip this CODE and proceed to the next one

        # Optionally, you could also handle other errors like elements being unclickable, etc.

        print("Continuing to next CODE...")
