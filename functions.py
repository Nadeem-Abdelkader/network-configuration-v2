"""
NETWORK CONFIGURATION SCREEN Application - v2
- Reads user network configuration data from multiple .txt files then allows user to edit and writes back updated data
to .txt files

Created by: Nadeem Abdelkader on 11/4/2022
Last updated by Nadeem Abdelkader on 11/4/2022

GUI framework = Tkinter

This file contains the helper function to be called from main.py
"""

# importing the necessary libraries
from tkinter import Frame, Label, Entry, X, LEFT, RIGHT, YES, messagebox, Button, Tk, TOP, ttk, StringVar, OptionMenu, \
    END

from parsing import read_from_txt_files, write_to_files

# declaring globals and constants to be used everywhere in the module
global entries, labels, value_inside_inet, value_inside_iface, my_ents, txt_result
global Network_tab, FQND_tab

data_dict = read_from_txt_files()

FIELDS = {
    'iface': 'Interface',
    'inet': 'Internet Networking',
    'address': 'IP address',
    'netmask': 'Netmask',
    'gateway': 'Gateway',
    'hostname': 'Host Name',
    'domain': 'Domain',
    'nameserver': 'Name Servers'
}


def track_iface(var, index, mode):
    """
    This function tracks changes that happen to the iface field in order to update the corresponding fields
    (inet, address, netmask, gateway)
    :return: void
    """
    current_choice = [d for d in data_dict['INTERFACESOPTS'] if d['iface'] == value_inside_iface.get()]
    value_inside_inet.set(current_choice[0]['inet'])

    entries['address'].delete(0, END)
    entries['address'].insert(0, current_choice[0]['address'])

    entries['netmask'].delete(0, END)
    entries['netmask'].insert(0, current_choice[0]['netmask'])

    entries['gateway'].delete(0, END)
    entries['gateway'].insert(0, current_choice[0]['gateway'])

    return


def track_inet(var, index, mode):
    """
    This function tracks changes that happen to the inet field in order to hide/show the corresponding fields
    (address, netmask, gateway)
    :return: void
    """
    if value_inside_inet.get() == 'dhcp':
        entries['address'].pack_forget()
        labels['address'].pack_forget()

        entries['netmask'].pack_forget()
        labels['netmask'].pack_forget()

        entries['gateway'].pack_forget()
        labels['gateway'].pack_forget()
    else:
        entries['address'].pack(side=RIGHT, expand=YES, fill=X)
        labels['address'].pack(side=LEFT)

        entries['netmask'].pack(side=RIGHT, expand=YES, fill=X)
        labels['netmask'].pack(side=LEFT)

        entries['gateway'].pack(side=RIGHT, expand=YES, fill=X)
        labels['gateway'].pack(side=LEFT)
    return


def make_form(fields):
    """
    This function created the actual GUI form using Tkinter Entry, Label, and Frames
    :param fields: array of strings that include the field names to createb the form according to
    :return: an array of Tkinter entries
    """
    global entries, labels, value_inside_inet, value_inside_iface
    entries = {}
    labels = {}
    iface_options = []
    for i in data_dict['INTERFACESOPTS'][1:]:
        iface_options.append(i['iface'])
    inet_options = ["static", "dhcp"]
    value_inside_iface = StringVar(my_root)
    value_inside_inet = StringVar(my_root)

    value_inside_iface.trace_add('write', track_iface)
    value_inside_inet.trace_add('write', track_inet)

    for field in fields:
        if field in ['domain', 'nameserver', 'hostname']:
            row = Frame(FQND_tab)
        else:
            row = Frame(Network_tab)
        lab = Label(row, width=22, text=FIELDS[field] + ": ", anchor='w')
        if field == 'iface':
            ent = OptionMenu(row, value_inside_iface, *iface_options)
        elif field == 'inet':
            ent = OptionMenu(row, value_inside_inet, *inet_options)
        else:
            ent = Entry(row)
        if field in ['iface', 'inet']:
            pass
        elif field in ['address', 'netmask', 'gateway']:
            ent.insert(0, data_dict['INTERFACESOPTS'][1][field])
        else:
            if type(data_dict[field]) == list:
                for j in data_dict[field]:
                    ent.insert(0, j + ", ")
            else:
                ent.insert(0, data_dict[field])
        if not (value_inside_inet.get() == 'dhcp' and field in ['address', 'netmask', 'gateway']):
            ent.pack(side=RIGHT, expand=YES, fill=X)
            row.pack(side=TOP, fill=X, padx=25, pady=5)
            lab.pack(side=LEFT)
        entries[field] = ent
        labels[field] = lab

    value_inside_iface.set(data_dict['INTERFACESOPTS'][1]['iface'])
    value_inside_inet.set(data_dict['INTERFACESOPTS'][1]['inet'])
    return entries


