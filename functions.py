"""
NETWORK CONFIGURATION SCREEN Application
- Reads user network configuration data from multiple .txt files then allows user to edit and writes back updated data
to .txt files

Created by: Nadeem Abdelkader on 11/4/2022
Last updated by Nadeem Abdelkader on 11/4/2022

GUI framework = Tkinter

This file contains the helper function to be called from main.py
"""

# importing the necessary libraries for working with json
from tkinter import Frame, Label, Entry, X, LEFT, RIGHT, YES, messagebox, Button, Tk, TOP, ttk

# declaring the constants to be used everywhere in the module
FIELDS_1 = ['KEYMAPOPTS', 'HOSTNAMEOPTS', 'INTERFACESOPTS', 'DNSOPTS', 'TIMEZONEOPTS', 'PROXYOPTS',
            'APKREPOSOPTS', 'SSHDOPTS', 'NTPOPTS', 'DISKOPTS', 'LBUOPTS', 'APKCACHEOPTS']

FIELDS_2 = ['iface', 'inet', 'address', 'netmask', 'gateway', 'hostname', 'domain', 'nameserver']

DISPlAY_FIELDS = ['Interface', 'Internet Networking', 'IP address', 'Netmask', 'Gateway', 'Host Name', 'Domain',
                  'Name Servers']

BASE_DIR = "/usr/local/KC/"

# For development
OS_BASE_DIR = BASE_DIR

# For production
# OS_BASE_DIR = "/"

ANSWERS_FILE = OS_BASE_DIR + "config/answers.txt"
HOST_FILE = OS_BASE_DIR + "etc/hostname"
INTERFACES_FILE = OS_BASE_DIR + "etc/network/interfaces"
RESOLVE_FILE = OS_BASE_DIR + "etc/resolv.conf"

MANUAL = True

global txt_result
global my_ents
global FQND_tab, Network_tab

data_dict_1 = {
    FIELDS_1[0]: "",
    FIELDS_1[1]: "",
    FIELDS_1[2]: "",
    FIELDS_1[3]: "",
    FIELDS_1[4]: "",
    FIELDS_1[5]: "",
    FIELDS_1[6]: "",
    FIELDS_1[7]: "",
    FIELDS_1[8]: "",
    FIELDS_1[9]: "",
    FIELDS_1[10]: "",
    FIELDS_1[11]: "",
}

data_dict_2 = {
    FIELDS_2[0]: "",
    FIELDS_2[1]: "",
    FIELDS_2[2]: "",
    FIELDS_2[3]: "",
    FIELDS_2[4]: "",
    FIELDS_2[5]: "",
    FIELDS_2[6]: [],
    FIELDS_2[7]: ""
}


def write_answers_txt():
    cont = True

    if cont:
        my_dict = read_to_dict_1(ANSWERS_FILE)
        filename = ANSWERS_FILE
        comments = ["# Example answer file for setup-alpine script\n"
                    "# If you don't want to use a certain option, then comment it out\n\n"
                    "# Use US layout with US variant\n",
                    "\n# Set hostname to alpine-test\n",
                    "\n# Contents of /etc/network/interfaces\n",
                    "\n# Search domain of example.com, Google public nameserver\n",
                    "\n# Set timezone to UTC\n",
                    "\n# set http/ftp proxy\n",
                    "\n# Add a random mirror\n",
                    "\n# Install Openssh\n",
                    "\n# Use openntpd\n",
                    "\n# Use /dev/sda as a data disk\n",
                    "\n# Setup in /media/sdb1\n"
                    ]
        with open(filename, 'w') as file:
            for i in range(len(FIELDS_1)):
                if i < len(comments):
                    file.write(comments[i])
                if my_dict[FIELDS_1[i]] == "":
                    if my_dict[FIELDS_1[i]].startswith("-"):
                        file.write(FIELDS_1[i] + "=\"" + my_dict[FIELDS_1[i]][:2] + "" + my_dict[FIELDS_1[i]] + "\"")
                    else:
                        file.write(FIELDS_1[i] + "=\"" + my_dict[FIELDS_1[i]] + "\"")
                else:
                    if my_dict[FIELDS_1[i]].startswith("-"):
                        file.write(FIELDS_1[i] + "=\"" + my_dict[FIELDS_1[i]][:2] + " " + my_dict[FIELDS_1[i]] + "\"")
                    else:
                        file.write(FIELDS_1[i] + "=\"" + my_dict[FIELDS_1[i]] + "\"")
                file.write("\n")
            file.write("\n")
    return


