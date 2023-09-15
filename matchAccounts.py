import os
import csv
import time
from fuzzywuzzy import fuzz

start = time.time()

def read_account_info(file_path):
    
    # Read the account information from a file and return as a list or dictionary
    account_info = []
    with open(file_path, 'r') as file:
        # Code to read the file and extract account information
        # Example: assuming each line in the file represents an account with name, city, and country separated by a comma
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        for line in file:
            
            split_values = line.strip().split(',')
            if len(split_values) == 4:
               id, name, city, business_Unit = split_values
               account_info.append({'id': id, 'name': name, 'city': city, 'Business_Unit': business_Unit})
            elif len(split_values) == 5:
               line = line.strip().split(',')
               # Remove the comma from the second column (index 1)
               for i in range(len(line)):
                   line[i] = line[i].replace(',', '')
                   line[i] = line[i].replace('"', '')
                   line[i] = line[i].replace(' , ', '')

               merged_value = line[1] + line[2]
               merged_line =line[:1] + [merged_value] + line[3:]
              
               line = ','.join(merged_line)
               
               id, name, city, business_Unit = line.split(',')
               account_info.append({'id': id, 'name': name, 'city': city, 'Business_Unit': business_Unit})
    return account_info

# Directory path where the account information files are located
directory_path = os.environ.get('SOURCE_DIRECTORY', 'source_documents')

if directory_path is None:
    print("Environment variable 'DIRECTORY_NAME' is not set.")
    exit()

# List of file names for account information
#file_names = ['TagetikAADB.csv', 'FRRAADB.csv']

final_directory_path = os.path.join(os.getcwd(), directory_path)

# List all files in the directory
file_names = os.listdir(final_directory_path)


# Dictionary to store matched accounts
matched_accounts = {}

# Read account information from each file and match accounts
for file_name in file_names:
    print(file_name)
    file_path = os.path.join(final_directory_path, file_name)
    account_info = read_account_info(file_path)
    for account in account_info:
        # Assuming 'id', 'name', 'city', and 'country' are the account attributes for fuzzy matching
        account_id = account['id']
        name = account['name']
        city = account['city']
        Business_Unit = account['Business_Unit']
        matched = False
        for matched_key in matched_accounts.keys():
            value = matched_accounts.get(matched_key)
            
            TMID,TGKID,TGKTAXID,FRRID, Name, City, Business_Unit = matched_key
            
            name_similarity = fuzz.ratio(name, Name)
            city_similarity = fuzz.ratio(city, City)
            #country_similarity = fuzz.ratio(country, matched_country)
            if (
                name_similarity >= 65
                and city_similarity >= 60
                #and country_similarity >= 80
            ):  # Adjust the thresholds as per your requirements
                matched_accounts[matched_key].append(account_id)
                matched = True
                #break
        if not matched:
            
            values = matched_accounts.get(account_id)
            
            if values is not None:
            # Unpack the values into variables
             TMID, TGKID, TGKTAXID, FRRID, Name, City, Business_Unit = values
            elif Business_Unit == 'Tagetik':
               matched_accounts[('',account_id,'','', name, city, Business_Unit)] = [account_id]
            elif Business_Unit == 'Teammate':
               matched_accounts[(account_id,'','','', name, city, Business_Unit)] = [account_id]
            elif Business_Unit == 'FRR':
               matched_accounts[('','','',account_id, name, city, Business_Unit)] = [account_id]
            elif Business_Unit == 'Tagetik Tax':
               matched_accounts[('','',account_id,'', name, city, Business_Unit)] = [account_id]
            
# Write matched accounts to a CSV file
output_file = 'matched_accounts.csv'
output_file_path = os.path.join(directory_path, output_file)
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['TMID','TGKID','TGKTAXID','FRRID', 'Name', 'City', 'Business_Unit'])  # Write header
    for key, account_ids in matched_accounts.items():
        TMID,TGKID,TGKTAXID,FRRID, name, city, bu = key
        for account_id in account_ids:
            writer.writerow([TMID,TGKID,TGKTAXID,FRRID, name, city, bu])
end = time.time()
print(f"\n> Answer (took {round(end - start, 2)} s.):")
print(f"Matched accounts have been written to '{output_file_path}' file.")
