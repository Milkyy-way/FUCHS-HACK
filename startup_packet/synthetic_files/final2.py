import pandas as pd

def clean_result_column(input_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Define a function to clean the result column
    def clean_result(value):
        if isinstance(value, str):
            # Replace text with an empty string if it's not numeric
            if not value.strip().replace('.', '', 1).isdigit():  # Allow one decimal point
                return ''  # Remove text
        return value  # Return the original value if it's numeric

    # Apply the cleaning function to the result column
    df['result'] = df['result'].apply(clean_result)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processed file saved as {output_file}")

# Example usage
input_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\final.csv'  # Input file
output_file = r'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\final_cleaned.csv'  # Output file

clean_result_column(input_file, output_file)
