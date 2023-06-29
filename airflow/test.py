# import os
# import pandas as pd
# import zipfile

# parquet_name = 'output.parquet'
# csv_name = 'output.csv'
# url = "https://s3.amazonaws.com/tripdata/JC-201509-citibike-tripdata.csv.zip"
# extract_path = 'extracted_files/'  # Destination directory for extraction

# # Download the .csv.zip file
# os.system(f"wget {url} -O {csv_name}.zip")

# # Extract the .csv file from the zip file
# with zipfile.ZipFile(f"{csv_name}.zip", 'r') as zip_ref:
#     zip_ref.extractall(extract_path)

# # Get the extracted file name
# extracted_file = zip_ref.namelist()[0]
# extracted_csv_path = os.path.join(extract_path, extracted_file)

# # Read the extracted CSV file
# df = pd.read_csv(extracted_csv_path)

# # Specify the absolute or relative path for the output CSV file
# output_csv_path = os.path.join(os.getcwd(), csv_name)

# # Save as a CSV file
# df.to_csv(output_csv_path, index=False)

# # Clean up - delete the downloaded .csv.zip file and extracted .csv file
# os.remove(f"{csv_name}.zip")
# os.remove(extracted_csv_path)






import os
import pandas as pd
import zipfile

parquet_name = 'output.parquet'
csv_name = 'output.csv'
url = "https://s3.amazonaws.com/tripdata/JC-201509-citibike-tripdata.csv.zip"

# Download the .csv.zip file
os.system(f"wget {url} -O {csv_name}.zip")

# Extract the .csv file from the zip file in the current directory
with zipfile.ZipFile(f"{csv_name}.zip", 'r') as zip_ref:
    zip_ref.extractall()

# Get the extracted file name
extracted_file = zip_ref.namelist()[0]
extracted_csv_path = os.path.join(os.getcwd(), extracted_file)

# Read the extracted CSV file
df = pd.read_csv(extracted_csv_path)

# Specify the absolute or relative path for the output CSV file
output_csv_path = os.path.join(os.getcwd(), csv_name)

# Save as a CSV file
df.to_csv(output_csv_path, index=False)

# Clean up - delete the downloaded .csv.zip file and extracted .csv file
os.remove(f"{csv_name}.zip")
os.remove(extracted_csv_path)




