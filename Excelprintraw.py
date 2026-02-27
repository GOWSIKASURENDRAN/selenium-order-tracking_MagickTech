import pandas as pd

# --------------------------------------------------
# Step 1: Provide the Excel file path
# --------------------------------------------------
file_path = r"C:\Users\GowsikaSurendran\Downloads\Excel import practise\orders - Copy.xlsx"

# --------------------------------------------------
# Step 2: Read the Excel file into DataFrame
# --------------------------------------------------
df = pd.read_excel(file_path)

# --------------------------------------------------
# Step 3: Replace empty cells (NaN) with "NULL"
# This avoids showing 'nan' in console output
# --------------------------------------------------
df = df.fillna("NULL")

# --------------------------------------------------
# Step 4: Update STATUS for specific Order_ID
# --------------------------------------------------
df.loc[df['Order_ID'] == 926727, 'STATUS'] = "D-DELIVERED"

# --------------------------------------------------
# Step 5: Print data row-wise (horizontal format)
# --------------------------------------------------
print("Data in Excel (Row-wise):\n")

# Print column headers
print(" | ".join(df.columns))

# Print separator line
print("-" * 120)

# Loop through each row and print values side-by-side
for index, row in df.iterrows():
    print(" | ".join(str(value) for value in row))