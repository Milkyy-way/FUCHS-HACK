from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

# Load the files: instrument data and machine mapping data
instrument_data_path = 'S:\\Hack\\startup_packet\\startup_packet\\synthetic_files\\hack2_mapped_output_product.xlsx'
machine_mapping_path = 'S:\\Hack\startup_packet\\startup_packet\\machine_mapping.csv'

# Load the data
instrument_df = pd.read_excel(instrument_data_path)
machine_mapping_df = pd.read_csv(machine_mapping_path)

# Remove rows with missing values or values like '---' only for the 'instrument' column
cleaned_instrument_df = instrument_df.copy()
cleaned_instrument_df['instrument'] = cleaned_instrument_df['instrument'].replace('---', pd.NA).fillna('')  # Replace NaNs with empty strings

# Combine the instrument names and machine names into a single list for vectorization
all_names = cleaned_instrument_df['instrument'].tolist() + machine_mapping_df['machine_name'].tolist()

# Convert names into TF-IDF vectors
vectorizer = TfidfVectorizer().fit_transform(all_names)
vectors = vectorizer.toarray()

# Split the vectors back into instrument and machine vectors
instrument_vectors = vectors[:len(cleaned_instrument_df)]
machine_vectors = vectors[len(cleaned_instrument_df):]

# Function to find the closest machine name based on cosine similarity
def find_closest_machine_name(instrument_vector):
    similarities = cosine_similarity([instrument_vector], machine_vectors)
    closest_match_index = np.argmax(similarities)
    return machine_mapping_df.iloc[closest_match_index]['machine_name']

# Apply the mapping for the 'instrument' column
cleaned_instrument_df['instrument'] = instrument_vectors.tolist()
cleaned_instrument_df['instrument'] = cleaned_instrument_df['instrument'].apply(find_closest_machine_name)

# Save the cleaned and mapped data to a new CSV file, keeping all other columns intact
output_csv_path = '2.csv'
cleaned_instrument_df.to_csv(output_csv_path, index=False)

print(f"Cleaned and mapped data saved to {output_csv_path}")