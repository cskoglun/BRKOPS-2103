#!/usr/bin/env python
'''
Automate poe consumption data collection.

Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Christina Skoglund Poulsen"
__email__ = "cskoglun@cisco.com"

import os
import sys
import time
import logging
from typing import List, Dict
import pandas as pd
import schedule

from pprint import pprint

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(dir_path)

from backend import (build_meraki_dataset, 
                     initiate_meraki_session, 
                     initiate_cc_session,
                     build_cc_dataset)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def combined_dataset(session_m, session_c) -> List[Dict]:
    """
    Create a combined dataset of relevant CC, Meraki data and timestamp
    """
    logging.info("Building dataset in way1.py initiated")

    # Data to collect
    meraki_dataset = build_meraki_dataset(session_m)
    cc_dataset = build_cc_dataset(session_c)
    timestamp = time.time()

    logging.info("Timestamp of when the data was collected: %s", timestamp)

    for item in meraki_dataset:
        item["timestamp"] = timestamp
    for item in cc_dataset:
        item["timestamp"] = timestamp

    return [{"cc": cc_dataset, "meraki": meraki_dataset}]


def create_dataframe(data: List[Dict], columns: List[str]) -> pd.DataFrame:
    """
    Creates a DataFrame from the given data with specified columns.
    """
    df = pd.DataFrame(data, columns=columns)
    return df


def append_to_csv(df: pd.DataFrame, path: str) -> None:
    """
    Appends a DataFrame to a CSV file, adding headers if the file is new or empty.
    """
    header = not os.path.exists(path) or os.stat(path).st_size == 0
    df.to_csv(path, mode="a", header=header, index=False)


def update_and_save_dataset(session_m, session_c, path: str) -> None:
    """
    Collects the combined data and updates the csv file.
    """
    logging.info("Inside update-and-save-dataset")
    dataset_all = combined_dataset(session_m, session_c)


    columns = [
        "platform",
        "timestamp",
        "sw_name",
        "sw_identifier",
        "powerinw",
        "port",
        "ap_name",
        "ap_identifier",
    ]

    data_to_save = []
    for platform in dataset_all:
        for key, datasets in platform.items():
            platform_name = {"cc": "catalyst center", "meraki": "meraki"}.get(key)
            if platform_name:
                for dataset in datasets:

                    data_to_save.append(
                        [
                            platform_name,
                            dataset.get("timestamp"),
                            dataset.get("sw_name"),
                            dataset.get("sw_serial"),
                            dataset.get("power_in_w"),
                            dataset.get("port_id"),
                            dataset.get("ap_name"),
                            dataset.get("ap_serial"),
                        ]
                    )
    if data_to_save:
        df = create_dataframe(data_to_save, columns)
        append_to_csv(df, path)
        logging.info("Database updated")
    else:
        print("Error. No data to update.")


def main(path: str) -> None:
    """
    Main function handling time scheduling
    """
    meraki_dashboard_session = initiate_meraki_session()
    catalystcenter_session = initiate_cc_session()
    update_and_save_dataset(meraki_dashboard_session, catalystcenter_session, path)

    schedule.every(1).minute.do(update_and_save_dataset,meraki_dashboard_session, catalystcenter_session,path)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # State to which file to save the data
    FILE_PATH = "way1/poe_database_timeseries.csv"
    main(FILE_PATH)
