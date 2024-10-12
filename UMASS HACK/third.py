import pandas as pd

def map_product_codes(input_file, mapping_file, output_file):
    # Read the main Excel file with product names
    df = pd.read_excel(input_file)

    # Read the product mapping Excel file
    mapping_df = pd.read_csv(mapping_file)

    # Create a dictionary for mapping product names to product IDs
    product_mapping = pd.Series(mapping_df['product_id'].values, index=mapping_df['product_name']).to_dict()

    # Map the product names to product IDs in the three columns
    df['product1_id'] = df['product1_id'].map(product_mapping)
    df['product2_id'] = df['product2_id'].map(product_mapping)
    df['product3_id'] = df['product3_id'].map(product_mapping)

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_file, index=False)
    print(f"File processed and saved as {output_file}")

# Example usage
input_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_splitting_product.xlsx'  # Input file with product columns
mapping_file = r'S:\\Hack\\startup_packet\\startup_packet\\product_mapping.csv'  # Product mapping file
output_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_mapped_output_product.xlsx'  # Output file with product codes

map_product_codes(input_file, mapping_file, output_file)
