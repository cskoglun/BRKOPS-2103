#!/usr/bin/env python
'''
Job to run the tests.

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
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

import os
from pyats.easypy import run
from pyats.topology import loader

import argparse

from message import message # custom module for printing results

MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
MERAKI_SWITCHES = (os.getenv("MERAKI_SWITCH_SERIAL"),)
MERAKI_INTERFACES = "1,8" # CHANGE TO INTERFACES YOU WANT TO CHECK!

CATALYST_CENTER_CREDS = {
        "url": os.getenv("CC_URL"),
        "username": os.getenv("CC_USERNAME"),
        "password": os.getenv("CC_PASSWORD")
    }

IOS_XE_DEVICES = ({"name":os.getenv("DEVICE_HOSTNAME"), "uuid":os.getenv("DEVICE_ID")},)
IOS_XE_INTERFACES = "GigabitEthernet1/0/46,GigabitEthernet1/0/47,GigabitEthernet1/0/48" #CHANGE TO INTERFACES YOU WANT TO CHECK

THOUSANDEYES_API_KEY = os.getenv("TE_API_KEY")
THOUSANDEYES_AGENT = os.getenv("TE_AGENT")

IOS_XE_PING_DESTINATIONS = (
    '8.8.8.8',
    '208.67.222.222'
)

MERAKI_PING_DESTINATIONS = (
    '8.8.8.8',
    '208.67.222.222'
)

THOUSANDEYES_URLS = ("ciscolive.com",)


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help = "Job name")
args = parser.parse_args()

def full_path(testcase_name:str, testcase_folder:str="testcases")->str:
    ''' Simple function for defining the path for the testcases '''
    test_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_path, testcase_folder, testcase_name)

def main(runtime):

    # define the job name from CLI argument
    runtime.job.name = args.name

    print(f"\n{'* '*22}*\n* {'  '*21}*")
    print("* Welcome to the Test-Driven port automator *")
    print(f"* {'  '*21}*\n{'* '*22}*\n")

    # CONFIGURATION TESTS
    task_id = "Catalyst Center interface configuration"
    cat_config = run(
        testscript=full_path('catalyst_center_config_testcase.py'),
        taskid=task_id,
        interfaces=IOS_XE_INTERFACES,
        device_list=IOS_XE_DEVICES,
        cat_creds = CATALYST_CENTER_CREDS
    )

    print(message(task_id, cat_config))

    task_id = "Meraki interface configuration"
    meraki_config = run(
        testscript=full_path('meraki_config_testcase.py'),
        taskid=task_id,
        interfaces=MERAKI_INTERFACES,
        serials=MERAKI_SWITCHES,
        api_key=MERAKI_API_KEY
    )

    print(message(task_id, meraki_config))

    # FUNCTIONAL TESTS

    task_id = "pyATS ping"
    pyats_ping = run(
        testscript=full_path('pyats_ping_testcase.py'),
        taskid=task_id,
        destinations=IOS_XE_PING_DESTINATIONS,
        testbed=loader.load("testbed.yaml")
    )

    print(message(task_id, pyats_ping))

    task_id = "Meraki ping"
    meraki_ping = run(
        testscript=full_path('meraki_ping_testcase.py'),
        taskid=task_id,
        destinations=MERAKI_PING_DESTINATIONS,
        serials=MERAKI_SWITCHES,
        api_key=MERAKI_API_KEY
    )

    print(message(task_id, meraki_ping))

    # SLA TESTS

    task_id = "ThousandEyes total response time"
    thousandeyes = run(
        testscript=full_path('thousandeyes_testcase.py'),
        taskid=task_id,
        url_to_test_list=THOUSANDEYES_URLS,
        agent=THOUSANDEYES_AGENT,
        token=THOUSANDEYES_API_KEY
    )

    print(message(task_id, thousandeyes))
