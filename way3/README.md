# Way 3 - Automate verification

The more you automate, the faster you are in breaking the network. That is why automating testing is really valuable. You can automate testing using for example pyATS framework together with Cisco APIs.

Testing can also be the very first thing you automate. The great thing about testing is that you can define many testcases that won't touch the network configuration - this means that automating testing is a safe way to introduce automation into your environment, while bringing value already from the first testcase.

## Testcases

There are 5 testcases in the `testcases` folder.

**Configuration validation**
- `catalyst_center_config_testcase.py`
- `meraki_config_testcase.py`

**Functional validation**
- `meraki_ping_testcase.py`
- `pyats_ping_testcase.py`

**SLA validation**
- `thousandeyes_testcase.py`

These can be run individually, or as a group by using the `job.py` file.

## Setup

1. Complete the `pip install -r requirements.txt` at the root of this repository
1. create a file `env` from the `env.template`
    ```bash
    cp env.template env
    ```
1. Fill in your preferred data to the `env`. If you are just planning to run certain tests, only those details need to be included

    ```
    TE_API_KEY=<thousandeyes_token>
    TE_AGENT=4

    DEVICE_IP=<ip> # your IOS XE IP
    DEVICE_PASSWORD=<password> # your IOS XE password
    DEVICE_USERNAME=<username> # your IOS XE username
    DEVICE_HOSTNAME=<hostname> # your IOS XE hostname
    DEVICE_ID=<device uuid from Cat Center> # YOUR IOS XE UUID in Catalyst Center

    MERAKI_API_KEY=<meraki key> # Your Meraki API key
    MERAKI_SWITCH_SERIAL=<switch> # Your Meraki switch serial
    MERAKI_AP_SERIAL=<ap> # Your Meraki AP serial

    CC_USERNAME=<username> # Your Catalyst Center username
    CC_PASSWORD=<password> # Your Catalyst Center password
    CC_URL=<url> # your Catalyst Center URL
    ```

    > **Note**: ThousandEyes agent 4 is a cloud agent that should work as it is. Change the ID to your own agent if preferred.

    For example (this is dummy data to give an example of the syntax):

    ```
    TE_API_KEY=abcd-1234-qwerty-9876-1357asdf
    TE_AGENT=4

    DEVICE_IP=10.10.10.5
    DEVICE_PASSWORD=my_secure_password
    DEVICE_USERNAME=admin
    DEVICE_HOSTNAME=switch
    DEVICE_ID=6abbf622-b243-45c8-b831-fe1d8ed7e5f0

    MERAKI_API_KEY=lhkdLHIFGIWAY872937173TGHJS
    MERAKI_SWITCH_SERIAL=Q0PP-5ACC-13W5
    MERAKI_AP_SERIAL=6BBA-9SZY-VS0R

    CC_USERNAME=admin
    CC_PASSWORD=my_secure_password
    CC_URL=catcenter.ciscolab.dk
    ```
3. Export the Environment variables
    ```bash
    export $(cat env)  
    ```

## Running single tests

To run a specific test from the `testcases` folder, you can simple use `python testcases/<testname>`.
Review the file of the testcase before running it - details that you might want to adjust are defined under the `if __name__ == "__main__"` conditional.

For example in the Meraki configuration test, you might want to redefine the interfaces whose status you are querying:
```python
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
```

