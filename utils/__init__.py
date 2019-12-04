import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


# Adapted from https://www.themarketingtechnologist.co/getting-started-with-the-google-analytics-reporting-api-in-python/
def ga_response_dataframe(reports):
    row_list = []
    
    # Get each collected report
    for report in reports:
        # Set column headers
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get(
            'metricHeader', {}).get('metricHeaderEntries', [])
    
        # Get each row in the report
        for row in report.get('data', {}).get('rows', []):
            # create dict for each row
            row_dict = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            # Fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimension_headers, dimensions):
                row_dict[header] = dimension

            # Fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(date_range_values):
                for metric, value in zip(metric_headers, values.get('values')):
                # Set int as int, float a float
                    if ',' in value or '.' in value:
                        row_dict[metric.get('name')] = float(value)
                    else:
                        row_dict[metric.get('name')] = int(value)

            row_list.append(row_dict)
    
    return pd.DataFrame(row_list)
    

def ga_dataframe(key_file_location, scopes, body):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    reports = []
    
    while True:
        response = analytics.reports().batchGet(body=body).execute()
        report = response['reports'][0]
        reports.append(report)
        if report.get('nextPageToken'):
            body['reportRequests'][0]['pageToken'] = report['nextPageToken']
        else:
            break
    
    return ga_response_dataframe(reports)
