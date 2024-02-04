#!/usr/bin/env python
'''
Configuration validation ("Is it there?") to test port status by
executing a simple Meraki API test.

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

from pyats import aetest
import meraki

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    @aetest.subsection
    def mark_tests_for_looping(self, serials:list):
        """
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the from the list of Meraki serials.
        """
        aetest.loop.mark(InterfaceConfigTestcase, device=serials)

class InterfaceConfigTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking port status using Cisco Meraki.
    '''

    @aetest.setup
    def get_device_interface_details(self, steps, device, interfaces, api_key):
        ''' Retrieving interface status from Meraki for the selected device '''
    
        dashboard = meraki.DashboardAPI(api_key, output_log=False)

        with  steps.start(
            f" Retrieving interface details for: {device}",
            continue_=True
        ) as step:
            try:
                switch_interfaces = dashboard.switch.getDeviceSwitchPorts(serial=device)
                self.interfaces = [
                    {
                        "id":interface["portId"],
                        "name":interface["name"],
                        "enabled":interface["enabled"]
                    }
                    for interface in switch_interfaces
                    if interface["portId"] in interfaces
                ]

            except Exception as err:
                step.failed(err)

            else:
                step.passed()


    @aetest.test
    def test_interface_status(self, steps, device):
        '''
        Comparing retrieved interface configuration to the expected result
        '''

        for interface in self.interfaces:
            interface_name = interface["name"]
            interface_id = interface["id"]

            with steps.start(
                f"{device}: Interface {interface_id} ({interface_name})",
                continue_=True
            ) as step:

                if interface["enabled"]:
                    step.passed(f"{device} {interface_name} is ✅ UP ✅")
                    
                else:
                    step.failed(f"{device} {interface_name} is ❌ DOWN ❌")


    @aetest.cleanup
    def cleanup(self):
        ''' No cleanup needed for this Meraki testcase '''
        pass

if __name__ == "__main__":
    import os

    print(f"\n{'* '*11}*")
    print("* STARTING PING TEST  *")
    print(f"{'* '*11}*\n")

    # Define your Meraki API key
    API_KEY = os.getenv("MERAKI_API_KEY")

    # Define a list or tuple of devices to be targeted using
    # their serial number
    serials =(os.getenv("MERAKI_SWITCH_SERIAL"),)

    # define the interfaces to be targeted in one string, separated by commas
    interfaces="1,8"

    # Call the test with the defined serials, interfaces, and api_key
    aetest.main(serials=serials, interfaces=interfaces, api_key=API_KEY)
