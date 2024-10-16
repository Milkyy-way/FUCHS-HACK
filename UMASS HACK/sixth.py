# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gWrgDA16S5ZYvIpOIDRJQ9pcsQsWbv8c
"""

from google.colab import drive
drive.mount('/content/drive')

# Assuming your file 'final.csv' is inside the 'startup_packet/synthetic_files/' folder in your Google Drive
file_path = '/content/drive/MyDrive/hack2_final.csv'  # Update with your actual path
import pandas as pd
df = pd.read_csv(file_path)

# Show the first few rows of the DataFrame
df.head()

import re

# Function to clean 'result' column
def clean_result_column(row):
    result = row['result']
    if isinstance(result, str):
        # Check if there is a unit in the result and separate it
        match = re.match(r"([0-9.]+)\s*([a-zA-ZÂ°C]+)", result)
        if match:
            value, unit = match.groups()
            row['result'] = float(value)
            row['unit_id'] = unit
        else:
            # Remove non-numeric words from result (like "Thermal Profile", "Viscosity")
            row['result'] = re.sub(r"[a-zA-Z\s]+", "", result)

    # Ensure two decimal places for numeric values
    try:
        row['result'] = round(float(row['result']), 2)
    except ValueError:
        pass  # In case the result is not convertible to float, keep it as is

    return row

# Apply the cleaning function to each row in the DataFrame
df_cleaned = df.apply(clean_result_column, axis=1)

# Show the cleaned DataFrame
df_cleaned.head()

df_cleaned.to_csv('hack2_output.csv', index=False)