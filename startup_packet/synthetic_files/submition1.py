import pandas as pd

def split_products(input_file, output_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_file)

    # Split the 'product' column into three new columns: 'product1_id', 'product2_id', 'product3_id'
    product_split = df['product'].str.split(', ', expand=True)

    # Assign the new columns to the DataFrame
    df['product1_id'] = product_split[0]
    df['product2_id'] = product_split[1]
    df['product3_id'] = product_split[2]

    # Drop the original 'product' column if needed
    # df.drop(columns=['product'], inplace=True)

    # Write the modified DataFrame back to an Excel file
    df.to_excel(output_file, index=False)
    print(f"File processed and saved as {output_file}")

# Example usage
input_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_extraction.xlsx'
output_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_splitting_product.xlsx'
split_products(input_file, output_file)
