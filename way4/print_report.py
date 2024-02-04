from prettytable import PrettyTable
import meraki
from dnacentersdk import api

def get_catalyst_center_switches(username:str, password:str, url:str)->list:
    """
    A function to retrieve Catalyst Center managed switches.

    Args:
        username (str) : Username used for authentication.
        password (str) : Password used for authentication
        url (str): The URL of your Catalyst center

    Returns:
        A list of dictionaries representing all the switches found in the network, in the correct
        format to be used with print_report function
    """

    session = api.DNACenterAPI(
                    base_url=url,
                    username=username,
                    password=password,
                    verify=False
                )

    response = session.devices.get_device_list(family='Switches and Hubs')

    devices = response["response"]
    switches = []

    for device in devices:
        switches.append({
            "hostname": device["hostname"],
            "platform": device["platformId"],
            "mgmt_ip": device["managementIpAddress"],
            "version": device["softwareVersion"]
        })

    return switches

def get_meraki_switches(api_key:str, organization_id:str)->list:
    """
    A function to retrieve Meraki managed switches.

    Args:
        api_key (str) : Meraki bearer token to authorize the API call
        organization_id (str): The ID of the Meraki organization whose switches are queried

    Returns:
        A list of dictionaries representing all the switches found in the organization, in the
        correct format to be used with print_report function
    """

    dashboard = meraki.DashboardAPI(api_key,
                                    output_log=False,
                                    print_console=False)

    devices = dashboard.organizations.getOrganizationDevices(organization_id, total_pages='all')
    switches = []
    for device in devices:
        if device["productType"] == "switch":
            switches.append({
                "hostname": device["name"],
                "platform": device["model"],
                "mgmt_ip": device["lanIp"],
                "version": device["firmware"]
            })
    return switches

def print_report(report_name: str, devices: list[dict])->None:
    """
    A function to print report on network's devices - name, platform
    management IP and SW or FW version.

    Args:
        report_name (str) : the title to be printed above the report.
        devices (list) : A list of dictionaries with keys: "hostname",
                        "platform", "mgmt_ip", "version"
    """

    table = PrettyTable()
    table.field_names = ["Name", "Platform", "Management IP", "SW/FW version"]
    for device in devices:
        table.add_row(
            [device["hostname"],
             device["platform"],
             device["mgmt_ip"],
             device["version"]]
        )

    print(f"\n*** MY REPORT: {report_name} ***\n")
    print(table)

if __name__ == "__main__":

    catalyst_report_name = "Catalyst Center managed switches"
    catalyst_url = "https://sandboxdnac.cisco.com"
    catalyst_username = "devnetuser"
    catalyst_password = "Cisco123!"
    catalyst_center_switches = get_catalyst_center_switches(catalyst_username, catalyst_password, catalyst_url)
    print_report(catalyst_report_name, catalyst_center_switches)

    meraki_report_name = "Meraki managed switches"
    meraki_token = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    meraki_org = "681155"
    meraki_switches = get_meraki_switches(meraki_token, meraki_org)
    print_report(meraki_report_name, meraki_switches)
