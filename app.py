from flask import Flask, render_template, request
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = OpenAI()

def format_payload(company_profile, job_description, job_requirements, job_benefits):
    payload = f"Company Profile: {company_profile} ; Job Description: {job_description} ; Requirements: {job_requirements} ; Benefits: {job_benefits} ;"
    return payload

@app.route('/', methods=['GET', 'POST'])
def index():
    system_prompt = "You will act as a job scam detector, analyzing the authenticity of a job offer based on the information provided by the user in the following format: Company Profile: {Provide a brief description of the company, its background, and industry.} Job Description: {Summarize the details of the job, including responsibilities and tasks.} Requirements: {List the qualifications and skills required for the job.} Benefits: {Enumerate the perks, compensation, and benefits offered with the job.} Please evaluate if the job offer appears to be a potential scam based on the following criteria:      The offer seems too good to be true, e.g. promising a lot of money for very little work.     There is a false sense of urgency, and the recruiter places you under pressure to act quickly.     The job involves receiving products, repackaging them, or transferring funds, which may be associated with illegal activities.     The job email contains spelling or grammar mistakes, or the company name is slightly altered.     The email sender address is a private email account (e.g., Gmail, Yahoo).     The hiring process seems too simple or fast, with no in-person or video interviews.     The job requires you to pay for something from your bank account or share personal financial information early in the application process.     You are asked to use a special app or move to a different site for further communications.     You are offered a job without the employer checking references or verifying your experience.  Provide a clear verdict (Scam or Not Scam) on whether the job offer appears to be a potential scam or not based on your analysis."
    if request.method == 'POST':
        company_profile = request.form['company_profile']
        job_description = request.form['job_description']
        job_requirements = request.form['job_requirements']
        job_benefits = request.form['job_benefits']

        system_message = {"role": "system", "content": system_prompt}
        # Format the input for OpenAI API
        user_input = format_payload(company_profile, job_description, job_requirements, job_benefits)

        # Create a message using user input
        user_message = {"role": "user", "content": user_input}

        # Send request to OpenAI API
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0613:personal::8P1FVa43",
            messages=[system_message, user_message]
        )
        # Extract and display the API response
        api_output = response.choices[0].message.content

        return render_template('index.html', user_input=(company_profile,job_description,job_requirements,job_benefits), api_output=api_output)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
