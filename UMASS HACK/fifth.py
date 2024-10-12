import pandas as pd

def replace_instrument_names(input_file, machine_mapping_file, report_mapping_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Read the machine mapping and report mapping CSV files
    machine_mapping_df = pd.read_csv(machine_mapping_file)
    report_mapping_df = pd.read_csv(report_mapping_file)

    # Create a mapping dictionary for machines and reports
    machine_mapping = pd.Series(machine_mapping_df['machine_id'].values, index=machine_mapping_df['machine_name']).to_dict()
    report_mapping = pd.Series(report_mapping_df['report_id'].values, index=report_mapping_df['report']).to_dict()

    # Replace the instrument names with codes
    df['instrument'] = df['instrument'].map(machine_mapping).fillna(df['instrument'])  # Only change if found in mapping
    df['report_id'] = df['report_id'].map(report_mapping).fillna(df['report_id'])  # Only change if found in mapping

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"File processed and saved as {output_file}")

# Example usage
input_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\2.csv'  # Input file with report_id and instrument
machine_mapping_file = r'S:\\Hack\\startup_packet\\startup_packet\\machine_mapping.csv'  # Machine mapping file
report_mapping_file = r'S:\\Hack\\startup_packet\\startup_packet\\report_mapping.csv'  # Report mapping file
output_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_final.csv'  # Output file with replaced instrument names

replace_instrument_names(input_file, machine_mapping_file, report_mapping_file, output_file)
