import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.stubhub.com/explore?lat=MjUuNDQ3ODg5OA%3D%3D&lon=LTgwLjQ3OTIyMzY5OTk5OTk5&to=253402300799999&tlcId=2'
driver.get(url)

# Wait for the elements to load
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.ifrHJW>li')))

# Extract match details
match_list = driver.find_elements(By.CSS_SELECTOR, 'ul.ifrHJW>li')
data_store = []

for match in match_list:
    try:
        title = match.find_element(By.CSS_SELECTOR, 'p.gYhGAZ').text  # Title
        location = match.find_elements(By.CSS_SELECTOR, 'p.jHVbjB')[1].text  # Location
        date_time = match.find_elements(By.CSS_SELECTOR, 'p.jHVbjB')[0].text  # Date/Time
        image_url = match.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')  # Image URL

        # Create a new template for each match
        match_data = {
            'title': title,
            'location': location,
            'datetime': date_time,
            'image_url': image_url
        }
        data_store.append(match_data)

    except Exception as e:
        print(f"Error processing match: {e}")

# Close WebDriver
driver.quit()

# Save data to a JSON file
output_file = "matches.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data_store, file, ensure_ascii=False, indent=4)

print(f"Data has been saved to {output_file}")
