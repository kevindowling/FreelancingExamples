from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import csv


# Set up the driver
chromedriver_path = chromedriver_autoinstaller.install()
options = Options()
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(options=options, service=service)
driver = webdriver.Chrome(service=service)

# Replace with the URL of the page you want to scrape
url = 'https://csfloat.com/db'

# Navigate to the page
driver.get(url)

# Find the table by its id (or use other find_element_by_* methods to locate the table)
table = driver.find_element(By.TAG_NAME, 'table')

# Get all rows in the table
rows = table.find_elements(By.TAG_NAME, 'tr')
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in rows:
        # For header ('th') and data ('td')
        header = [ele.text.strip() for ele in row.find_elements(By.TAG_NAME, 'th')]
        if header:
            writer.writerow(header)
        
        cols = [ele.text.strip() for ele in row.find_elements(By.TAG_NAME, 'td')]
        if cols:
            writer.writerow(cols)

# Close the browser window
driver.quit()
