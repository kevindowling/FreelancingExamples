from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import csv
import os

# Set up the driver
chromedriver_path = chromedriver_autoinstaller.install()
options = Options()
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(options=options, service=service)
driver = webdriver.Chrome(service=service)

# Take user input for the URL
url = input("Please enter the URL of the page you want to scrape: ")

# Navigate to the page
driver.get(url)

# Find all tables on the page
tables = driver.find_elements(By.TAG_NAME, 'table')
print(f"Found {len(tables)} table(s)")

try:
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                header = [ele.text.strip() for ele in row.find_elements(By.TAG_NAME, 'th')]
                if header:
                    writer.writerow(header)
                cols = [ele.text.strip() for ele in row.find_elements(By.TAG_NAME, 'td')]
                if cols:
                    writer.writerow(cols)
except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser window
driver.quit()
