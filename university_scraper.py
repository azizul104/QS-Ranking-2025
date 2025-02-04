from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sel_ex
import time
import pandas as pd

# Initialize WebDriver
browser = webdriver.Chrome()
browser.maximize_window()

# Base URL of the website to scrape
ranking_url = "https://www.topuniversities.com/world-university-rankings?page="
total_pages = 20  # Number of pages to extract data from
metric_ids = ['research-discovery', 'learning-experience', 'employability', 'global-engagement', 'sustainability']

# List to store extracted university data
university_data = []

for page_num in range(total_pages):
    print(f"\n>>> Processing Page {page_num + 1} <<<\n")
    
    # Open the target page
    browser.get(ranking_url + str(page_num))
    time.sleep(5)
    
    # Handle Terms & Conditions popup
    try:
        time.sleep(10)  # Allow popup to load
        terms_popup = browser.find_element(By.XPATH, '//*[@id="popup-buttons"]/button[1]')
        terms_popup.click()
        print("Closed Terms and Conditions popup.")
    except Exception:
        print("No Terms and Conditions popup detected.")
    
    # Handle Academic Role Survey popup
    try:
        time.sleep(5)
        survey_popup = browser.find_element(By.XPATH, "//div[contains(@class,'modal-content')]")
        academic_option = survey_popup.find_element(By.XPATH, "//input[@type='radio'][@name='role'][@value='Academic']")
        academic_option.click()
        close_survey = survey_popup.find_element(By.XPATH, "//button[@data-dismiss='modal']")
        close_survey.click()
        print("Closed Academic Role Survey popup.")
        time.sleep(2)
    except Exception:
        print("No Academic Role Survey popup detected.")
    
    # Close success survey modal if it appears
    try:
        survey_success_popup = browser.find_element(By.XPATH, "//div[contains(@class,'modal-content')]")
        close_button = survey_success_popup.find_element(By.XPATH, '//*[@id="success_survey"]/div/div/div[1]/img')
        close_button.click()
        print("Closed Success Survey popup.")
        time.sleep(2)
    except Exception:
        print("No Success Survey popup detected.")
    
    # Click "Load More" button repeatedly if available
    load_attempts = 0
    while True:
        try:
            load_more = browser.find_element(By.XPATH, "//button[contains(@class,'loadmorebutton')]")
            load_more.click()
            load_attempts += 1
            print(f"Page {page_num + 1}: Loaded additional universities - Attempt {load_attempts}")
            time.sleep(3)
        except Exception:
            print("No more 'Load More' button detected.")
            break
    
    # Find university listings
    ranking_section = browser.find_element(By.ID, 'ranking-data-load')
    university_rows = ranking_section.find_elements(By.XPATH, "//div[contains(@class,'ind ') and contains(@class , 'main')]")
    print(f"Total universities identified on Page {page_num + 1}: {len(university_rows)}")
    
    # Scroll to the top before processing
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    # Extract data from each university listing
    for index, row in enumerate(university_rows):
        print(f"Processing row {index + 1} of {len(university_rows)} on Page {page_num + 1}")
        
        record = {
            'University Name': '',
            'Location': ''
        }
        
        row_content = row.text.split('\n')
        node_id = row.get_attribute('nid')
        
        try:
            record[row_content[0].split()[0]] = row_content[0].split()[1]
            record[row_content[1].split(':')[0]] = row_content[1].split(':')[1].strip()
            record['University Name'] = row_content[2]
            
            location_info = row_content[3].split(', ')
            record['Location'] = location_info[1] if len(location_info) > 1 else location_info[0]
            
            record[row_content[-4]] = row_content[-3]
            record[row_content[-2]] = row_content[-1]
        except IndexError as err:
            print(f"Skipping row {index + 1} on Page {page_num + 1} due to IndexError: {err}")
            continue
        
        time.sleep(1)
        
        # Extract additional details from tabs
        for metric in metric_ids[1:]:
            time.sleep(1)
            
            # Close any unexpected popup before switching tabs
            try:
                modal_popup = browser.find_element(By.XPATH, "//div[contains(@class,'modal show')]")
                close_modal = modal_popup.find_element(By.XPATH, "//button[@data-dismiss='modal']")
                close_modal.click()
                time.sleep(2)
                print("Closed modal before switching tabs.")
            except Exception:
                pass  # No popup detected
            
            try:
                metric_tab = row.find_element(By.XPATH, f"//a[@id='{metric}-{node_id}'][@data-toggle='tab']")
                browser.execute_script("arguments[0].scrollIntoView();", metric_tab)
                browser.execute_script("arguments[0].click();", metric_tab)
                time.sleep(1)
            except sel_ex.ElementClickInterceptedException:
                print(f"Click intercepted on {metric}-{node_id}, skipping...")
                continue
            
            # Extract data from opened tab
            try:
                tab_content = browser.find_element(By.ID, f"{metric}-{node_id}-tab")
                tab_text = tab_content.text.split('\n')
                
                if tab_text[0] == 'Sustainability Score':
                    record[tab_text[0]] = tab_text[1]
                else:
                    for idx in range(0, len(tab_text), 2):
                        record[tab_text[idx]] = tab_text[idx + 1]
            except Exception as err:
                print(f"Error retrieving {metric} tab: {err}")
        
        university_data.append(record)

# Store extracted data in CSV
results_df = pd.DataFrame(university_data)
results_df.to_csv('world_university_rankings_2025.csv', index=False)
print("\nData extraction complete! Saved to 'world_university_rankings_2025.csv'.")

# Close WebDriver
time.sleep(5)
browser.quit()