def read_to_dict_1(filename):
    """
    This function reads data from a txt file to a dictionary
    :param filename: file to read from
    :return: dictionary contining read data
    """
    f = open(filename, 'r')
    f = f.read()
    f = f.split('\"')
    for i in range(len(f)):
        for j in range(len(FIELDS_1)):
            if f[i].endswith(FIELDS_1[j] + "="):
                if f[i + 1].startswith("-"):
                    data_dict_1[FIELDS_1[j]] = f[i + 1][3:]
                else:
                    data_dict_1[FIELDS_1[j]] = f[i + 1]
    return data_dict_1


def read_to_dict_2():
    """
    This function reads data from a txt file to a dictionary
    :return: dictionary containing read data
    """
    filename = INTERFACES_FILE
    data_dict_2['nameserver'] = []
    if filename == INTERFACES_FILE:
        f = open(filename, 'r')
        f = f.read()
        f = f.replace('\n', ' ')
        f = f.split(' ')
        for i in range(len(f)):
            for j in range(len(FIELDS_2)):
                if f[i] == FIELDS_2[j]:
                    data_dict_2[FIELDS_2[j]] = f[i + 1]
    filename = RESOLVE_FILE
    if filename == RESOLVE_FILE:
        f = open(filename, 'r')
        f = f.read()
        f = f.replace('\n', ' ')
        f = f.split(' ')
        f = list(filter(None, f))
        f = list(filter(bool, f))
        f = list(filter(len, f))
        f = list(filter(lambda item: item, f))
        for i in range(len(f)):
            for j in range(len(FIELDS_2)):
                if f[i] == FIELDS_2[j]:
                    if FIELDS_2[j] == 'nameserver':
                        data_dict_2[FIELDS_2[j]].append(str(f[i + 1]))
                    else:
                        if (i + 1) < len(f):
                            data_dict_2[FIELDS_2[j]] = str(f[i + 1])
                        else:
                            data_dict_2[FIELDS_2[j]] = ""

    filename = HOST_FILE
    if filename == HOST_FILE:
        f = open(filename, 'r')
        f = f.read()
        f = f.replace("\n", "")
        f = f.split("           ")
        data_dict_2[FIELDS_2[5]] = f[0]

    return data_dict_2


def read_txt_to_lst(filename):
    """
    This function reads the data from .txt file to a list
    :param filename: txt file to read from
    :return: list containing the data
    """
    mylines = []
    with open(filename, 'rt') as myfile:
        for myline in myfile:
            if myline.startswith(FIELDS_2[0]) or myline.startswith(FIELDS_2[1]) or myline.startswith(
                    FIELDS_2[2]) or \
                    myline.startswith(FIELDS_2[3]) or myline.startswith(FIELDS_2[4]) or myline.startswith(FIELDS_2[5]) \
                    or myline.startswith(FIELDS_2[6]) or myline.startswith(FIELDS_2[7]) or \
                    myline.startswith(FIELDS_2[8]) or myline.startswith(FIELDS_2[9]) or \
                    myline.startswith(FIELDS_2[10]) or \
                    myline.startswith(FIELDS_2[11]):
                start = myline.find("\"")
                end = myline.rfind("\"")
                if myline[start + 1:end].startswith("-"):
                    mylines.append(myline[start + 4:end])
                else:
                    mylines.append(myline[start + 1:end])
    return mylines


