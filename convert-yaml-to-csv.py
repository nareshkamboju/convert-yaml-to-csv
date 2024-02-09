import csv
import yaml
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python main.py filename")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as file:
    yaml_data = file.read()

data = yaml.safe_load(yaml_data)

jobs = data['jobs']
test_names = set()
job_names = []

for job in data["jobs"]:
    job_names.append(job['name'])

for job in data.get("jobs", []):
    tests = job.get("tests", [])
    for test in tests:
        test_name = test.get("tests", [])
        test_names.update(test_name)

result = {test_name: {job_name: [] for job_name in job_names} for test_name in test_names}
for job in jobs:
    job_name = job['name']
    for test_name in test_names:
        tests = job.get("tests", [])
        for test in tests:
            if "tests" in test and test_name in test["tests"]:
                result[test_name][job_name].extend(test["device"])

with open(f'{os.path.splitext(filename)[0]}.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(['Test'] + job_names)

    for test_name, devices_by_job in result.items():
        row = [test_name]
        for job_name, devices in devices_by_job.items():
            row.append(''.join(devices))
        writer.writerow(row)

print(result)

import pandas as pd
df = pd.read_csv(f'{os.path.splitext(filename)[0]}.csv')
df.to_excel(f'{os.path.splitext(filename)[0]}.xlsx', index=None, header=True)

