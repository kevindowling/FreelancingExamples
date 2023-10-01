# Web Scraper with Selenium

This program is a simple Python script that uses Selenium to scrape tables from web pages and writes the output to a CSV file. This particular implementation is set up to scrape a table from 'https://csfloat.com/db' but can be modified to scrape from any URL.

## Prerequisites

- Python
- Selenium
- ChromeDriver Autoinstaller
- Google Chrome Browser

## Installation

To run the script, you need to have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/).

Once Python is installed, you can install the required libraries using pip:

```sh
pip install selenium chromedriver-autoinstaller
```

## Usage

1. Replace the `url` variable with the URL of the page you want to scrape.
```python
url = 'https://your_url.com'
```

2. Run the script.
```sh
python scraper.py
```

3. The scraped data will be written to `output.csv` in the same directory as the script.

## Code Overview

- The script uses Selenium to instantiate a Chrome browser and navigate to the specified URL.
- The table is located by its tag name, and the rows within the table are then located and iterated over.
- The header (`th`) and data (`td`) of each row are extracted and written to the CSV file.
- After processing all rows, the browser window is closed.
