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

order_id_value = "0926727"        # <-- Change this value manually
phone_value = "7174694371"       # <-- Change this value manually

# Enter Order ID
order_input = wait.until(
    EC.presence_of_element_located((By.ID, "order_id"))
)
order_input.clear()
order_input.send_keys(order_id_value)

# Enter Phone Number
phone_input = wait.until(
    EC.presence_of_element_located((By.ID, "phone_no"))
)
phone_input.clear()
phone_input.send_keys(phone_value)

# Click "Get Status" Button
track_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get Status')]"))
)
track_button.click()

print(f"Tracking Order ID: {order_id_value} with Phone: {phone_value}")
input("Press Enter to close browser...")

