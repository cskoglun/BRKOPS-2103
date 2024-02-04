"""
This is the backend script where all API calls are defined and where the data mapping
takes place when using scripts way1.py and way2.py.
"""
import os
import logging
from dotenv import load_dotenv
import requests

from pprint import pprint

from dnacentersdk import DNACenterAPI
from meraki import DashboardAPI

load_dotenv()

CC_USERNAME = os.getenv("CC_USERNAME")
CC_PASSWORD = os.getenv("CC_PASSWORD")
CC_HOST = os.getenv("CC_HOST")
MERAKI_KEY = os.getenv("MERAKI_DASHBOARD_API_KEY")
ORG = "Meraki Nordics Lab" #Input your organization name
NETWORKS = ["Cisco Live Energy Mgmt Demo"] # Your network name

# Cisco CC backend
def initiate_cc_session() -> DNACenterAPI:
    """
    Returns an instance of the DNACenterAPI class from dnacentersdk
    """
    try:
        catalystcenter = DNACenterAPI(
            base_url=f"https://{CC_HOST}:443",
            username=CC_USERNAME,
            password=CC_PASSWORD,
            verify=False,
        )
        return catalystcenter
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to initiate DNACenterAPI session: %s", e)
        return None

def get_physical_topology_nodes_links(session_c: DNACenterAPI) -> list:
    """
    Retrieves the whole physical topology of Catalyst Center.
    Output is a list with all nodes and links data.
    """
    try:
        physical_topology_response = session_c.topology.get_physical_topology()
        physical_topology_data = physical_topology_response["response"]
        physical_topology_nodes = physical_topology_data["nodes"]
        physical_topology_links = physical_topology_data["links"]

        return physical_topology_nodes, physical_topology_links
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to get physical topology nodes from CC: %s", e)
        return None

def get_switch_info(nodes, switch_device_uuid):
    """
    Retrieve switch label for a given switch device UUID.
    """
    for item in nodes:
        if item["id"] == switch_device_uuid:
            return item["label"]
    return None

def process_link(link, nodes, ap_device_label, ap_device_uuid, ap_platform_id):
    """
    Process a single link and return device mapping if applicable.
    """
    interface_uuid = (link.get("endPortID")
                      if link["source"] == ap_device_uuid
                      else link.get("startPortID"))
    switch_device_uuid = (link["target"]
                          if link["source"] == ap_device_uuid
                          else link["source"])
    interface_name = (link.get("endPortName")
                      if link["source"] == ap_device_uuid
                      else link.get("startPortName"))
    switch_label = get_switch_info(nodes, switch_device_uuid)

    if switch_label:  # Ensure switch_label is not None
        return {
            "interface_label": ap_device_label,
            "ap_platform_id": ap_platform_id,
            "interfaceUuid": interface_uuid,
            "interface_name": interface_name,
            "switch_label": switch_label,
            "switch_deviceUuid": switch_device_uuid,
            "AP_Uuid": ap_device_uuid,
        }
    return None

def create_cc_data_mapping(session_c: DNACenterAPI) -> list:
    """
    This function returns a list of dictionaries with interfaceUuid, AP_Uuid and SW_Uuid data.
    The data is retrieved by the Topology API of Cisco Catalyt Center.
    It will return a list of dictionaries if successful, otherwise it returns an empty list.
    """
    topology_data = get_physical_topology_nodes_links(session_c)
    nodes, links = topology_data

    mapping_list = []
    for node in nodes:
        if "Unified AP" in node["family"]:
            ap_device_uuid, ap_device_label, ap_platform_id = (node["id"],
                                                               node["label"],
                                                               node["platformId"])
            mapping_list.extend(
                filter(
                    None, [
                        process_link(
                            link,
                            nodes,
                            ap_device_label,
                            ap_device_uuid,
                            ap_platform_id
                            )
                            for link in links
                            if ap_device_uuid in (link['source'], link['target'])
                    ]
                )
            )

    # Filtering for demo purposes
    demo_mapping_list = [ap for ap in mapping_list if "Skog" in ap["interface_label"]]
    return demo_mapping_list

def unique_poe_access_sw(session_c: DNACenterAPI) -> list:
    """
    Retrieves list of all switches that have APs connected to them
    """
    poe_devices_data = create_cc_data_mapping(session_c)
    all_switches = []
    for item in poe_devices_data:
        all_switches.append(item["switch_deviceUuid"])

    uniqe_switches_uuids = list(set(all_switches))

    return uniqe_switches_uuids

