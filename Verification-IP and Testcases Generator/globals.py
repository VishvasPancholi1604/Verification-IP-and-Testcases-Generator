import os
import argparse
from datetime import date

# import required functions and variables
# from global required file
from global_required import *

# will print debugging info when set True
# advised to keep as False for general purpose
debug_mode = False

# prefix will be appended before each
# file name and class name along with
# the project name
prefix    = 'ei_'

# verbosity of each `uvm_info messages
# in the skeleton
verbosity = 'UVM_FULL'

# developer name
# will be added in header of each file
developer_name = 'einfochips Ltd'

# project name note
# used to guide user while entering project name
project_name_note = 'Project name will be appended with the prefix, for example ' \
                    f'if project name is \'axi4\' file names will start with \'{prefix}axi4\' prefix.'

# component selection note
# used to guide user while selecting components
# which needs to be created
component_selection_note = 'enter \'all\' to create each component.\nstart with \'!\' to enter ' \
                           'component list which are not to be created. \ni.e. !9,5 will create ' \
                           'every component except \'reference_model\' and \'monitor\''

# environment name note
# used to guide user while naming
# environment components
environment_name_note = 'Environment name should end with \'_environment\' suffix i.e. \'axi_environment\', ' \
                        '\'ahb_environment\', etc. \nFor each environment, user will be asked to enter agent names seperated by comma'

# agent name notes
# used to guide user while naming
# agent components for each environment
agent_name_note = 'Agent name should end with \'_agent\' suffix i.e. \'master_agent\', \'slave_agent\', etc.'

# agent type notes
# used to guide user for selecting
# the type of the agent, which can be
# 1. active, 2. passive or 3. noseqr
agent_type_note = '3 types of agents can be created\n\t1. \'active\' (will create sequencer, driver and monitor files)' \
                  '\n\t2. \'passive\' (will only create a monitor file)' \
                  '\n\t3. \'noseqr\' (will create driver and monitor file, not sequencer)' \
                  '\ndefault agent type is \'active\' if pressed enter to skip..'

# parsing command line arguments
args = get_args()

# project name declaration
# when generating a VIP skeleton it's user defined
# when running the script with '-t' cla, it will
# extract project name from path (user needs to be
# in SIM directory of project..)
if args.testcases == False:
    project_name = input(f'Enter the Project Name \n[NOTE : {project_name_note}] \n>> ')
else:
    current_dir = os.getcwd()
    project_name = find_project_name(current_dir)
project = prefix + project_name

# project folder name declaration
# folder name = prefix + project name
folder_name = project

# debug mode
# prints messages only if debug mode is Enabled
def debug(print_this = ''):
    if debug_mode == True:
        print(print_this)

# header to add in each file
def header(filename = '', title = '', is_module = False):
    type = 'class' if is_module == False else ''
    hdr = f'''// ------------------------------------------------------------------------- 
// File name    : {filename}
// Title        : {project_name} {title.replace('_', ' ')} {type}
// Project      : {project_name.upper()} VIP
// Created On   : {date.today()}
// Developers   : {developer_name}
// Purpose      : 
// Assumptions  : 
// Limitations  :  
// Known Errors : 
// -------------------------------------------------------------------------'''
    return hdr

# add comment box above functions
def comment(method_name = '', parameters_passed = '', returned_parameters = '', description = ''):
    comment = f'''//////////////////////////////////////////////////////////////////
// Method name        : {method_name}
// Parameter Passed   : {parameters_passed}
// Returned Parameter : {returned_parameters}
// Description        : {description}
//////////////////////////////////////////////////////////////////'''
    return comment

# component/object list which can be created
# can be selected by user
component_list = [
    'transaction',
    'sequence',
    'sequencer',
    'driver',
    'monitor',
    'agent',
    'scoreboard',
    'subscriber',
    'reference_model',
    'environment',
    'base_test',
    'interface'
]

# dictionary indicating component to be extended from
# objects/components created will be extended from the same
seq_item = f'{project}_transaction_c'
type_by_name = {
    'seq_item'        : 'uvm_sequence_item',
    'transaction'     : 'uvm_sequence_item',
    'sequencer'       : f'uvm_sequencer#({seq_item})',
    'sequence'        : f'uvm_sequence#({seq_item})',
    'driver'          : f'uvm_driver#({seq_item})',
    'monitor'         : 'uvm_monitor',
    'agent'           : 'uvm_agent',
    'environment'     : 'uvm_env',
    'scoreboard'      : 'uvm_component',
    'subsciber'       : f'uvm_subscriber#({seq_item})',
    'reference_model' : 'uvm_component',
    'base_test'       : 'uvm_test'
}

# returns the type of component by looking from the dictionary
# returns 'uvm_component' if string passed is of undefined type
def lookup_for_comp_type(comp_name = ''):
    for key in type_by_name:
        if key in comp_name:
            return type_by_name[key]
    return 'uvm_component'

# short name for handles to be created
# prefix will be appended if present
handle_short_name = {
    'driver'          : 'drv',
    'monitor'         : 'mon',
    'transaction'     : 'tr',
    'sequencer'       : 'seqr',
    'sequence'        : 'seq',
    'environment'     : 'env',
    'scoreboard'      : 'scb',
    'subscriber'      : 'sub',
    'reference_model' : 'ref'
}

# dictionary for defining path of file
comp_path = {
    'environment' : '/DEVELOPMENT/ENV/',
    'base_test'   : '/DEVELOPMENT/TEST/',
    'top'         : '/DEVELOPMENT/TOP/',
    'run'         : '/DEVELOPMENT/SIM/',
    'test'        : '/DEVELOPMENT/TEST/'
}

# returns the full path of the file
# by looking up in comp_path dict
def return_path(key = '', is_py = False):
    extension = '.sv' if is_py == False else '.py'
    folder = '/DEVELOPMENT/SRC/'
    for dkey in comp_path:
        if dkey in key:
            folder = comp_path[dkey]
            break
    path = folder_name + folder
    file_name = project + '_' + key + extension
    full_path = os.path.join(path, file_name)
    debug(full_path)
    return full_path

# look-up dictionary for component alias
for_prefix = [
    'driver',
    'sequencer',
    'sequence',
    'subscriber'
]

# returns alias of the component
# from look-up dictionary
def return_prefix(name):
    for pname in for_prefix:
        if pname in name:
            if name != pname:
                prefix = name[:-len(pname)]
                return prefix
    return False

# finds package file located in SRC directory
# reads the package file and returns the
# content of the file as a string.
def read_package_file():
    current_path = os.getcwd()
    print()
    if 'DEVELOPMENT' and 'SIM' not in current_path:
        print('[ERROR] Please change directory to \'SIM\'')
    else:
        src_path = current_path[:-len('SIM')] + 'SRC'
        package_path = os.path.join(src_path, f'{project}_package.sv')
        if os.path.isfile(package_path):
            with open(package_path, 'r') as file:
                pkg_data = file.read()
            return pkg_data
        print('[ERROR] package file not found..')
        return None

# includes user generated testcases to
# the pakage file automatically
# returns the updated package file as a string
def add_testcases_to_package(package_string, testcases):
    endpackage_index = package_string.rfind('endpackage')
    if endpackage_index != -1:
        package_header = package_string[:endpackage_index]
        testcases_strings = [f'\t`include "{project}_{testcase}.sv"' for testcase in testcases]
        testcases_string = '\n'.join(testcases_strings)
        updated_package_string = f'{package_header[:-1]}\n{testcases_string}\nendpackage : {project}_package'
        return updated_package_string
    else:
        return package_string