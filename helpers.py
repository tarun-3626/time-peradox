import csv

def read_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)
    return headers, data

def validate_csv(headers, expected_headers):
    return all(h in headers for h in expected_headers)