def get_cc_poe_data(session_c: DNACenterAPI, interface_name: str) -> int:
    """
    Retrieves PoE consumption data per switch interface that is connected
    to an Access Point.
    """
    unique_switch_ids = unique_poe_access_sw(session_c)
    for item in unique_switch_ids:
        device_uuid = item
        try:
            response = session_c.devices.poe_interface_details(device_uuid)
            for poe_interface in response["response"]:
                if poe_interface["interfaceName"] == interface_name:
                    poe_data_watts = poe_interface["portPowerDrawn"]
            return poe_data_watts
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error("Failed to get PoE interface details from CC: %s", e)
            return None

def build_cc_dataset(session_c) -> list:
    """
    Builds the final dataset that will be stored in the database with relevant data
    for Catalyst Center.
    """
    data_list = []

    data = create_cc_data_mapping(session_c)

    for item in data:

        interface_name = item["interface_name"]
        poe_consumption = get_cc_poe_data(session_c, interface_name)

        dataset = {}
        dataset["sw_name"] = item["switch_label"]
        dataset["sw_serial"] = item["switch_deviceUuid"]
        dataset["port_id"] = item["interfaceUuid"]
        dataset["port_name"] = interface_name
        dataset["power_in_w"] = poe_consumption
        dataset["ap_name"] = item["interface_label"]
        dataset["ap_serial"] = item["ap_platform_id"]

        data_list.append(dataset)
    return data_list


# Meraki backend
def initiate_meraki_session() -> DashboardAPI:
    """
    Returns an instance of the DashboardAPI class from meraki
    """
    try:
        dashboard = DashboardAPI(MERAKI_KEY, print_console=False)
        return dashboard
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to initiate Meraki Dashboard session: %s", e)
        return None

def get_organization_id(session_m: DashboardAPI) -> str:
    """
    Retrieves organization ID
    """
    try:
        my_orgs = session_m.organizations.getOrganizations()

        for item in my_orgs:
            if item["name"] == ORG:
                organization_id = item["id"]

        return organization_id
    
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to get Meraki organization ID data: %s", e)
        return None

def get_network_ids(session_m: DashboardAPI) -> list:
    """
    Retrieves network IDs for specific organization
    """
    organization_id = get_organization_id(session_m)
    try:
        networks = session_m.organizations.getOrganizationNetworks(
            organization_id, total_pages="all"
        )
        network_ids = []
        for network in networks:
            if network["name"] in NETWORKS:
                network_ids.append(network["id"])

        return network_ids
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to get Meraki organization networks data: %s", e)
        return None


def get_access_devices(session_m: DashboardAPI) -> list:
    """
    Retrieves all meraki access devices (switches and wireless)
    """
    network_ids_list = get_network_ids(session_m)

    access_data = []

    for item in network_ids_list:
        networkid = item
        try:
            devices_data = session_m.networks.getNetworkDevices(networkid)
            for device in devices_data:
                if "switch" in device["firmware"]:
                    access_data.append(device)
                elif "wireless" in device["firmware"]:
                    access_data.append(device)

            return access_data
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error("Failed to get Meraki network devices data: %s", e)
            return None


def get_active_poe_port_statuses(session_m: DashboardAPI) -> list:
    """
    Retrieve all PoE port statuses and watt data.
    """
    access_data = get_access_devices(session_m)

    for access_device in access_data:
        if "switch" in access_device["firmware"]:
            sw_serial = access_device["serial"]
    try:
        port_statuses = session_m.switch.getDeviceSwitchPortsStatuses(
            serial=sw_serial, timespan=3600
        )

        return port_statuses
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error("Failed to get Meraki switchport data: %s", e)
        return None
    



def build_meraki_dataset(session_m: DashboardAPI) -> dict:
    """
    Builds final meraki dataset.
    """
    access_data = get_access_devices(session_m)

    for access_device in access_data:
        if "switch" in access_device["firmware"]:
            sw_serial = access_device["serial"]
            sw_model = access_device["model"]
        else:
            ap_serial = access_device["serial"]
            ap_model = access_device["model"]

    port_statuses = get_active_poe_port_statuses(session_m)

    dataset = {}
    for port in port_statuses:
        if port["status"] == "Connected":
            if port["isUplink"] is False:
                print("not an uplink")
                if port["powerUsageInWh"] != 0.0:
                    dataset["sw_name"] = sw_model
                    dataset["sw_serial"] = sw_serial
                    dataset["port_id"] = port["portId"]
                    dataset["port_name"] = port["portId"]
                    dataset["power_in_w"] = port["powerUsageInWh"]
                    dataset["ap_name"] = ap_model
                    dataset["ap_serial"] = ap_serial
                else:
                    pass
            else:
                pass
        else:
            pass


    return [dataset]