"""
NETWORK CONFIGURATION SCREEN Application - v2
- Reads user network configuration data from multiple .txt files then allows user to edit and writes back updated data
to .txt files

Created by: Nadeem Abdelkader on 11/4/2022
Last updated by Nadeem Abdelkader on 11/4/2022

GUI framework = Tkinter

This file contains the helper functions that are used for parsing txt files to dictionaries in functions.py
"""

# declaring the constants to be used everywhere in the module
INTERFACESOPTS_FIELDS = ['iface', 'inet', 'address', 'netmask', 'gateway']
MAIN_FIELDS = ['INTERFACESOPTS', 'hostname', 'domain', 'nameserver']

INTERFACE_TYPES = ['loopback', 'dhcp', 'static']

INTERFACESOPTS_DICT = {
    INTERFACESOPTS_FIELDS[0]: "",
    INTERFACESOPTS_FIELDS[1]: "",
    INTERFACESOPTS_FIELDS[2]: "",
    INTERFACESOPTS_FIELDS[3]: "",
    INTERFACESOPTS_FIELDS[4]: "",
}

MAIN_DICT = {
    MAIN_FIELDS[0]: [],
    MAIN_FIELDS[1]: "",
    MAIN_FIELDS[2]: "",
    MAIN_FIELDS[3]: [],
}

BASE_DIR = "/usr/local/KC/"

# For development
OS_BASE_DIR = BASE_DIR

# For production
OS_BASE_DIR = "/"

ANSWERS_FILE = OS_BASE_DIR + "config/answers.txt"
HOST_FILE = OS_BASE_DIR + "etc/hostname"
INTERFACES_FILE = OS_BASE_DIR + "etc/network/interfaces"
RESOLV_FILE = OS_BASE_DIR + "etc/resolv.conf"


def read_from_txt_files():
    """
    This function reads data from a txt file to a dictionary
    :param filename: file to read from
    :return: dictionary contining read data
    """
    interfaces = read_from_interfaces_file()
    hostname = read_from_hostname_file()
    domain, nameservers = read_from_resolv_file()
    local_dict = dict.fromkeys(MAIN_DICT)
    local_dict[MAIN_FIELDS[0]] = interfaces
    local_dict[MAIN_FIELDS[1]] = hostname
    local_dict[MAIN_FIELDS[2]] = domain
    local_dict[MAIN_FIELDS[3]] = nameservers
    return local_dict


def read_from_resolv_file():
    """
    This function reads and returns the domain name and the nameservers from resolv.conf file
    :return: domain name and list of nameservers in a tuple (domain name, [nameserver])
    """
    resolv_file = open(RESOLV_FILE, 'r')
    content = resolv_file.readlines()
    nameservers_lst = []
    domain = ""
    for i in range(len(content)):
        a = content[i].strip("\n").split()
        if a[0] == MAIN_FIELDS[2]:
            domain = a[1]
        elif a[0] == MAIN_FIELDS[3]:
            nameservers_lst.append(a[1])
    return domain, nameservers_lst


def read_from_hostname_file():
    """
    This function reads and returns the hostname from hostname file
    :return: hostname
    """
    host_file = open(HOST_FILE, 'r')
    hostname = host_file.read()
    return hostname


def read_from_interfaces_file():
    """
    This function reads and returns the iface, inet, address, netmask, and gateway from the interfaces file
    :return: interfaces: a list of dictionaries where each dictionary contains the configuration for a certain
                         interfaces (e.g. eth0, eth1, etc...)
    """
    interfaces = []
    interfaces_file = open(INTERFACES_FILE, 'r').read().split("\n\n")
    for interface in interfaces_file:
        local_dict = dict.fromkeys(INTERFACESOPTS_DICT, "")
        interface = interface.split()
        for i in range(len(interface)):
            if interface[i] in INTERFACESOPTS_DICT:
                local_dict[interface[i]] = interface[i + 1]
        interfaces.append(local_dict)
    return interfaces


def write_to_files(data):
    """
    This function writes a dictionary to 3 files (resolv.conf, hostname, interfaces)
    :param data: dictioanry to write to files
    :return: void
    """
    interfaces_file = open(INTERFACES_FILE, 'w')
    host_file = open(HOST_FILE, 'w')
    resolv_file = open(RESOLV_FILE, 'w')

    for i in data:
        if i == MAIN_FIELDS[0]:
            for j in data[i]:
                if j[INTERFACESOPTS_FIELDS[1]] == INTERFACE_TYPES[0]:
                    interfaces_file.write(
                        "auto " + j[INTERFACESOPTS_FIELDS[0]] + "\n" + INTERFACESOPTS_FIELDS[0] + " " + j[
                            INTERFACESOPTS_FIELDS[0]] + " " + INTERFACESOPTS_FIELDS[1] + " " + j[
                            INTERFACESOPTS_FIELDS[1]] + "")
                elif j[INTERFACESOPTS_FIELDS[1]] == INTERFACE_TYPES[1]:
                    interfaces_file.write(
                        "\n\nauto " + j[INTERFACESOPTS_FIELDS[0]] + "\n" + INTERFACESOPTS_FIELDS[0] + " " + j[
                            INTERFACESOPTS_FIELDS[0]] + " " + INTERFACESOPTS_FIELDS[1] + " " + j[
                            INTERFACESOPTS_FIELDS[1]] + "")
                elif j[INTERFACESOPTS_FIELDS[1]] == INTERFACE_TYPES[2]:
                    interfaces_file.write(
                        "\n\nauto " + j[INTERFACESOPTS_FIELDS[0]] + "\n" + INTERFACESOPTS_FIELDS[0] + " " + j[
                            INTERFACESOPTS_FIELDS[0]] + " " + INTERFACESOPTS_FIELDS[1] + " " + j[
                            INTERFACESOPTS_FIELDS[1]] + "")
                    interfaces_file.write(
                        "\n    " + INTERFACESOPTS_FIELDS[2] + " " + j[INTERFACESOPTS_FIELDS[2]] + "\n    " +
                        INTERFACESOPTS_FIELDS[3] + " " + j[INTERFACESOPTS_FIELDS[3]] + "\n    " + INTERFACESOPTS_FIELDS[
                            4] + " " + j[
                            INTERFACESOPTS_FIELDS[4]] + "")
        elif i == MAIN_FIELDS[1]:
            host_file.write(data[i])
        elif i == MAIN_FIELDS[2]:
            resolv_file.write(MAIN_FIELDS[2].lower() + " " + data[i] + "\n")
        elif i == MAIN_FIELDS[3]:
            for j in data[i]:
                resolv_file.write(MAIN_FIELDS[3].lower() + " " + j + "\n")
    return