After defining, you can run the test:
```
$ python testcases/meraki_config_testcase.py


* * * * * * * * * * * *
* STARTING PING TEST  *
* * * * * * * * * * * *

2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: |                            Starting common setup                             |
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: |                  Starting subsection mark_tests_for_looping                  |
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: The result of subsection mark_tests_for_looping is => PASSED
2024-02-02T00:44:57: %AETEST-INFO: The result of common setup is => PASSED
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: |       Starting testcase InterfaceConfigTestcase[device=Q2HP-3HCC-H335]       |
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %AETEST-INFO: |                Starting section get_device_interface_details                 |
2024-02-02T00:44:57: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:57: %MERAKI-INFO: Meraki dashboard API session initialized with these parameters: {'version': '1.40.1', 'api_key': '************************************07b6', 'base_url': 'https://api.meraki.com/api/v1', 'single_request_timeout': 60, 'certificate_path': '', 'requests_proxy': '', 'wait_on_rate_limit': True, 'nginx_429_retry_wait_time': 60, 'action_batch_retry_wait_time': 60, 'network_delete_retry_wait_time': 240, 'retry_4xx_error': False, 'retry_4xx_error_wait_time': 60, 'maximum_retries': 2, 'simulate': False, 'be_geo_id': None, 'caller': None, 'use_iterator_for_get_pages': False}
2024-02-02T00:44:57: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:57: %AETEST-INFO: :      Starting STEP 1:  Retrieving interface details for: Q2HP-3HCC-H335      :
2024-02-02T00:44:57: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:57: %MERAKI-DEBUG: {'tags': ['switch', 'configure', 'ports'], 'operation': 'getDeviceSwitchPorts', 'method': 'GET', 'url': '/devices/Q2HP-3HCC-H335/switch/ports', 'params': None}
2024-02-02T00:44:57: %MERAKI-INFO: GET https://api.meraki.com/api/v1/devices/Q2HP-3HCC-H335/switch/ports
2024-02-02T00:44:58: %MERAKI-INFO: switch, getDeviceSwitchPorts - 200 OK
2024-02-02T00:44:58: %AETEST-INFO: The result of STEP 1:  Retrieving interface details for: Q2HP-3HCC-H335 is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +..........................................................+
2024-02-02T00:44:58: %AETEST-INFO: :                       STEPS Report                       :
2024-02-02T00:44:58: %AETEST-INFO: +..........................................................+
2024-02-02T00:44:58: %AETEST-INFO: STEP 1 -  Retrieving interface details for: Q2HP-3HCC-H335Passed    
2024-02-02T00:44:58: %AETEST-INFO: ............................................................
2024-02-02T00:44:58: %AETEST-INFO: The result of section get_device_interface_details is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: |                    Starting section test_interface_status                    |
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:58: %AETEST-INFO: :           Starting STEP 1: Q2HP-3HCC-H335: Interface 1 (WIRELESS)            :
2024-02-02T00:44:58: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:58: %AETEST-INFO: Passed reason: Q2HP-3HCC-H335 WIRELESS is ✅ UP ✅
2024-02-02T00:44:58: %AETEST-INFO: The result of STEP 1: Q2HP-3HCC-H335: Interface 1 (WIRELESS) is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:58: %AETEST-INFO: :            Starting STEP 2: Q2HP-3HCC-H335: Interface 8 (UPLINK)             :
2024-02-02T00:44:58: %AETEST-INFO: +..............................................................................+
2024-02-02T00:44:58: %AETEST-INFO: Passed reason: Q2HP-3HCC-H335 UPLINK is ✅ UP ✅
2024-02-02T00:44:58: %AETEST-INFO: The result of STEP 2: Q2HP-3HCC-H335: Interface 8 (UPLINK) is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +..........................................................+
2024-02-02T00:44:58: %AETEST-INFO: :                       STEPS Report                       :
2024-02-02T00:44:58: %AETEST-INFO: +..........................................................+
2024-02-02T00:44:58: %AETEST-INFO: STEP 1 - Q2HP-3HCC-H335: Interface 1 (WIRELESS)   Passed    
2024-02-02T00:44:58: %AETEST-INFO: STEP 2 - Q2HP-3HCC-H335: Interface 8 (UPLINK)     Passed    
2024-02-02T00:44:58: %AETEST-INFO: ............................................................
2024-02-02T00:44:58: %AETEST-INFO: The result of section test_interface_status is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: |                           Starting section cleanup                           |
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: The result of section cleanup is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: The result of testcase InterfaceConfigTestcase[device=Q2HP-3HCC-H335] is => PASSED
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: |                               Detailed Results                               |
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2024-02-02T00:44:58: %AETEST-INFO: --------------------------------------------------------------------------------
2024-02-02T00:44:58: %AETEST-INFO: .
2024-02-02T00:44:58: %AETEST-INFO: |-- common_setup                                                          PASSED
2024-02-02T00:44:58: %AETEST-INFO: |   `-- mark_tests_for_looping                                            PASSED
2024-02-02T00:44:58: %AETEST-INFO: `-- InterfaceConfigTestcase[device=Q2HP-3HCC-H335]                        PASSED
2024-02-02T00:44:58: %AETEST-INFO:     |-- get_device_interface_details                                      PASSED
2024-02-02T00:44:58: %AETEST-INFO:     |   `-- Step 1:  Retrieving interface details for: Q2HP-3HCC-H335     PASSED
2024-02-02T00:44:58: %AETEST-INFO:     |-- test_interface_status                                             PASSED
2024-02-02T00:44:58: %AETEST-INFO:     |   |-- Step 1: Q2HP-3HCC-H335: Interface 1 (WIRELESS)                PASSED
2024-02-02T00:44:58: %AETEST-INFO:     |   `-- Step 2: Q2HP-3HCC-H335: Interface 8 (UPLINK)                  PASSED
2024-02-02T00:44:58: %AETEST-INFO:     `-- cleanup                                                           PASSED
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO: |                                   Summary                                    |
2024-02-02T00:44:58: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-02T00:44:58: %AETEST-INFO:  Number of ABORTED                                                            0 
2024-02-02T00:44:58: %AETEST-INFO:  Number of BLOCKED                                                            0 
2024-02-02T00:44:58: %AETEST-INFO:  Number of ERRORED                                                            0 
2024-02-02T00:44:58: %AETEST-INFO:  Number of FAILED                                                             0 
2024-02-02T00:44:58: %AETEST-INFO:  Number of PASSED                                                             2 
2024-02-02T00:44:58: %AETEST-INFO:  Number of PASSX                                                              0 
2024-02-02T00:44:58: %AETEST-INFO:  Number of SKIPPED                                                            0 
2024-02-02T00:44:58: %AETEST-INFO:  Total Number                                                                 2 
2024-02-02T00:44:58: %AETEST-INFO:  Success Rate                                                            100.0% 
2024-02-02T00:44:58: %AETEST-INFO: --------------------------------------------------------------------------------

```

## Running all tests from the `job.py` file

pyATS jobs can be used to run a test workflow. By opening the `job.py`, you will notice that there is plenty of variables defined in the beginning - we are collecting all the required details from the environment variables you defined in the setup section. We are also defining targeted interfaces (`IOS_XE_INTERFACES` and `MERAKI_INTERFACES`) and destinations (`IOS_XE_PING_DESTINATIONS`, `MERAKI_PING_DESTINATIONS` and `THOUSANDEYES_URLS `). Edit these as required to match to what you want to test.

Each of the tests are run with `pyats.easypy` method `run`, and relevant arguments are passed in to be used by the testcase.

Argument parses allows us to capture job name from the CLI command while running the job.

Run the job with the command:
```bash
$ pyats run job job.py --name MY_TEST
```

To see the results in browser after the job has run, use the following command:
```bash
pyats logs view
```

If you are running your job from a container, you can review the logs in browser by defining the port you have exposed from your container, and `--host 0.0.0.0`. This way you can access the results in `localhost:your_port`

For example:
```bash
pyats logs view --port 80 --host 0.0.0.0
```
