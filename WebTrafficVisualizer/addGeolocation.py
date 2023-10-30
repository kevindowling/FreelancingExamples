import csv
import requests
import json
import os 


filename = 'accessLog.csv'
ips = set()

with open(filename, mode ='r')as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        ips.add(lines['IP'])


batch_size = 100  # max size accepted by ip-api
ip_batches = [list(ips)[i:i + batch_size] for i in range(0, len(ips), batch_size)]


url = "http://ip-api.com/batch"
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
}
geolocations = {}

for ip_batch in ip_batches:
    payload = json.dumps([{"query": ip} for ip in ip_batch])
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        results = response.json()
        for result in results:
            if 'query' in result and 'status' in result and result['status'] == 'success':
                # Store the needed geolocation data, for instance, 'country', 'region', 'city'.
                geolocations[result['query']] = {
                    'geolocation': f"{result['country']}, {result['regionName']}, {result['city']}",
                    'latitude': result.get('lat', 'N/A'),
                    'longitude': result.get('lon', 'N/A')
                }    
            else:
                print(f"Failed to get geolocation for batch: {ip_batch}")

new_filename = 'geolocated_' + filename

file_exists = os.path.isfile(new_filename)

with open(filename, mode='r') as infile, open(new_filename, mode='a', newline='') as outfile:
    reader = csv.reader(infile)

    if not file_exists:
        writer = csv.writer(outfile)
        headers = next(reader)
        headers.extend(['Geolocation', 'Latitude', 'Longitude'])  # Add new headers
        writer.writerow(headers)
    else:
        next(reader)  # Skip headers if they already exist

    for row in reader:
        ip = row[1]
        geolocation_info = geolocations.get(ip, {})
        geolocation = geolocation_info.get('geolocation', 'Not found')
        latitude = geolocation_info.get('latitude', 'N/A')
        longitude = geolocation_info.get('longitude', 'N/A')

        row.extend([geolocation, latitude, longitude])  # Append new data
        writer = csv.writer(outfile)
        writer.writerow(row)

print(f"Data appended to {new_filename}")

print(f"New file with geolocations written to {new_filename}")

try:
    if os.path.isfile(filename):  # Ensuring that the file exists before trying to delete it
        os.remove(filename)
        print(f"Original file {filename} has been deleted.")
    else:
        print(f"File {filename} not found, could not delete.")
except Exception as e:
    print(f"An error occurred while trying to delete file {filename}: {e}")