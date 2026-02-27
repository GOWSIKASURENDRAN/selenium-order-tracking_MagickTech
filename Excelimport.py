import pandas as pd

# File path
file_path = r"C:\Users\GowsikaSurendran\Downloads\Excel import practise\orders.xlsx"

# Read Excel
df = pd.read_excel(file_path)

print("Existing Data in Excel:")
print(df)

# Create new row as DICTIONARY
new_row_data = {
    "Order_ID": 930001,
    "CUSTOMER_ID": "ACD003",
    "CONTACT_PHONE": "7177654321",
    "STATUS": "C",
    "ORDER_TYPE": "D-DISPATCHED",
    "BOL_ID": 272552,
    "CARRIER_ID": "ACD Logistics LLC",
    "PRO_NUMBER": 1272031,
    "RECEIVED_STATUS": "NULL"
}

# Convert dictionary into DataFrame (IMPORTANT)
new_row_df = pd.DataFrame([new_row_data])

# Add new row properly
df = pd.concat([df, new_row_df], ignore_index=True)

# Update existing row
df.loc[df['Order_ID'] == 926727, 'STATUS'] = "D-DELIVERED"

# Save back to Excel
df.to_excel(file_path, index=False)

print("\nUpdated Data in Excel:")
print(df)