def make_form(root, fields):
    """
    This function created the actual GUI form using Tkinter Entry, Label, and Frames
    :param root: root Tkinter window
    :param fields: array of strings that include the field names to createb the form according to
    :return: an array of Tkinter entries
    """
    entries = {}
    i = 0
    data = read_to_dict_2()
    for field in fields:
        if field in ['domain', 'nameserver', 'hostname']:
            row = Frame(FQND_tab)
        else:
            row = Frame(Network_tab)
        lab = Label(row, width=22, text=DISPlAY_FIELDS[i] + ": ", anchor='w')
        if field == "Password" or field == "Re-enter Password":
            ent = Entry(row, show="*")
        else:
            ent = Entry(row)
            if type(data[field]) != list and data[field].startswith("-"):
                ent.insert(0, data[field][3:])
            else:
                if type(data[field]) == list:
                    for j in data[field]:
                        ent.insert(0, j + ", ")
                else:
                    ent.insert(0, data[field])
        ent.insert(0, "")
        if MANUAL:
            row.pack(side=TOP, fill=X, padx=25, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
        else:
            if field in ['hostname', 'domain', 'nameserver']:
                row.pack(side=TOP, fill=X, padx=25, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
        i += 1
    return entries


def read(ents):
    """
    This function re reads data from .txt file and re populates the entries
    :param ents: entries to re populate
    :return: void
    """

    data = read_to_dict_2()
    for i in range(len(FIELDS_2)):
        ents[FIELDS_2[i]].delete(0, 'end')
        if FIELDS_2[i] == 'nameserver':
            data[FIELDS_2[i]] = list(dict.fromkeys(data[FIELDS_2[i]]))
            for j in data[FIELDS_2[i]]:
                ents[FIELDS_2[i]].insert(0, j + ", ")
        else:
            if type(data[FIELDS_2[i]]) != list:
                if data[FIELDS_2[i]].startswith("-"):
                    ents[FIELDS_2[i]].insert(0, data[FIELDS_2[i]][3:])
                else:
                    ents[FIELDS_2[i]].insert(0, data[FIELDS_2[i]])
    txt_result.config(text="Successfully read data!", fg="green")
    return


def make_label(root):
    """
    This function adds the GUI heading
    :param root: root Tkinter window
    :return: void
    """
    txt_title = Label(root, width=0, font=(
        'arial', 10), text="dasdasdasda")
    txt_title.pack(side=TOP, padx=5, pady=5)
    return


def submit(entries):
    """
    This function is executed when the user fills in all the inforamtion and clicks submit.
    It takes all the entered information an writes it to a .json file (users.json)
    :param entries: an array of entries that contain the entered information
    :return: void
    """
    # Uncomment this if you want to make all fields except 'address', 'netmask', and 'gateway' required
    empty_field = False
    for i in entries:
        # Remove this if condition if you want to make all fields required
        if i not in ['address', 'netmask', 'gateway']:
            if entries[i].get() == "" or entries[i].get() == []:
                empty_field = True
    if empty_field:
        txt_result.config(text="Please complete the required field!", fg="red")
    else:
        cont = True
        if cont:
            my_dict = {}
            for i in range(len(entries)):
                my_dict[FIELDS_2[i]] = entries[FIELDS_2[i]].get()

            interfaces_file = INTERFACES_FILE
            resolve_file = RESOLVE_FILE
            host_file = HOST_FILE

            interfaces_file = open(interfaces_file, 'w')
            interfaces_file.write("auto lo\niface lo inet loopback\n\nauto " + my_dict['iface'] + "\n")
            resolve_file = open(resolve_file, 'w')
            host_file = open(host_file, 'w')
            for i in range(len(FIELDS_2)):
                if FIELDS_2[i] in ['iface', 'inet', 'address', 'netmask', 'gateway']:
                    if my_dict['inet'] == 'dhcp':
                        if FIELDS_2[i] in ['iface', 'inet']:
                            if i >= 1:
                                interfaces_file.write(FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + "\n")
                            else:
                                interfaces_file.write(FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + " ")
                    else:
                        if i >= 1:
                            if FIELDS_2[i] != 'inet':
                                interfaces_file.write("    " + FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + "\n")
                            else:
                                interfaces_file.write("" + FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + "\n")
                        else:
                            interfaces_file.write(FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + " ")
                if FIELDS_2[i] in ['domain', 'nameserver']:
                    if FIELDS_2[i] == 'domain':
                        resolve_file.write(FIELDS_2[i] + " " + my_dict[FIELDS_2[i]] + "\n")
                    if FIELDS_2[i] == 'nameserver':
                        my_dict[FIELDS_2[i]] = my_dict[FIELDS_2[i]].replace(" ", "")
                        my_dict[FIELDS_2[i]] = my_dict[FIELDS_2[i]].split(",")
                        my_dict[FIELDS_2[i]] = my_dict[FIELDS_2[i]][::-1]
                        for j in my_dict[FIELDS_2[i]]:
                            if j != "":
                                resolve_file.write(FIELDS_2[i] + " " + j + "\n")
                if FIELDS_2[i] == 'hostname':
                    host_file.write(my_dict[FIELDS_2[i]])
            write_answers_txt()
            txt_result.config(text="Successfully submitted data!", fg="green")
            clear(entries, True)

    return


def clear(entries, on_submit=False):
    """
    This function is executed when the users clicks the "clear" button.
    It resets the entire form
    :param entries: an array of entries to clear
    :param on_submit: if clear on submit or not in order to display the correct message
    :return: void
    """
    for i in range(len(FIELDS_2)):
        entries[FIELDS_2[i]].delete(0, 'end')
    if not on_submit:
        txt_result.config(text="Cleared form!", fg="green")
    return


def quit_program():
    """
    This function is executed when the users clicks the "quit" button.
    It quits the entire application
    :return: void
    """
    result = messagebox.askquestion(
        'Network Configuration', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        my_root.destroy()
    return


def text_alert():
    """
    This function creates the label where we will later add some alerts to the user like
    "please complete the required field" or "Submitted data successfully"
    :return: void
    """
    global txt_result
    txt_result = Label(my_root)
    txt_result.pack()
    return


def create_buttons():
    """
    This function creates 3 buttons (submit, clear, and quit) and associates them with the appropriate methods
    :return: void
    """
    top = Frame(my_root)
    top.pack(side=TOP)
    submit_button = Button(my_root, text="Submit", command=lambda: submit(my_ents), bg='#e4e4e4')
    read_button = Button(my_root, text="Read", command=lambda: read(my_ents))
    clear_button = Button(my_root, text="Clear", command=lambda: clear(my_ents))
    quit_button = Button(my_root, text="Quit", command=quit_program)
    submit_button.pack(in_=top, side=LEFT)
    read_button.pack(in_=top, side=LEFT)
    clear_button.pack(in_=top, side=LEFT)
    quit_button.pack(in_=top, side=LEFT)
    return


def initialise_window():
    """
    This function initialises the Tkinter GUI window
    :return: root Tkinter window
    """
    global my_root, my_ents, FQND_tab, Network_tab
    my_root = Tk()
    my_root.resizable(True, True)
    tabControl = ttk.Notebook(my_root)
    Network_tab = Frame(tabControl)
    FQND_tab = Frame(tabControl)
    tabControl.add(Network_tab, text='Network')
    tabControl.add(FQND_tab, text='FQND')
    tabControl.pack()
    my_ents = make_form(my_root, FIELDS_2)
    # 475x250 - Alpine
    # 550x335 - Others
    my_root.geometry("550x335")
    my_root.title("Network Configuration")
    return my_root


# calling function to initialise the GUI window
my_root = initialise_window()
