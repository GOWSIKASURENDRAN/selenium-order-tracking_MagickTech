# Import time module to use time.sleep() for waiting between actions
import time
# Print message in terminal so we know script started
print("Python script is running!")
# Selenium imports
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options and driver
chrome_options = Options()
service = Service(r"C:\\Users\\GowsikaSurendran\\Downloads\\AutomationTesting\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

# Open the tracking page
# Go to the order tracking website
driver.get("https://www.magickwoods.com/track/")
# Wait up to 10 seconds for elements to load
wait = WebDriverWait(driver, 10)

# List of orders to check
orders = [
    {"order_id": "0926727", "phone": "7174694371"},# First order
    {"order_id": "0926727", "phone": "7174694371"},# Second order
    {"order_id": "0929890", "phone": "6306327433"},# third order
    {"order_id": "0932116", "phone": "8477442218"}# fourth order
]
# Loop through each order in the list
for order in orders:
    # Wait for the Order ID input box to appear, then select it
    order_input = wait.until(EC.presence_of_element_located((By.ID, "order_id")))
    order_input.clear()# Clear any existing text in the input box
    order_input.send_keys(order["order_id"])# Type the Order ID into the box
    
    # Wait for the Phone Number input box to appear, then select it
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "phone_no")))
    phone_input.clear()# Clear any existing text in the input box
    phone_input.send_keys(order["phone"])# Type the phone number into the box
    
    # Wait for the "Get Status" button to be clickable, then click it
    track_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get Status')]")))
    track_button.click()# Click the button to submit the form
    
    # Print message in terminal so you know which order was checked
    print(f"Checked Order ID: {order['order_id']} with Phone: {order['phone']}")
    
    # Wait 20 seconds so the result loads and you can see it in browser
    time.sleep(20)

    # Refresh the page for the next order in the list
    driver.get("https://www.magickwoods.com/track/")  # refresh page for next order

# Finish script and wait for user to close browser
input("All done! Press Enter to close browser...")
driver.quit()