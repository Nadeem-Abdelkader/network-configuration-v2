# PARSING FOR NETWORK CONFIG INTERFACE
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
# BASE_DIR = "KC/"

# For development
OS_BASE_DIR = BASE_DIR

# For production
# OS_BASE_DIR = "/"

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
    resolv_file = open(RESOLV_FILE, 'r')
    domain = resolv_file.readline().split()
    res = [domain[1]]
    nameservers = resolv_file.readlines()
    nameservers_lst = []
    for i in range(len(nameservers)):
        a = nameservers[i].strip("\n").split()
        nameservers_lst.append(a[1])
    res.append(nameservers_lst)
    return domain[1], nameservers_lst


def read_from_hostname_file():
    host_file = open(HOST_FILE, 'r')
    hostname = host_file.read()
    return hostname


def read_from_interfaces_file():
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


# data = read_from_txt_files()
# print(data)
# write_to_files(data)
