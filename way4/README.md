# Way 4: Get started today!

To efficiently and practically learn automation, the best way in our opinion is to create an MVP. MVP is a minimum viable product solving a use case. The goal is to make a plan, and learn the needed automation functionalities as you proceed with creating the features. To start getting value immediately from your automation, divide your use case to small enough chunks in order to create fast functional code.

Get started by solving your use case:
1. Define your use case
2. List needed features
3. Find code from others
4. Complete one feature.
5. Celebrate and repeat.

## Flow to create a MVP feature by feature: List out my access devices

In this folder you can see an example of a script that prints out the switches from a Meraki and Catalyst Center environments.

> **Note:** The script has been tested in February 2024 with DevNet always on sandboxes, and the needed Catalyst Center credentials and Meraki API_token are hardcoded in the script. You may directly run the script, but you may also replace the credentials and API token with your own. Note that it is not best practice to hard code your credentials, and **be really careful to never push the credentials to Github or other external repository**.

The features of this use case:
1. Define your use case -> **Print a report of the network's switches**
2. List needed features
    1. Retrieve Meraki devices
    2. Retrieve Catalyst devices
    3. Print out a summary
3. Find code from others
    1. Meraki API: [Get Organization SDK code snippets in documentation](https://developer.cisco.com/meraki/api-v1/get-organization-devices/)
    2. Catalyst Center API: [Quick start for the SDK](https://dnacentersdk.readthedocs.io/en/latest/api/quickstart.html), [Blog on how to use the SDK](https://blogs.cisco.com/developer/using-cisco-dna-center-sdk)
    3. Nice library to print out a pretty report: [`PrettyTable` documentation](https://pypi.org/project/prettytable/)
4. Complete one feature. -> Retrieve Meraki devices (`meraki_feature_example.py``)
5. Celebrate and repeat.

### Feature 1: Retrieve Meraki devices

Run `meraki_feature_example` to retrieve all the Meraki device data.

```bash
$ python meraki_feature_example.py

2024-01-30 10:21:03       meraki:     INFO > Meraki dashboard API session initialized with these parameters: {'version': '1.40.1', 'api_key': '************************************9ea0', 'base_url': 'https://api.meraki.com/api/v1', 'single_request_timeout': 60, 'certificate_path': '', 'requests_proxy': '', 'wait_on_rate_limit': True, 'nginx_429_retry_wait_time': 60, 'action_batch_retry_wait_time': 60, 'network_delete_retry_wait_time': 240, 'retry_4xx_error': False, 'retry_4xx_error_wait_time': 60, 'maximum_retries': 2, 'simulate': False, 'be_geo_id': None, 'caller': None, 'use_iterator_for_get_pages': False}
2024-01-30 10:21:03       meraki:     INFO > GET https://api.meraki.com/api/v1/organizations/681155/devices
2024-01-30 10:21:04       meraki:     INFO > organizations, getOrganizationDevices; page 1 - 200 OK
[{'name': 'Sun Room', 'serial': 'Q2EK-UKGM-XSD9', 'mac': 'e0:55:3d:10:5e:b2', 'networkId': 'L_566327653141843049', 'productType': 'wireless', 'model': 'MR84', 'address': '3049 Warrington Road Shaker Heights OH 44120', 'lat': 41.47684, 'lng': -81.57801, 'notes': '', 'tags': ['recently-added'], 'lanIp': None, 'configurationUpdatedAt': '2023-07-17T18:20:22Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/Lyoli-wireless/n/WdPtFdg/manage/nodes/new_list/246656701324978', 'details': []}, {'name': '', 'serial': 'Q2GV-7HEL-HC6C', 'mac': '34:56:fe:a3:db:7b', 'networkId': 'L_566327653141856854', 'productType': 'camera', 'model': 'MV12W', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.1.241', 'configurationUpdatedAt': '2023-12-12T00:41:36Z', 'firmware': 'camera-4-18-1', 'url': 'https://n392.meraki.com/DNEAlertsNet-cam/n/uMosbcg/manage/nodes/new_list/57548243983227', 'details': []}, {'name': 'Office Switch', 'serial': 'Q2HP-C2YW-KB2E', 'mac': 'e0:55:3d:d2:6f:7a', 'networkId': 'L_566327653141843049', 'productType': 'switch', 'model': 'MS220-8P', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.1.227', 'configurationUpdatedAt': '2023-12-26T02:55:10Z', 'firmware': 'switch-15-21-1', 'url': 'https://n392.meraki.com/Lyoli-switch/n/kjwRabg/manage/nodes/new_list/246656714043258', 'details': []}, {'name': 'ms01-dl1', 'serial': 'Q2HP-EC87-M9B8', 'mac': 'e0:55:3d:d0:04:c5', 'networkId': 'L_783626335162466320', 'productType': 'switch', 'model': 'MS220-8P', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.128.2', 'configurationUpdatedAt': '2023-12-18T14:00:34Z', 'firmware': 'switch-15-21-1', 'url': 'https://n392.meraki.com/DevNetLab-switch/n/0Yt-Qbig/manage/nodes/new_list/246656713884869', 'details': []}, {'name': 'ms01-dl3', 'serial': 'Q2HP-W3HC-2C8D', 'mac': 'e0:55:3d:d2:79:0f', 'networkId': 'L_783626335162466515', 'productType': 'switch', 'model': 'MS220-8P', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.128.6', 'configurationUpdatedAt': '2023-11-16T18:50:26Z', 'firmware': 'switch-15-21-1', 'url': 'https://n392.meraki.com/DevNetLab3-switc/n/XOn1mcig/manage/nodes/new_list/246656714045711', 'details': []}, {'name': 'Basement Switch', 'serial': 'Q2HP-Y9R9-FK5Y', 'mac': 'e0:55:3d:d0:d3:5d', 'networkId': 'L_566327653141843049', 'productType': 'switch', 'model': 'MS220-8P', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': [], 'lanIp': '192.168.1.249', 'configurationUpdatedAt': '2023-12-23T10:08:34Z', 'firmware': 'switch-15-21-1', 'url': 'https://n392.meraki.com/Lyoli-switch/n/kjwRabg/manage/nodes/new_list/246656713937757', 'details': []}, {'name': 'ap01-dl2', 'serial': 'Q2KD-KWMU-7U92', 'mac': 'e0:cb:bc:8c:1f:fe', 'networkId': 'L_783626335162466514', 'productType': 'wireless', 'model': 'MR42', 'address': '', 'lat': 41.30627, 'lng': -81.61507, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.128.3', 'configurationUpdatedAt': '2024-01-11T09:50:57Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/DevNetLab2-wirel/n/3dpsodig/manage/nodes/new_list/247165646282750', 'details': []}, {'name': 'Basement AP', 'serial': 'Q2LD-3Y7V-7Y2X', 'mac': 'e0:55:3d:c0:73:56', 'networkId': 'L_566327653141843049', 'productType': 'wireless', 'model': 'MR52', 'address': '3049 Warrington Road Shaker Heights OH 44120', 'lat': 41.47684, 'lng': -81.57801, 'notes': '', 'tags': [], 'lanIp': '192.168.1.94', 'configurationUpdatedAt': '2024-01-02T00:54:17Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/Lyoli-wireless/n/WdPtFdg/manage/nodes/new_list/246656712864598', 'details': []}, {'name': 'ap01-dl3', 'serial': 'Q2LD-D932-NRPU', 'mac': '0c:8d:db:b2:2f:2c', 'networkId': 'L_783626335162466515', 'productType': 'wireless', 'model': 'MR52', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'lanIp': '192.168.1.142', 'configurationUpdatedAt': '2024-01-11T09:50:57Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/DevNetLab3-wirel/n/e5u4ibig/manage/nodes/new_list/13803415809836', 'details': []}, {'name': 'ap01-dl1', 'serial': 'Q2LD-FGN3-VP7S', 'mac': '0c:8d:db:b2:77:f8', 'networkId': 'L_783626335162466320', 'productType': 'wireless', 'model': 'MR52', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': [], 'lanIp': '192.168.128.7', 'configurationUpdatedAt': '2024-01-11T09:50:57Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/DevNetLab-wirele/n/61qIJbig/manage/nodes/new_list/13803415828472', 'details': []}, {'name': '1st Floor AP', 'serial': 'Q2LD-GYL3-KEHX', 'mac': 'e0:55:3d:c0:76:f4', 'networkId': 'L_566327653141843049', 'productType': 'wireless', 'model': 'MR52', 'address': '', 'lat': 41.476798707110106, 'lng': -81.5780361515379, 'notes': '', 'tags': ['LTV'], 'lanIp': None, 'configurationUpdatedAt': '2024-01-15T22:12:46Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/Lyoli-wireless/n/WdPtFdg/manage/nodes/new_list/246656712865524', 'details': []}, {'name': '', 'serial': 'Q2LD-N2U5-D83H', 'mac': '0c:8d:db:b2:8a:5a', 'networkId': 'N_566327653141899127', 'productType': 'wireless', 'model': 'MR52', 'address': '', 'lat': 41.130929746675434, 'lng': -81.86433465058565, 'notes': '', 'tags': [], 'lanIp': '24.144.215.84', 'configurationUpdatedAt': '2018-10-25T14:41:08Z', 'firmware': 'Not running configured version', 'url': 'https://n392.meraki.com/Nolan/n/9qi_yag/manage/nodes/new_list/13803415833178', 'details': []}, {'name': '', 'serial': 'Q2LD-X2S2-AG2U', 'mac': '0c:8d:db:b2:8c:f0', 'networkId': 'N_566327653141899127', 'productType': 'wireless', 'model': 'MR52', 'address': '', 'lat': 41.130968131649794, 'lng': -81.86433330948114, 'notes': '', 'tags': [], 'lanIp': None, 'configurationUpdatedAt': '2018-10-10T01:09:22Z', 'firmware': 'Not running configured version', 'url': 'https://n392.meraki.com/Nolan/n/9qi_yag/manage/nodes/new_list/13803415833840', 'details': []}, {'name': 'Office AP', 'serial': 'Q2LD-ZWCZ-UA77', 'mac': 'e0:55:3d:c0:72:d8', 'networkId': 'L_566327653141843049', 'productType': 'wireless', 'model': 'MR52', 'address': '3049 Warrington Road Shaker Heights OH 44120', 'lat': 41.47684, 'lng': -81.57801, 'notes': '', 'tags': [], 'lanIp': '192.168.1.177', 'configurationUpdatedAt': '2024-01-08T16:47:34Z', 'firmware': 'wireless-29-5-1', 'url': 'https://n392.meraki.com/Lyoli-wireless/n/WdPtFdg/manage/nodes/new_list/246656712864472', 'details': []}, {'name': 'MX65', 'serial': 'Q2QN-FD4H-JKYA', 'mac': 'e0:55:3d:73:05:4d', 'networkId': 'L_783626335162466515', 'productType': 'appliance', 'model': 'MX65', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'wan1Ip': '192.168.128.101', 'wan2Ip': None, 'configurationUpdatedAt': '2024-01-01T22:11:36Z', 'firmware': 'wired-18-1-07', 'url': 'https://n392.meraki.com/DevNetLab3-appli/n/uhtVwcig/manage/nodes/new_list/246656707790157', 'details': []}, {'name': 'mx01-dl1', 'serial': 'Q2QN-Q6EY-NP7J', 'mac': '0c:8d:db:b0:c2:dc', 'networkId': 'L_783626335162466320', 'productType': 'appliance', 'model': 'MX65', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': [], 'wan1Ip': '192.168.128.102', 'wan2Ip': None, 'configurationUpdatedAt': '2023-11-21T03:03:20Z', 'firmware': 'wired-18-1-07', 'url': 'https://n392.meraki.com/DevNetLab-applia/n/xaNlkcig/manage/nodes/new_list/13803415716572', 'details': []}, {'name': 'mx01-dl2', 'serial': 'Q2QN-UTMQ-ZJQA', 'mac': '0c:8d:db:b0:c3:44', 'networkId': 'L_783626335162466514', 'productType': 'appliance', 'model': 'MX65', 'address': '', 'lat': 37.4180951010362, 'lng': -122.098531723022, 'notes': '', 'tags': ['recently-added'], 'wan1Ip': '192.168.1.220', 'wan2Ip': None, 'configurationUpdatedAt': '2023-11-19T21:39:10Z', 'firmware': 'wired-18-1-07', 'url': 'https://n392.meraki.com/DevNetLab2-appli/n/lelHCbig/manage/nodes/new_list/13803415716676', 'details': []}]
```

Pay attention to the following:
1. Meraki SDK prints logs and creates log files when the script is ran. This is not always optimal, especially when creating a terminal based application, in which the logs may make it hard for the user to use the app.
  You can define whether you want log files to be generated (`output_log`) and/or logs printed (`print_console`) when initializing your Meraki SDK:

  ```python
  dashboard = meraki.DashboardAPI(api_key,
                                    output_log=False,
                                    print_console=False)
  ```

2. When using `.organizations.getOrganizationDevices`, a list is returned: each device is a dictionary in the list with details such as `name`, `productType` and `model`, to mention a few. For your report, the next step could be to choose which of the returned information you want to include in your report.

### Feature 2: Retrieve Catalyst devices

To add next feature, complete similar script for Catalyst Center to print out the returned response. How is that different from Meraki response? How is it similar to the Meraki response?

### Feature 3: Print out a summary

To print the Catalyst and Meraki devices nicely, choose what kind of output you would like to get. You could start just by using simple `print()` statements until you are happy with the data you have selected. However, with the Python libraries, it is relatively easy to move fast to more fancy looking printing. A fun library for printing out a report would be to use `PrettyTable`. In the library's [documentation](https://pypi.org/project/prettytable/) you can see ready examples on how to install and use the the library.

## Example of "ready" prototype for printing the devices

For the final report, we chose to include only switches, and to include data on the switch's "Name", "Platform", "Management IP", and "SW/FW version".

```bash
$ python print_report.py 

*** MY REPORT: Catalyst Center managed switches ***

+------+--------------+---------------+----------------------+
| Name |   Platform   | Management IP |    SW/FW version     |
+------+--------------+---------------+----------------------+
| sw1  | C9KV-UADP-8P |  10.10.20.175 | 17.9.20220318:182713 |
| sw2  | C9KV-UADP-8P |  10.10.20.176 | 17.9.20220318:182713 |
| sw3  | C9KV-UADP-8P |  10.10.20.177 | 17.9.20220318:182713 |
| sw4  | C9KV-UADP-8P |  10.10.20.178 | 17.9.20220318:182713 |
+------+--------------+---------------+----------------------+

*** MY REPORT: Meraki managed switches ***

+-----------------+----------+---------------+----------------+
|       Name      | Platform | Management IP | SW/FW version  |
+-----------------+----------+---------------+----------------+
|  Office Switch  | MS220-8P | 192.168.1.227 | switch-15-21-1 |
|     ms01-dl1    | MS220-8P | 192.168.128.2 | switch-15-21-1 |
|     ms01-dl3    | MS220-8P | 192.168.128.6 | switch-15-21-1 |
| Basement Switch | MS220-8P | 192.168.1.249 | switch-15-21-1 |
+-----------------+----------+---------------+----------------+
```