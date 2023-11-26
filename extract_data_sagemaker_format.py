import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Load the CSV file into a DataFrame
df = pd.read_csv('fake_job_postings.csv')

# Separate rows into scams and not scams
scam_rows = df[df['fraudulent'] == 1]
not_scam_rows = df[df['fraudulent'] == 0]

# Extract random rows for scams and not scams
random_scam_rows = scam_rows
random_not_scam_rows = not_scam_rows.sample(n=len(scam_rows.index), random_state=10)

# Function to convert row to the desired format
def row_to_json(row):
    return [
        '''Company Profile: ''' + str(row['company_profile']).replace('"',"'") + 
        '''; Job Description: ''' + str(row['description']).replace('"',"'") +
        '''; Requirements: ''' + str(row['requirements']).replace('"',"'") +
        '''; Benefits: ''' + str(row['benefits']).replace('"',"'"),
        int(row['fraudulent'])
    ]

# Convert selected rows to the desired format
scam_json = [row_to_json(row) for _, row in random_scam_rows.iterrows()]
not_scam_json = [row_to_json(row) for _, row in random_not_scam_rows.iterrows()]

# Combine scam and not scam JSONs
output = scam_json + not_scam_json

# Define the schema based on your data
schema = pa.schema([
    ('Text', pa.string()),  # Assuming your text data goes here
    ('Label', pa.int32())   # Assuming your label (fraudulent) is an integer
])

# Separate data into two arrays based on the schema
texts = [item[0] for item in output]
labels = [item[1] for item in output]

# Create Arrow table
table = pa.table({'Text': texts, 'Label': labels}, schema=schema)

# Specify the Parquet file name
parquet_file = 'train_sagemaker.parquet'

# Write the Arrow Table to a Parquet file
pq.write_table(table, parquet_file)

print("Program ran successfully.")
