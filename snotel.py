import requests
import pandas as pd

base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data"
params = {
    "stationTriplets": "*:AK:SNTL",
    "elements": "SNWD",
    "duration": "DAILY",
    "beginDate": "2012-08-01",
    "endDate": "2013-07-31",
    "periodRef": "END",
    "centralTendencyType": "NONE",
    "returnFlags": "false",
    "returnOriginalValues": "false",
    "returnSuspectData": "false",
}

full_url = requests.Request("GET", base_url, params=params).prepare().url
print("Requesting URL:")
print(full_url)

response = requests.get(full_url)
if response.status_code == 200:
    raw_data = response.json()

    records = []
    for station in raw_data:
        station_id = station["stationTriplet"]
        for entry in station["data"]:
            element_code = entry["stationElement"]["elementCode"]
            for value in entry["values"]:
                records.append(
                    {
                        "stationTriplet": station_id,
                        "elementCode": element_code,
                        "date": value["date"],
                        "value": value["value"],
                    }
                )

    df = pd.DataFrame(records)
    print(df.head())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
