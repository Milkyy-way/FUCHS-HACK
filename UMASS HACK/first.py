import os
import pandas as pd
from docx import Document

# Define mappings for the columns
COLUMN_MAPPINGS = {
    'machine_id': ['Instrument', 'Device', 'Spectrometer', 'Technique', 'Method','Equipment Used', 'Primary Substance', 'Additives', 'Equipment', 'Additive'],
    'product': ['Mixture Components', 'Sample', 'Ingredients', 'Mixture Composition', 'Mixture composition', 'sample combination', 'test instrument', 'Instrumentation', 'Mixture Components', 'Sample Composition'],
    'result': ['Measurement', 'Result', 'Measurement Value', 'Measurement value', 'Measurements', 'Mass/Charge','Wavelength (cm-1)','Observed Wavelength (nm)']
}

# Function to find the correct column based on mappings
def find_column(df, possible_columns):
    for col in possible_columns:
        if col in df.columns:
            return df[col]
    return None

# Function to extract data from Word documents
def process_word_file(filepath, report_id):
    all_data = []
    doc = Document(filepath)

    for table in doc.tables:
        # Extract the table data into a pandas DataFrame
        data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(data)
        
        # Find the relevant columns
        instrument_col = find_column(df, COLUMN_MAPPINGS['machine_id'])
        product_col = find_column(df, COLUMN_MAPPINGS['product'])
        result_col = find_column(df, COLUMN_MAPPINGS['result'])

        if instrument_col is not None and product_col is not None and result_col is not None:
            # Combine the relevant columns into a new DataFrame
            combined_df = pd.DataFrame({
                'report_id': report_id,  # Add the report_id column
                'instrument': instrument_col,
                'product': product_col,
                'result': result_col
            })
            all_data.append(combined_df)
    
    return all_data

def process_files(input_directory, output_file):
    all_data = []

    # Ensure the correct handling of file paths
    input_directory = os.path.abspath(input_directory)
    
    # Iterate through all files in the directory and process Excel and Word files
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        
        # Extract the report ID (filename without the extension)
        report_id = os.path.splitext(filename)[0]
        
        # Process Excel files
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            xls = pd.ExcelFile(filepath)
            
            # Iterate through each sheet in the Excel file
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # Find the relevant columns
                instrument_col = find_column(df, COLUMN_MAPPINGS['machine_id'])
                product_col = find_column(df, COLUMN_MAPPINGS['product'])
                result_col = find_column(df, COLUMN_MAPPINGS['result'])

                if instrument_col is not None and product_col is not None and result_col is not None:
                    # Combine the relevant columns into a new DataFrame
                    combined_df = pd.DataFrame({
                        'report_id': report_id,  # Add the report_id column
                        'instrument': instrument_col,
                        'product': product_col,
                        'result': result_col
                    })
                    all_data.append(combined_df)
        
        # Process Word files
        elif filename.endswith(".docx"):
            word_data = process_word_file(filepath, report_id)
            all_data.extend(word_data)
    
    # Concatenate all data and write to a new Excel file
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_excel(output_file, index=False)
        print(f"Extraction complete. Data saved to {output_file}.")
    else:
        print("No data found to extract.")

# Example usage
input_directory = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\reports_2024-09-26_00-39-17'
output_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_extraction.xlsx'
process_files(input_directory, output_file)
