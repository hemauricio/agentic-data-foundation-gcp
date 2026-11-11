import csv
import random
import uuid

# Define the file and headers
filename = 'synthetic_telco_churn.csv'
headers = ['customerID', 'MonthlyCharges', 'TotalCharges', 'tenure', 'Churn']

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for _ in range(5000):
        customer_id = str(uuid.uuid4())
        tenure = random.randint(1, 72)
        monthly_charges = round(random.uniform(20.0, 120.0), 2)
        total_charges = round(tenure * monthly_charges, 2)
        
        # Create a pattern for BigQuery ML to find:
        # High monthly charges + low tenure = high probability of Churn
        if tenure < 12 and monthly_charges > 85.0:
            churn_prob = 0.75
        elif tenure > 48:
            churn_prob = 0.10
        else:
            churn_prob = 0.30
            
        churn = "Yes" if random.random() < churn_prob else "No"
        
        writer.writerow([customer_id, monthly_charges, total_charges, tenure, churn])

print(f"Successfully generated 5,000 rows in {filename}")
