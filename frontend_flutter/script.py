
import csv
from datetime import datetime

# Function to parse each line of input data
def parse_line(line):
    timestamp = line[1]  # Date in format 'dd.mm.yyyy'
    start_time = line[2]  # Start time in format 'hh:mm'
    end_time = line[3]    # End time in format 'hh:mm'
    
    # Convert to datetime objects for easier comparison
    start_datetime = datetime.strptime(f"{timestamp} {start_time}", "%d.%m.%Y %H:%M")
    end_datetime = datetime.strptime(f"{timestamp} {end_time}", "%d.%m.%Y %H:%M")
    
    return start_datetime, end_datetime

# Function to calculate the maximum number of ambulances active at the same time
def max_concurrent_ambulances(lines):
    # Parse the lines and store the start and end times
    events = []
    
    for line in lines:
        start, end = parse_line(line)
        events.append((start, 'start'))
        events.append((end, 'end'))
    
    # Sort events: first by time, then by event type ('end' before 'start' to handle simultaneous events)
    events.sort(key=lambda x: (x[0], x[1] == 'start'))
    
    # Track the number of ambulances that are active
    max_active = 0
    current_active = 0
    
    for event in events:
        if event[1] == 'start':
            current_active += 1
            max_active = max(max_active, current_active)
        else:
            current_active -= 1
    
    return max_active

# Read data from CSV file
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        return [row for row in reader if row[1] == '23.03.2023']  # Filter only the rows with the desired date

# Path to the CSV file
csv_file_path = '../transporte.csv'

# Read the CSV file and filter for the 23.03.2023 date
data = read_csv(csv_file_path)

# Call the function to get the maximum concurrent ambulances
max_active_ambulances = max_concurrent_ambulances(data)

# Output the result
print(f"The maximum number of ambulances active at the same time on 23.03.2023 was: {max_active_ambulances}")
