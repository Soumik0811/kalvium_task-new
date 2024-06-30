import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# List of URLs to scrape
list_link = [
    "https://results.eci.gov.in/AcResultGen2ndJune2024/partywisewinresult-1658S21.htm",
"https://results.eci.gov.in/AcResultGen2ndJune2024/partywisewinresult-1619S21.htm"
]

# Initialize an empty list to store data
data = []

# Set up the WebDriver
for url in list_link:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    # Find the table body element
    table = driver.find_element(By.TAG_NAME, 'tbody')

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    # Iterate through the rows and extract data
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        data.append(row_data)
    
    # Close the WebDriver
    driver.quit()

# Convert data to DataFrame
df = pd.DataFrame(data, columns=['ID', 'Constituency', 'Candidate', 'Votes', 'Margin', 'Stations'])

# Write DataFrame to Excel
excel_file = 'election_results.xlsx'
df.to_excel(excel_file, index=False)

print(f"Data successfully written to {excel_file}")
