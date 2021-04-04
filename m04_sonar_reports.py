import requests
from pprint import pprint
import json
import time
import pandas as pd
import os
import numpy as np
import datetime
import argparse

from m01_init_build import DEFAULT_GROUPS_FILE

METRICS = ['complexity', 'cognitive_complexity', 'duplicated_blocks',
              'duplicated_files', 'duplicated_lines', 'duplicated_lines_density',
              'new_violations', 'violations',
              'false_positive_issues', 'open_issues', 'confirmed_issues', 
              'reopened_issues', 'code_smells', 'new_code_smells', 'sqale_rating',
              'sqale_index', 'new_technical_debt', 'sqale_debt_ratio', 
              'new_sqale_debt_ratio', 'alert_status', 'quality_gate_details',
              'bugs', 'new_bugs', 'reliability_rating', 'reliability_remediation_effort',
              'new_reliability_remediation_effort', 'vulnerabilities', 'new_vulnerabilities',
              'security_rating', 'security_remediation_effort', 'classes', 'comment_lines',
              'comment_lines_density', 'directories', 'files', 'lines', 'ncloc', 
              'ncloc_language_distribution', 'functions', 'projects', 'statements',
              'branch_coverage', 'new_branch_coverage',
              'coverage',
              'new_coverage', 'line_coverage', 'new_line_coverage', 
              'lines_to_cover', 'new_lines_to_cover', 'skipped_tests', 'uncovered_conditions',
              'new_uncovered_conditions', 'uncovered_lines', 'tests', 'test_execution_time', 
              'test_errors', 'test_failures', 'test_success_density']


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download and test repositories of ing-sw")

    parser.add_argument("-d", "--debug", action='store_true',
                        help="If present, print debug messages")
    parser.add_argument("-i", "--groups_file", default=DEFAULT_GROUPS_FILE,
                        help="Path to the CSV containing the groups")
    args = parser.parse_args()
    debug = args.debug
    groups_file = args.groups_file

    df = pd.read_csv(groups_file, header=None).dropna()
    ids = []
    for index, row in df.iterrows():
        group_id = 'group-%02d' % int(row[0])
        ids.append(group_id)

    sonar_url = 'http://localhost:9000/api/measures/search?projectKeys=' + '%2C'.join(ids) + '&metricKeys=' + '%2C'.join(METRICS)
    resp = requests.get(sonar_url)
    data = resp.json()

    os.makedirs('reports', exist_ok=True)

    date = datetime.datetime.today()
    date_str = date.strftime("%Y-%m-%d_%H-%M-%S")

    metrics = []
    components = []
    for record in data['measures']:

        if record['metric'] not in metrics:
            metrics.append(record['metric'])

        if record['component'] not in components:
            components.append(record['component'])

    columns = ['group-id', 'date'] + metrics

    df = pd.DataFrame(columns=columns)

    for i, group_id in enumerate(components):
        new_row = [group_id, date]
        for m in metrics:
            found = False
            for record in data['measures']:
                if not found and record['component'] == group_id and record['metric'] == m:
                    if "value" in record:
                        try:
                            v = float(record['value'])
                        except ValueError:
                            v = record["value"]
                    else:
                        v = np.nan
                    new_row.append(v)
                    found = True
            if not found:
                new_row.append(np.nan)

        df.loc[i] = new_row
        
        
    # Fix types;
    df = df.infer_objects()

    # Fix line coverage;
    df.loc[df["line_coverage"] == 0, "line_coverage"] = 1 - df["lines_to_cover"] / df["ncloc"]

    print(df)

    print("groups with <= 40 tests")
    print(df[df["tests"] <= 40][["group-id", "ncloc", "tests"]])

    df.to_csv('reports/sonar_report_' + date_str + '.csv', index=False)
