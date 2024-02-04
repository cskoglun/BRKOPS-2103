#!/usr/bin/env python
'''
Powersaver script that turns access ports on and off in your
Catalyst and Meraki network.

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
from os.path import exists

import requests
from dotenv import load_dotenv
import pandas as pd
from colorama import Fore, Style 

from dnacentersdk.exceptions import ApiError

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(dir_path)

from backend import (
    initiate_cc_session,
    initiate_meraki_session,
    build_meraki_dataset,
    build_cc_dataset,
)

load_dotenv()

def cc_port_dataset(session_c) -> list:
    """
    Builds a Catalyst Center port dataset.
    """
    cc_data = build_cc_dataset(session_c)
    cc_data = [
        {key: item[key] for key in item if key not in ["power_in_w", "timestamp"]}
        for item in cc_data
    ]
    return cc_data

def create_and_update_port_database(session_m, session_c, file_path):
    """
    Creates and updates a port database for Way2.
    """
    meraki_ports = build_meraki_dataset(session_m)
    cc_ports = cc_port_dataset(session_c)

    ports_dataset = {"cc": cc_ports, "meraki": meraki_ports}

    columns = [
        "platform",
        "sw_name",
        "sw_identifier",
        "port",
        "port_name",
        "ap_name",
        "ap_identifier",
    ]

    rows = []
    for key, value in ports_dataset.items():
        for item in value:
            row = {
                "platform": key,
                "sw_name": item["sw_name"],
                "sw_identifier": item["sw_serial"],
                "port": item["port_id"],
                "port_name": item["port_name"],
                "ap_name": item["ap_name"],
                "ap_identifier": item["ap_serial"],
            }
            rows.append(row)

    combined_df = pd.DataFrame(rows, columns=columns)

    # Determine if headers should be written
    write_header = not exists(file_path)

    # Write the combined DataFrame to CSV in one operation
    combined_df.to_csv(file_path, mode="a", header=write_header, index=False)

    return combined_df

def find_interface_name(file_path: str, port_id: str) -> str:
    """
    Finds interface name from port_database.csv that matches the interface id.
    """
    df = pd.read_csv(file_path)
    filtered_df = df[df["port"] == port_id]

    # Check if there's at least one match
    if not filtered_df.empty:
        # Assuming the first match is the desired one (in case of multiple matches)
        return filtered_df.iloc[0]["port_name"]
    else:
        return ""  # Return an empty string if no match is found

def find_serial(file_path: str, port_id: str):
    """
    Finds interface name from port_database.csv that matches the interface id.
    """
    df = pd.read_csv(file_path)
    filtered_df = df[df["port"] == port_id]

    # Check if there's at least one match
    if not filtered_df.empty:
        # Assuming the first match is the desired one (in case of multiple matches)
        return filtered_df.iloc[0]["sw_identifier"]
    else:
        return ""  # Return an empty string if no match is found

def update_interface_status(
    session_m, session_c, action_arg, platform, interface_uuid
) -> list:
    """
    Function updates switch interface Admin Status and changes its description
    """

    if action_arg.upper() in ["UP", "DOWN"]:
        if platform.lower() == "cc":
            interface_name = find_interface_name("port_database.csv", interface_uuid)
            new_status = action_arg.upper()
            payload = {
                "description": f"Interface status configured to 'Admin {new_status} through API'",
                "adminStatus": f"{new_status}",
            }
            try:
                session_c.devices.update_interface_details(
                    interface_uuid, payload=payload
                )
                print(
                    Fore.GREEN
                    + f"Catalyst - Port {interface_name} with id {interface_uuid} is updated to {new_status}"
                )

            except ApiError as e:
                print(
                    Fore.RED
                    + f"No action as the port {interface_name} is already {new_status}"
                )

        elif platform.lower() == "meraki":
            serial = find_serial("port_database.csv", interface_uuid)
            port_id = interface_uuid
            if action_arg.upper() == "UP":
                new_status = True
                new_status_output = "True"
            elif action_arg.upper() == "DOWN":
                new_status = False
                new_status_output = "False"
            else:
                print("ERROR")
            try:
                session_m.switch.updateDeviceSwitchPort(
                    serial,
                    port_id,
                    enabled=new_status,
                )
                print(
                    f"Meraki - Port 1 with id 1 has changed status to {new_status_output} MS device"
                )
                # TODO missing a function on how to detect if port is already up/down
                # Need to include functionality separately

            except (requests.exceptions.RequestException, ValueError) as e:
                print(str(e))
        else:
            pass
    else:
        print("Sorry did not understand that")

    return None

def main(args: list):
    """
    Main function to either create a database or update port status
    """
    meraki_dashboard_session = initiate_meraki_session()
    catalystcenter_session = initiate_cc_session()

    if len(args) == 2:
        if "create" in args[0].lower():
            db_name = args[1].lower()
            create_and_update_port_database(
                meraki_dashboard_session, catalystcenter_session, file_path=db_name
            )

    elif len(args) == 1:
        action = args[0].upper()
        if action in ("UP", "DOWN"):
            columns = [
                "platform",
                "sw_name",
                "sw_identifier",
                "port",
                "port_name",
                "ap_name",
                "ap_identifier",
            ]

            data = pd.read_csv("port_database.csv", names=columns, header=None)
            platform_list = data["platform"].values.tolist()
            port_list = data["port"].values.tolist()

            # create mapping dictionary
            index_to_platform = {}

            # Populate the dictionary during enumeration
            for index, item in enumerate(platform_list):
                if "cc" in item:
                    index_to_platform[index] = "cc"
                elif "meraki" in item:
                    index_to_platform[index] = "meraki"

            # Use the dictionary to update interface status
            for index, value in enumerate(port_list):
                platform_type = index_to_platform.get(index)
                if platform_type:
                    update_interface_status(
                        meraki_dashboard_session,
                        catalystcenter_session,
                        action,
                        platform_type,
                        value,
                    )
    else:
        print("only one argument!")
    return None

if __name__ == "__main__":

    arg = sys.argv[1:]

    if len(arg) >= 1:
        main(arg)

    else:
        print(
            "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
        )
        print(
            "*                                                                               *"
        )
        print(
            "*                          Welcome to the power saver script!                   *"
        )
        print(
            "*                                                                               *"
        )
        print(
            "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
        )
        _PORTSTATUS = str(
            input(
                "\nDo you want to shut down the access points and save some watts (y/n)[n]?:"
            )
            or "n"
        )
        if _PORTSTATUS.lower() in ("n", "no"):
            _TURNON = str(
                input("\nDo you want to turn on the access points (y/n)[n]?:") or "n"
            )

            if _TURNON.lower() in ("n", "no"):
                print(Fore.LIGHTYELLOW_EX + "No action will be taken")
            elif _TURNON.lower() in ("y", "yes"):
                _STATUS = "up"
                print(
                    Fore.LIGHTYELLOW_EX
                    + '\nYour action "turn APs on" is being posted to Cisco Catalyst Center and Meraki...\n '
                )
                arguments = [_STATUS]
                main(arguments)
            else:
                print("I did not understand that. No action taken.")

        elif _PORTSTATUS.lower() in ("y", "yes"):
            _CHECK = str(
                input(
                    "\n...double checking: You REALLY want to shut down the access points?(y/n)[n]"
                )
                or "n"
            )
            if _CHECK.lower() in ("y", "yes"):
                _STATUS = "down"
                print(
                    Fore.LIGHTYELLOW_EX
                    + '\nYour action "shut APs down" is being pushed to Cisco Catalyst Center and Meraki... '
                )
                print(Style.RESET_ALL)
                arguments = [_STATUS]
                main(arguments)
            elif _CHECK.lower() in ("n", "no"):
                print(Fore.LIGHTYELLOW_EX + "\nAborted!\n")
            else:
                print(
                    "\nI did not understand that. Please try to run the script again\n"
                )
