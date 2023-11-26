import pandas as pd
import random
import json

# Load the CSV file into a DataFrame
df = pd.read_csv('fake_job_postings.csv')

# Separate rows into scams and not scams
scam_rows = df[df['fraudulent'] == 1]
not_scam_rows = df[df['fraudulent'] == 0]

# Extract 20 random rows for scams and not scams
# used for training data set
#random_scam_rows = scam_rows.sample(n=20, random_state=42)
#random_not_scam_rows = not_scam_rows.sample(n=20, random_state=42)

random_scam_rows = scam_rows.sample(n=10, random_state=10)
random_not_scam_rows = not_scam_rows.sample(n=10, random_state=10)

# Function to convert row to the desired format
def row_to_json(row):
    if row['fraudulent'] == 1:
        answer = "Scam"
    else:
        answer = "Not Scam"
    return '''{"messages": [{"role": "system","content": "You will act as a job scam detector, analyzing the authenticity of a job offer based on the information provided by the user in the following format: Company Profile: {Provide a brief description of the company, its background, and industry.} Job Description: {Summarize the details of the job, including responsibilities and tasks.} Requirements: {List the qualifications and skills required for the job.} Benefits: {Enumerate the perks, compensation, and benefits offered with the job.} Please evaluate if the job offer appears to be a potential scam based on the following criteria:      The offer seems too good to be true, e.g. promising a lot of money for very little work.     There is a false sense of urgency, and the recruiter places you under pressure to act quickly.     The job involves receiving products, repackaging them, or transferring funds, which may be associated with illegal activities.     The job email contains spelling or grammar mistakes, or the company name is slightly altered.     The email sender address is a private email account (e.g., Gmail, Yahoo).     The hiring process seems too simple or fast, with no in-person or video interviews.     The job requires you to pay for something from your bank account or share personal financial information early in the application process.     You are asked to use a special app or move to a different site for further communications.     You are offered a job without the employer checking references or verifying your experience.  Provide a clear verdict (Scam or Not Scam) on whether the job offer appears to be a potential scam or not based on your analysis."},{"role": "user","content": " Company Profile: ''' + str(row['company_profile']).replace('"',"'") + '''; Job Description: ''' + str(row['description']).replace('"',"'")  + '''; Requirements: ''' + str(row['requirements']).replace('"',"'")  + '''; Benefits: ''' + str(row['benefits']).replace('"',"'")  + '''; "},{"role": "assistant","content": "''' + answer + '''"}]}'''

# Convert selected rows to the desired format
scam_json = [row_to_json(row) for _, row in random_scam_rows.iterrows()]
print(scam_json[0])
not_scam_json = [row_to_json(row) for _, row in random_not_scam_rows.iterrows()]

# Combine scam and not scam JSONs
output_json = scam_json + not_scam_json

# Write the output to a JSON file
#with open('output.json', 'w') as json_file:
#    json.dump(output_json, json_file, indent=2)

with open('test_data.json', 'w', encoding='utf-8') as json_file:
    for _ in output_json:
        json_file.write(_)
        json_file.write("\n")

print("Output written to 'output.json'")
