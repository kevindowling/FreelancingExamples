from flask import Flask, request, jsonify
import csv
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/trafficdata": {"origins": "http://127.0.0.1:5500"}})  # replace with your frontend's actual origin

# Replace this with the actual location of your server.
SERVER_COORDINATES = [40.7128, -74.0060] #New York, New York
WHITELISTED_TRAFFIC = ["/","/api/simulate", "/assets/*", "/blog*"]

def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%d/%b/%Y:%H:%M:%S %z')

def isLegitimateTraffic(request):
    # Split the request string on the space character
    parts = request.split(" ", 1)
    
    # If there's no space or more than one space, return False
    if len(parts) != 2:
        return False
    
    # Take the substring after the space
    request_substring = parts[1]
    
    for pattern in WHITELISTED_TRAFFIC:
        if pattern.endswith('*'):
            if request_substring.startswith(pattern[:-1]):
                return True
        else:
            if request_substring == pattern:
                return True
    return False

def read_and_filter_csv(start_time, end_time, csv_file='geolocated_accessLog.csv'):
    filtered_data = []
    
    with open(csv_file, encoding='ISO-8859-1') as csvfile: 
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers if there's any
        
        for row in reader:
            timestamp, _, request, _, lat, long = row  # adapt this based on the actual CSV structure
            
            # Check request against white list
            legitimate = isLegitimateTraffic(request)

            # Parse the timestamp and compare it within the range.
            entry_time = parse_datetime(timestamp)
            if start_time <= entry_time <= end_time:
                filtered_data.append({
                    "id": f"request{len(filtered_data) + 1}",
                    "coordinates": [float(lat), float(long)],
                    "type": "request",
                    "request": request,
                    "isLegitimate": legitimate
                })

    return filtered_data



@app.route('/trafficdata', methods=['GET'])
@cross_origin()  # This enables CORS on this route.
def traffic_data():
    start_time_str = request.args.get('start_time')  # Expecting time in the same format as your CSV entries.
    end_time_str = request.args.get('end_time')
    
    # Validate input times
    if not start_time_str or not end_time_str:
        return "Invalid input times", 400

    try:
        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)
    except ValueError as e:
        return f"Invalid time format: {e}", 400

    # Read and filter data from CSV
    nodes_data = read_and_filter_csv(start_time, end_time)

    # Construct the desired output format
    traffic_data = {
        "nodes": [
            { "id": "server", "coordinates": SERVER_COORDINATES, "type": "server" },
            *nodes_data
        ],
        "links": [
            { "source": node["id"], "target": "server" } for node in nodes_data
        ]
    }

    return jsonify(traffic_data)


if __name__ == '__main__':
    app.run(debug=True)
