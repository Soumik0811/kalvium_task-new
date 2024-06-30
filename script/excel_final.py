import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

link_list = [
    "https://results.eci.gov.in/AcResultGen2ndJune2024/candidateswise-S2123.htm"
]


# Initialize ExcelWriter outside the loop
with pd.ExcelWriter('election_results2.xlsx', engine='xlsxwriter') as writer:
    workbook = writer.book

    for link in link_list:
        # Set up the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        try:
            # Open the URL
            driver.get(link)
            time.sleep(10)
            # Extract title
            title_h2 = driver.find_element(By.TAG_NAME, 'h2').text

            # Page 2: Candidates
            candidates = []
            cand_boxes = driver.find_elements(By.CLASS_NAME, 'col-md-4.col-12')

            for box in cand_boxes:
                image = box.find_element(By.TAG_NAME, 'img').get_attribute('src')
                name = box.find_element(By.TAG_NAME, 'h5').text
                party = box.find_element(By.TAG_NAME, 'h6').text
                status_divs = box.find_element(By.CLASS_NAME, 'status').find_elements(By.TAG_NAME, 'div')
                votes = status_divs[1].text.split(' ')[0]
                try:
                    margin = status_divs[1].text.split(' ')[1] + ' ' + status_divs[1].text.split(' ')[2]
                except IndexError:
                    margin = "Uncontested"


                candidates.append({
                    'Name': name,
                    'Party': party,
                    'Image Link': image,
                    'Votes': votes,
                    'Margin': margin
                })

            # Page 3: Table
            switch_list = driver.find_element(By.CLASS_NAME, 'switch-list')
            links = switch_list.find_elements(By.TAG_NAME, 'a')
            links[2].click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-striped')))

            header = [th.text for th in driver.find_elements(By.CSS_SELECTOR, 'table.table-striped thead th')]

            body = []
            rows = driver.find_elements(By.CSS_SELECTOR, 'table.table-striped tbody tr')
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                body.append([col.text for col in cols])

            footer = [td.text for td in driver.find_elements(By.CSS_SELECTOR, 'table.table-striped tfoot th, table.table-striped tfoot td')]
            table_data = {
                "header": header,
                "body": body,
                "footer": footer
            }

            # Page 1: Tables
            switch_list = driver.find_element(By.CLASS_NAME, 'switch-list')
            links = switch_list.find_elements(By.TAG_NAME, 'a')
            links[0].click()
            tables_data = []
            time.sleep(5)

            for i in range(1, 9):
                try:
                    button = driver.find_element(By.XPATH, f"//button[contains(@onclick, 'tab{i}')]")
                    button.click()
            
                    tab_id = f'tab{i}'
                    tab = driver.find_element(By.ID, tab_id)
                    header = [th.text for th in tab.find_elements(By.CSS_SELECTOR, 'table thead th')]
                    first_header = header[0]
                    header = header[1:]
            
                    body = []
                    rows = tab.find_elements(By.CSS_SELECTOR, 'table tbody tr')
                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        body.append([col.text for col in cols])
            
                    footer = [td.text for td in tab.find_elements(By.CSS_SELECTOR, 'table tfoot th, table tfoot td')]
                    table_data_1 = {
                        "header": header,
                        "body": body,
                        "footer": footer
                    }
                    tables_data.append(table_data_1)
                
                except NoSuchElementException:
                    print(f"Button or tab {i} not found. Exiting loop.")
                    break

            # Write data to Excel sheets
            sheet_name = link.split('/')[-1].replace('.htm', '')
            worksheet = workbook.add_worksheet(sheet_name[:31])  # Limit sheet name length to 31 characters
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter'
            })

            worksheet.write('A1', title_h2, title_format)
            worksheet.set_column('A:A', 50)

            start_row = 3

            for index, table in enumerate(tables_data, start=1):
                worksheet.write(start_row, 0, f"Round {index} - Page 1", title_format)
                start_row += 1

                header_row = start_row
                worksheet.write_row(start_row, 0, table['header'], title_format)

                start_row += 1
                for row_data in table['body']:
                    worksheet.write_row(start_row, 0, row_data)
                    start_row += 1

                footer_row = start_row + 1
                worksheet.write_row(start_row, 0, table['footer'])

                start_row += 2

            worksheet.write(start_row, 0, "Table - Page 3", title_format)
            start_row += 1

            worksheet.write_row(start_row, 0, table_data['header'], title_format)

            start_row += 1
            for row_data in table_data['body']:
                worksheet.write_row(start_row, 0, row_data)
                start_row += 1

            start_row += 2

            worksheet.write(start_row, 0, "Candidates - Page 2", title_format)
            start_row += 1

            candidates_columns = list(candidates[0].keys())
            worksheet.write_row(start_row, 0, candidates_columns)
            start_row += 1

            for candidate in candidates:
                worksheet.write_row(start_row, 0, list(candidate.values()))
                start_row += 1

            print(f"Data from {link} uploaded successfully!")

        finally:
            driver.quit()

print("All data scraped and saved to 'election_results.xlsx' successfully!")