def submit(my_ents):
    """
    This function is executed when the user fills in all the inforamtion and clicks submit.
    It takes all the entered information an writes it to a .json file (users.json)
    :param my_ents: an array of entries that contain the entered information
    :return: void
    """
    # Comment this out (next 10 lines) if you want to make all fields optional
    empty_field = False
    for i in entries:
        if i in ['iface', 'inet']:
            pass
        else:
            if entries[i].get() == "" or entries[i].get() == []:
                empty_field = True
    if empty_field:
        txt_result.config(text="Please complete the required field!", fg="red")
    else:
        for i in my_ents:
            if i in ['iface', 'inet', 'address', 'netmask', 'gateway']:
                for j in data_dict['INTERFACESOPTS']:
                    if j['iface'] == value_inside_iface.get():
                        j['inet'] = value_inside_inet.get()
                        if value_inside_inet.get() == 'dhcp':
                            j['address'] = ''
                            j['netmask'] = ''
                            j['gateway'] = ''
                        else:
                            j['address'] = my_ents['address'].get()
                            j['netmask'] = my_ents['netmask'].get()
                            j['gateway'] = my_ents['gateway'].get()
            else:
                if i == 'nameserver':
                    data_dict[i] = my_ents[i].get().split(", ")[::-1]
                    data_dict[i] = list(filter(None, data_dict[i]))
                else:
                    data_dict[i] = my_ents[i].get()
        write_to_files(data_dict)
        txt_result.config(text="Successfully submitted data!", fg="green")
        clear(my_ents, True)
    return


def read(my_ents):
    """
    This function re reads data from .txt file and re populates the entries
    :param my_ents: entries to re populate
    :return: void
    """
    for field in FIELDS:
        if field in ['iface', 'inet']:
            pass
        elif field in ['address', 'netmask', 'gateway']:
            my_ents[field].delete(0, 'end')
            my_ents[field].insert(0, data_dict['INTERFACESOPTS'][1][field])
        else:
            my_ents[field].delete(0, 'end')
            if type(data_dict[field]) == list:
                for j in data_dict[field]:
                    my_ents[field].insert(0, j + ", ")
            else:
                my_ents[field].insert(0, data_dict[field])
    value_inside_iface.set(data_dict['INTERFACESOPTS'][1]['iface'])
    value_inside_inet.set(data_dict['INTERFACESOPTS'][1]['inet'])
    txt_result.config(text="Successfully read data!", fg="green")
    return entries


def clear(my_ents, on_submit=False):
    """
    This function is executed when the users clicks the "clear" button.
    It resets the entire form
    :param my_ents: an array of entries to clear
    :param on_submit: if clear on submit or not in order to display the correct message
    :return: void
    """
    for i in my_ents:
        if i == 'iface':
            value_inside_iface.set(data_dict['INTERFACESOPTS'][1]['iface'])
        elif i == 'inet':
            value_inside_inet.set(data_dict['INTERFACESOPTS'][1]['inet'])
        else:
            entries[i].delete(0, 'end')
    if not on_submit:
        txt_result.config(text="Successfully cleared data!", fg="green")


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


def create_buttons():
    """
    This function creates 4 buttons (submit, clear, read, and quit) and associates them with the appropriate methods
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


def make_tabs(my_root):
    """
    This function creates the 2 seperate tabs of our program (Network and FQND)
    :param my_root: root Tkinter window
    :return: void
    """
    global Network_tab, FQND_tab
    tab_control = ttk.Notebook(my_root)
    Network_tab = Frame(tab_control)
    FQND_tab = Frame(tab_control)
    tab_control.add(Network_tab, text='Network')
    tab_control.add(FQND_tab, text='FQND')
    tab_control.pack()
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


def initialise_window():
    """
    This function initialises the Tkinter GUI window
    :return: root Tkinter window
    """
    global my_root, my_ents
    my_root = Tk()
    my_root.resizable(True, True)
    make_tabs(my_root)
    my_ents = make_form(FIELDS)
    text_alert()
    create_buttons()
    my_root.geometry("550x330")
    my_root.title("Network Configuration")
    return my_root


my_root = initialise_window()
