import time
print("Python script is running!")
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
service = Service(r"C:\\Users\\GowsikaSurendran\\Downloads\\AutomationTesting\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get("https://www.magickwoods.com/track/")
wait = WebDriverWait(driver, 10)

# List of orders
orders = [
    {"order_id": "0926727", "phone": "7174694371"},
    {"order_id": "0926727", "phone": "7174694371"},
    #{"order_id": "929890", "phone": "6306327433"},
    {"order_id": "932116", "phone": "8477442218"}
]

for order in orders:
    order_input = wait.until(EC.presence_of_element_located((By.ID, "order_id")))
    order_input.clear()
    order_input.send_keys(order["order_id"])
    
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "phone_no")))
    phone_input.clear()
    phone_input.send_keys(order["phone"])
    
    track_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get Status')]")))
    track_button.click()
    
    print(f"Checked Order ID: {order['order_id']} with Phone: {order['phone']}")
    
    time.sleep(20)  # wait for result to load
    driver.get("https://www.magickwoods.com/track/")  # refresh page for next order

input("All done! Press Enter to close browser...")

