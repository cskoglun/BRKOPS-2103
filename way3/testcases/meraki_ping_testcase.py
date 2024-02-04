'''
A simple Ping testcase using Meraki and pyATS.

-------------------------------------------------------------------------
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

import time
from pyats import aetest
import meraki


__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    ping_jobs = []

    @aetest.subsection
    def creating_ping_jobs(self, steps, serials:list, destinations:list, api_key:str):
        '''
        Creating and running the Meraki ping jobs
        '''
        dashboard = meraki.DashboardAPI(api_key, output_log=False)

        for serial in serials:
            with steps.start(
                f"Creating the ping jobs on {serial}", continue_=True
            ) as step:
                for destination in destinations:
                    with step.start(destination):
                        try:
                            ping_job = dashboard.devices.createDeviceLiveToolsPing(serial=serial, target=destination, count=3)
                        except Exception as err:
                            step.failed(f'Step failed, reason: {err}')
                        else:
                            self.ping_jobs.append(ping_job)
                            step.passed(f'Ping job created for {destination}')
 
    @aetest.subsection
    def mark_tests_for_looping(self):
        '''
        Run the PingTestCase with each of the created ping jobs.
        '''
        aetest.loop.mark(PingTestcase, ping_job=self.ping_jobs)


class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''

    @aetest.setup
    def retrieve_ping_metrics(self, steps, ping_job, api_key):
        '''
        Retrieve the Ping job metrics from Meraki.
        '''
        dashboard = meraki.DashboardAPI(api_key, output_log=False)

        with steps.start(
            f"Retrieving Ping metrics from {ping_job['request']['serial']} to {ping_job['request']['target']}"
        ) as step:
            for i in range (6):
                print(f"Trying to retrieve data ({i})...")
                results = dashboard.devices.getDeviceLiveToolsPing(ping_job['request']['serial'], ping_job['pingId'])
                if not results["status"] == "complete":
                    print("Results not available, waiting for 5s...", end="\n\n") # It takes a moment for the metrics to generate
                    time.sleep(5)
                else:
                    self.results = results["results"]
                    step.passed(f"Ping job results retrieved successfully.")
            step.failed("Couldn't retrieve Ping job data")

    @aetest.test
    def ping(self, steps, ping_job):
        '''
        Compare the retrieved ping job metrics to expected result.
        '''

        with steps.start(
            f"Checking Ping from {ping_job['request']['serial']} to {ping_job['request']['target']}", continue_=True
                ) as step:
                if self.results["loss"]["percentage"] == 100: # If package loss is 100 %, fail
                    result_description = "100 % packet loss"
                    step.failed(result_description)
                else:
                    result_description = f"Packet loss {self.results['loss']['percentage']} %"
                    step.passed(result_description)

if __name__ == "__main__":
    import os

    print(f"\n{'* '*11}*")
    print("* STARTING PING TEST  *")
    print(f"{'* '*11}*\n")

    # Define your Meraki API key
    API_KEY = os.getenv("MERAKI_API_KEY")

    # Define a list or tuple of devices to be targeted using
    # their serial number
    serials = (os.getenv("MERAKI_SWITCH_SERIAL"), os.getenv("MERAKI_AP_SERIAL"))

    # Define the IP addresses to test
    my_destinations= ("8.8.8.8", "208.67.222.222")

    # Call the test with the destination IP addresses, device serials, and Meraki API key
    ping_test = aetest.main(
                            destinations=my_destinations,
                            serials=serials,
                            api_key=API_KEY
                        )
