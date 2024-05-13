from bs4 import BeautifulSoup
import requests
import csv

# A list that will contain all the claims from all the patents
total_lst = []

# Function to extract claims text from a patent URL
def extract_claims(patent_url):
    claims_list = []
    response = requests.get(patent_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Identify the HTML elements containing the claims
    claim_divs = soup.find_all('div', {'class': 'claim'})
    if claim_divs:
        for div in claim_divs:
            claim_text = div.get_text(strip=True)  # Get text and remove leading/trailing whitespace
            claims_list.append(claim_text)
            total_lst.append(claim_text)
        return claims_list
    else:
        return None

# Patents URLs
patent_urls = [
    "https://patents.google.com/patent/GB2478972A/en?q=(phone)&oq=phone",
    "https://patents.google.com/patent/US9634864B2/en?oq=US9634864B2",
    "https://patents.google.com/patent/US9980046B2/en?oq=US9980046B2"
]


# Extract claims from each patent
for url in patent_urls:
    claims = extract_claims(url)

# Remove any duplicates from a List:
total_lst = list(dict.fromkeys(total_lst))

# Save all the claims to csv file
# Define the file name for your CSV
file_name = "claims.csv"

# Write the claims to the CSV file
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Claims'])
    # Write the claims
    for claim in total_lst:
        writer.writerow([claim])

