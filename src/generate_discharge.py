import json
import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load .env before accessing any environment variables
load_dotenv()

def load_consultation_data(path):
    with open(path, 'r') as f:
        return json.load(f)

def generate_prompt(consultation_data):
    return f"""You are a veterinary assistant. Write a discharge note for the pet based on the following consultation data:

Patient:
- Name: {consultation_data['patient']['name']}
- Species: {consultation_data['patient']['species']}
- Breed: {consultation_data['patient']['breed']}
- Gender: {consultation_data['patient']['gender']}
- Neutered: {consultation_data['patient']['neutered']}
- Date of Birth: {consultation_data['patient']['date_of_birth']}
- Weight: {consultation_data['patient']['weight']}

Consultation:
- Date: {consultation_data['consultation']['date']}
- Time: {consultation_data['consultation']['time']}
- Reason: {consultation_data['consultation']['reason']}
- Notes: {[note['note'] for note in consultation_data['consultation'].get('clinical_notes', [])]}
- Procedures: {[proc['name'] for proc in consultation_data['consultation']['treatment_items'].get('procedures', [])]}

Please write a short and friendly discharge summary explaining what was done and what to do next.
"""

def call_openai(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()

def save_output(output_path, note):
    with open(output_path, 'w') as f:
        json.dump({"discharge_note": note}, f, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_discharge.py path/to/consultation.json")
        sys.exit(1)

    input_path = sys.argv[1]
    base_name = os.path.basename(input_path)
    output_path = os.path.join("solution", base_name)

    data = load_consultation_data(input_path)
    prompt = generate_prompt(data)
    note = call_openai(prompt)
    save_output(output_path, note)
    print(f"✅ Discharge note generated: {output_path}")

if __name__ == "__main__":
    main()