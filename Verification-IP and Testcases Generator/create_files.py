# importing dependancies
import os
from globals import *
from component_functions import *
from select_components import *
from create_module import *
from object_functions import *
from run import create_run_file

# create a list of components to be created
# from the dictionary, one of the most important
# function in the script
def reverse_list(comp_hierarchy, comp_list = []):
    revList = []
    for key in comp_hierarchy:
        comp_list.append(key)
        if isinstance(comp_hierarchy[key], dict):
            comp_list = reverse_list(comp_hierarchy[key])
        elif isinstance(comp_hierarchy[key], list):
            comp_list += comp_hierarchy[key]
        elif isinstance(comp_hierarchy[key], str):
            comp_list.append(comp_hierarchy[key])
    return comp_list

# a secont most important function
# returns a dictionary which contains
# name of the component as a key and
# handles to be created as a value
def dict_recursion(comp_handles = {}, comptree = {}):
    for key in comptree:
        if isinstance(comptree[key], dict):
            comp_handles.update({key : list(comptree[key])})
            debug(f'updated dict: {comp_handles}')
            comp_handles = dict_recursion(comp_handles, comptree[key])
        else:
            comp_handles.update({key : comptree[key]})
            debug(f'updated dict: {comp_handles}')
    return comp_handles

# create directories function
# creates directories in below format
# project (prefix + project name)
# |--> DEVELOPMENT
#    |--> ENV
#    |--> RTL
#    |--> SIM
#    |--> SRC
#    |--> TEST
#    |--> TOP
def create_directories():
    os.makedirs(folder_name, exist_ok=True)
    os.makedirs(os.path.join(folder_name, 'DEVELOPMENT'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'ENV'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'RTL'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'SIM'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'SRC'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'TEST'), exist_ok=True)
    os.makedirs(os.path.join(folder_name + '/DEVELOPMENT', 'TOP'), exist_ok=True)

# creates components from dictionary returned
# by 'dict_recursion' function
def create_from_dictionary(args, comp_handle = {}, testbench = {}, objects = [], interface = []):
    create_directories()
    print()
    for key in comp_handle:
        full_path = return_path(key)
        print(f'creating file : {key} at {full_path}')
        debug(f'component name : {key} handles : {",".join(comp_handle[key])}')
        debug()
        with open(full_path, 'w') as file:
            file.write(create_component(key, ','.join(comp_handle[key])))
        for name in comp_handle[key]:
            full_path = return_path(name)
            if os.path.isfile(full_path) == False:
                print(f'creating file : {name} at {full_path}')
                debug(f'component name : {key} handles : None')
                debug()
                with open(full_path, 'w') as file:
                    file.write(create_component(name))
            else:
                debug(f'file {name} already exists!!')

    # create base test class
    full_path = return_path('base_test')
    print(f'creating file : base_test at {full_path}')
    with open(full_path, 'w') as file:
        file.write(create_test('base_test', ','.join(list(testbench))))

    # create objects
    for name in objects:
        full_path = return_path(name)
        print(f'creating file : {name} at {full_path}')
        debug()
        with open(full_path, 'w') as file:
            file.write(create_object(name))

    # temporary solution for extend type in case of multiple environments
    if args.environment == True:
        full_path = return_path('transaction')
        with open(full_path, 'w') as file:
            file.write(create_object('transaction'))

    # convert to list and then reverse the list.
    # very important step, else files will be
    # included in reverse order in package
    # resulting in compilation error in sv..
    comp_list = reverse_list(testbench)
    comp_list.reverse()

    # append base test at last
    comp_list.append('base_test')

    # required to prevent compilation error
    # since drivers are parameterized with
    # transaction class objects in UVM..
    if 'transaction' not in objects:
        objects.append(f'transaction')

    # create a package file
    full_path = return_path('package')
    with open(full_path, 'w') as file:
        file.write(create_package(comp_list, objects, interface))

    # create interface files
    for name in interface:
        full_path = return_path(name)
        print(f'creating file : {name} at {full_path}')
        debug()
        with open(full_path, 'w') as file:
            file.write(create_interface(name))

    # create top module file
    full_path = return_path('top')
    print(f'creating file : {project_name}_top at {full_path}')
    debug()
    with open(full_path, 'w') as file:
        file.write(top_module(interface))

    # creating a python script
    # for compilation and simulation of
    # the Verification IP in 'SIM' folder
    full_path = return_path('run', is_py=True)
    print(f'creating python script : run.py at {full_path}')
    with open(full_path, 'w') as file:
        file.write(create_run_file(project_name))