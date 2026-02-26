# Import modules
import time
from datetime import datetime
import requests  # For URL checks
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Python script is running!")

# Setup Chrome options and driver
chrome_options = Options()
service = Service(r"C:\Users\GowsikaSurendran\Downloads\AutomationTesting\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

# Open the tracking page
driver.get("https://www.magickwoods.com/track/")
wait = WebDriverWait(driver, 10)

# List of orders to check
orders = [
    {"order_id": "0926727", "phone": "7174694371"},
    {"order_id": "0926727", "phone": "7174694371"},
    {"order_id": "0929890", "phone": "6306327433"},
    {"order_id": "0932116", "phone": "8477442218"}
]

# Store results
results = []

# Accept Cookies Automatically (if popup appears)
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-cky-tag='accept-button']")
        )
    )
    cookie_button.click()
    print("Cookies accepted.")
except:
    print("No cookie popup found.")

# Loop through orders
for order in orders:
    # Fill Order ID
    order_input = wait.until(EC.presence_of_element_located((By.ID, "order_id")))
    order_input.clear()
    order_input.send_keys(order["order_id"])

    # Fill Phone
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "phone_no")))
    phone_input.clear()
    phone_input.send_keys(order["phone"])

    # Click Get Status
    track_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get Status')]"))
    )
    track_button.click()
    print(f"Checked Order ID: {order['order_id']} with Phone: {order['phone']}")

    # Wait for results to load
    time.sleep(20)  # Adjust if needed

    # Capture full page text
    try:
        result_text = driver.find_element(By.TAG_NAME, "body").text
    except:
        result_text = "Status Not Found"

    # URL check
    try:
        response = requests.head(driver.current_url, timeout=5)
        url_status = "PASS" if response.status_code == 200 else f"FAIL ({response.status_code})"
    except:
        url_status = "FAIL (Not Reachable)"

    # Phone field check
    try:
        driver.find_element(By.ID, "phone_no")
        phone_field_status = "PASS"
    except:
        phone_field_status = "FAIL"

    # Status text check
    order_status = "PASS" if result_text and "not found" not in result_text.lower() else "FAIL"

    # Final result
    final_result = "PASS" if url_status=="PASS" and phone_field_status=="PASS" and order_status=="PASS" else "FAIL"

    # Save result
    results.append({
        "order_id": order["order_id"],
        "phone": order["phone"],
        "status": result_text[:200],
        "url_check": url_status,
        "phone_field_check": phone_field_status,
        "order_status_check": order_status,
        "final_result": final_result,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Refresh page for next order
    driver.get("https://www.magickwoods.com/track/")

# Create HTML report
html_content = f"""
<html>
<head>
<title>QA Automation Report</title>
<style>
body {{font-family: Arial; background-color:#f4f6f9;}}
h1 {{text-align:center;}}
table {{
  border-collapse: collapse;
  width: 95%;
  margin: auto;
  background-color: white;
}}
th {{
  background-color: #2c3e50;
  color: white;
  padding: 10px;
}}
td {{
  padding: 8px;
  border: 1px solid #ddd;
}}
tr:nth-child(even) {{background-color: #f2f2f2;}}
</style>
</head>
<body>

<h1>Order Tracking Automation Report</h1>
<p style="text-align:center;">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

<table>
<tr>
<th>Order ID</th>
<th>Phone</th>
<th>Status Result</th>
<th>Checked Time</th>
<th>URL Check</th>
<th>Phone Field Check</th>
<th>Order Status Check</th>
<th>Final Result</th>
</tr>
"""

for r in results:
    html_content += f"""
<tr>
<td>{r['order_id']}</td>
<td>{r['phone']}</td>
<td>{r['status']}</td>
<td>{r['time']}</td>
<td>{r['url_check']}</td>
<td>{r['phone_field_check']}</td>
<td>{r['order_status_check']}</td>
<td>{r['final_result']}</td>
</tr>
"""

html_content += """
</table>
</body>
</html>
"""

# Save report
report_path = r"C:\Users\GowsikaSurendran\Downloads\AutomationTesting\order_report.html"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Report saved at:", report_path)
input("All done! Press Enter to close browser...")
driver.quit()