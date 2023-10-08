
# Web Table Scraper

This repository contains a Python script that allows users to scrape tables from a specified URL using Selenium and then save the scraped data to a CSV file.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/web-table-scraper.git
   cd web-table-scraper
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Script**:
   ```bash
   python scraper.py
   ```

2. **Input the URL**:
   The script will prompt you to enter the URL of the page containing the tables you wish to scrape.

3. **Check the Output**:
   The scraped data will be saved in `output.csv` in the current directory.

## Compilation to Executable

If you'd like to compile the script into a standalone executable:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Compile**:
   ```bash
   pyinstaller --onefile scraper.py
   ```

The resulting executable will be found in the `dist` directory.

## Dependencies

- Selenium
- ChromeDriver Autoinstaller

## Contribution

Feel free to fork the repository and submit pull requests. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
