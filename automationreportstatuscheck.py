# Import modules
import time
from datetime import datetime
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Python script is running!")

# -------------------------------
# Setup Chrome Driver
# -------------------------------
chrome_options = Options()
service = Service(r"C:\Users\GowsikaSurendran\Downloads\AutomationTesting\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# -------------------------------
# Backend Orders Data
# -------------------------------
orders = [
    {"order_id": "0926727", "phone": "7174694371", "order_type": "D-DISPATCHED"},
    {"order_id": "0929890", "phone": "6306327433", "order_type": "D-DISPATCHED"},
    {"order_id": "0932116", "phone": "8477442218", "order_type": "D-DISPATCHED"},
    {"order_id": "0932124", "phone": "8477442218", "order_type": "D-Dispatched"},
    {"order_id": "0934766", "phone": "7176379320", "order_type": "D-Dispatched"}
]

# -------------------------------
# Map Backend ORDER_TYPE
# -------------------------------
def map_order_type(order_type):
    order_type = order_type.upper().strip()  # Normalize to uppercase

    if "DISPATCHED" in order_type:
        return "DISPATCHED"
    elif "SHIP READY" in order_type:
        return "SHIP READY"
    elif "IN TRANSIT" in order_type:
        return "IN TRANSIT"
    else:
        return order_type  # fallback, use as-is

# -------------------------------
# Store Results
# -------------------------------
results = []

# -------------------------------
# Open Tracking Page
# -------------------------------
driver.get("https://www.magickwoods.com/track/")

# Accept cookies if popup appears
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

# -------------------------------
# Validation Loop
# -------------------------------
for order in orders:

    # Enter Order ID
    order_input = wait.until(
        EC.presence_of_element_located((By.ID, "order_id"))
    )
    order_input.clear()
    order_input.send_keys(order["order_id"])

    # Enter Phone
    phone_input = wait.until(
        EC.presence_of_element_located((By.ID, "phone_no"))
    )
    phone_input.clear()
    phone_input.send_keys(order["phone"])

    # Click Get Status
    track_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Get Status')]")
        )
    )
    track_button.click()

    print(f"Checking Order: {order['order_id']}")

    # -------------------------------
    # Get Website Status Properly
    # -------------------------------
    try:
        # Wait until status text is not empty
        wait.until(
            lambda d: d.find_element(By.ID, "order_status_res").text.strip() != ""
        )

        status_element = driver.find_element(By.ID, "order_status_res")
        actual_status = status_element.text.strip().upper()  # normalize to uppercase

        # Remove word "PRODUCT" if present
        actual_status = actual_status.replace("PRODUCT", "").strip()

        print("Website Status:", actual_status)

    except Exception as e:
        actual_status = "NOT FOUND"
        print("Status not found:", e)

    # -------------------------------
    # URL Check
    # -------------------------------
    try:
        response = requests.head(driver.current_url, timeout=5)
        url_status = "PASS" if response.status_code == 200 else "FAIL"
    except:
        url_status = "FAIL"

    # -------------------------------
    # Phone Field Check
    # -------------------------------
    try:
        driver.find_element(By.ID, "phone_no")
        phone_field_status = "PASS"
    except:
        phone_field_status = "FAIL"

    # -------------------------------
    # Backend vs Website Comparison
    # -------------------------------
    expected_status = map_order_type(order["order_type"])

    if actual_status == expected_status:
        order_status_check = "PASS"
    else:
        order_status_check = "FAIL"

    # -------------------------------
    # Final Result
    # -------------------------------
    final_result = "PASS" if (
        url_status == "PASS"
        and phone_field_status == "PASS"
        and order_status_check == "PASS"
    ) else "FAIL"

    # Save Result
    results.append({
        "order_id": order["order_id"],
        "phone": order["phone"],
        "expected_status": expected_status,
        "actual_status": actual_status,
        "url_check": url_status,
        "phone_field_check": phone_field_status,
        "order_status_check": order_status_check,
        "final_result": final_result,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Reload page for next order
    driver.get("https://www.magickwoods.com/track/")

# -------------------------------
# Generate HTML Report
# -------------------------------
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
.pass {{background-color:#d4edda;}}
.fail {{background-color:#f8d7da;}}
</style>
</head>
<body>

<h1>Order Tracking Automation Report</h1>
<p style="text-align:center;">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

<table>
<tr>
<th>Order ID</th>
<th>Phone</th>
<th>Expected Status</th>
<th>Actual Status</th>
<th>Checked Time</th>
<th>URL Check</th>
<th>Phone Field Check</th>
<th>Status Match</th>
<th>Final Result</th>
</tr>
"""

for r in results:
    row_class = "pass" if r["final_result"] == "PASS" else "fail"
    html_content += f"""
<tr class="{row_class}">
<td>{r['order_id']}</td>
<td>{r['phone']}</td>
<td>{r['expected_status']}</td>
<td>{r['actual_status']}</td>
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

# Save Report
report_path = r"C:\Users\GowsikaSurendran\Downloads\AutomationTesting\order_report.html"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Report saved at:", report_path)

input("All done! Press Enter to close browser...")
driver.quit()