import csv
import re

# Define the path of the nginx access log and the output CSV file
log_file_path = '/var/log/nginx/access.log'
csv_file_path = 'accessLog.csv'  # Change this to your desired output path

# Regex for parsing the log file lines
log_pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\[(?P<timestamp>.*?)\] "(?P<method>[A-Z]+) (?P<endpoint>.*?) HTTP/1.[0-1]"'

# Open the log file and prepare to parse it
with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Timestamp', 'IP', 'Endpoint'])  # Writing the headers

    # Read the log file line by line
    for line in log_file:
        match = re.match(log_pattern, line)
        if match:
            data = match.groupdict()
            csv_writer.writerow([data['timestamp'], data['ip'], data['method'] + ' ' + data['endpoint']])


# Clear the log file (uncomment the line below to enable this functionality)
open(log_file_path, 'w').close()
