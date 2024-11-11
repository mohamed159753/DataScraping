from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import openpyxl
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
driver.get('https://www.linkedin.com/login')
username = 'your_linkedIn_username'
password = 'Your_LinkedIn_password'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
email_element = driver.find_element(By.ID, 'username')
email_element.send_keys(username)
password_element = driver.find_element(By.ID, 'password')
password_element.send_keys(password)
password_element.send_keys(Keys.RETURN)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'global-nav-typeahead')))
search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Cliquez pour lancer une recherche"]')))
search_button.click()
search_query = 'software developer'
search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Recherche"]')))
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)
time.sleep(10)
try:
filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '(//button[contains(@class, "search-reusables__filter-pill-button")])[3]')))
filter_button.click()
except Exception as e:
print(f"Error clicking filter button: {e}")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'reusable-search__result-container')))
results = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = 'Name'
sheet['B1'] = 'Occupation'
sheet['C1'] = 'Location'
sheet['D1'] = 'Profile Link'
for index, result in enumerate(results, start=2):
try:
name = result.find_element(By.TAG_NAME, 'span').text
occupation = result.find_element(By.CLASS_NAME, 'entity-result__primary-subtitle').text
location = result.find_element(By.CLASS_NAME, 'entity-result__secondary-subtitle').text
profile_link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        sheet[f'A{index}'] = name
        sheet[f'B{index}'] = occupation
        sheet[f'C{index}'] = location
        sheet[f'D{index}'] = profile_link
        
    except Exception as e:
        print(f"An error occurred: {e}")

excel_filename = 'linkedin_results.xlsx'
workbook.save(excel_filename)
print(f'Excel file "{excel_filename}" has been saved.')

driver.quit()

