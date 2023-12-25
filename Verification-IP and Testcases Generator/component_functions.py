# importing dependancies
from globals import *

# returns short name of the handle by
# looking up in the dictionary with '_h' suffix
def return_handle_name(handle_name=''):
    for key in handle_short_name:
        if key in handle_name:
            if handle_name[:-len(key)] != '':
                handle = f'{handle_name[:-len(key)]}_{handle_short_name[key]}_h'.replace('__', '_')
            else:
                handle = handle_short_name[key] + '_h'
            return handle
    return handle_name + '_h'

# used for handles declarations in
# the class defination
def extract_handles(handles=''):
    if handles != '':
        handles = handles.replace(' ', '').split(',')
        handle_list = []
        if len(handles) > 0:
            for name in handles:
                class_name = f'{project}_{name}_c'
                handle_list.append(f'\t{class_name} {return_handle_name(name)};\n')
            comment = '\n\t// handles declaration\n'
        return comment + ''.join(handle_list)
    else:
        return ''

# used for declaration of create method
# in the build phase of class declaration
def build_by_handles(handles=''):
    if handles != '':
        handles = handles.replace(' ', '').split(',')
        handle_list = []
        for name in handles:
            class_name = f'{project}_{name}_c'
            handle_list.append(
                f'\t{return_handle_name(name)} = {class_name}::type_id::create(\"{return_handle_name(name)}\", this);\n')
        return '\n' + ''.join(handle_list)[:-1]
    else:
        return ''

# returns the index of string from list
def return_string_index(my_list, search_string):
    for i, item in enumerate(my_list):
        if search_string in item:
            return i
    return False

# sequencer driver connection
# pseudo-intelligent function which
# knows (kind of;)) which sequencer needs
# to be connected with which driver
def connect_by_handles(handles=''):
    handles = handles.replace(' ', '').split(',')
    driver_idx = return_string_index(handles, 'driver')
    seqr_idx = return_string_index(handles, 'sequencer')

    if ((type(driver_idx) != int) or (type(seqr_idx) != int)):
        return ''
    else:
        return f'\n\t{return_handle_name(handles[driver_idx])}.seq_item_port.connect({return_handle_name(handles[seqr_idx])}.seq_item_export);'

# component skeleton core
# returns a fully created component in the
# form of string by taking two arguments
# cmponent name and handles to be created
def create_component(comp_name, handles=''):
    component = f"""{header(f'{project}_{comp_name}.sv', comp_name)}

class {project}_{comp_name}_c extends {lookup_for_comp_type(comp_name)};
    `uvm_component_utils({project}_{comp_name}_c)    
{extract_handles(handles)}
    // component constructor
    extern function new(string str = "", uvm_component parent);

    // component build phase
    extern virtual function void build_phase(uvm_phase phase);

    // component connect phase
    extern virtual function void connect_phase(uvm_phase phase);    

    // component run phase
    extern virtual task run_phase(uvm_phase phase); 
endclass : {project}_{comp_name}_c

{comment('new()', 'string and handle of parent class', 'none', 'component constructor')}
function {project}_{comp_name}_c::new(string str = "", uvm_component parent);
    super.new(str, parent);
endfunction : new

{comment('build_phase()', 'handle of class uvm_phase', 'none', 'for building components')}
function void {project}_{comp_name}_c::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_type_name(), "build phase", {verbosity}){build_by_handles(handles)}
endfunction : build_phase

{comment('connect_phase()', 'handle of class uvm_phase', 'none', 'for connecting components')}
function void {project}_{comp_name}_c::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    `uvm_info(get_type_name(), "connect phase", {verbosity}){connect_by_handles(handles)}
endfunction : connect_phase

{comment('run_phase()', 'handle of class uvm_phase', 'none', 'post build/connect phase')}
task {project}_{comp_name}_c::run_phase(uvm_phase phase);
    super.run_phase(phase);
    `uvm_info(get_type_name(), "run phase", {verbosity})
endtask : run_phase
"""
    return component

# base test skeleton core
# returns a fully created base test in the
# form of string by taking two arguments
# cmponent name and handles to be created
def create_test(testname='base_test', handles=''):
    extend_type = 'uvm_test' if 'base_test' in testname else f'{project}_base_test_c'
    test = f'''{header(f'{project}_{testname}', testname)}

class {project}_{testname}_c extends {extend_type};
    `uvm_component_utils({project}_{testname}_c)    
{extract_handles(handles)}
    // test constructor
    extern function new(string str = "", uvm_component parent);

    // test build phase
    extern virtual function void build_phase(uvm_phase phase);

    // test end of elaboration phase
    extern virtual function void end_of_elaboration_phase(uvm_phase phase);

    // test run phase
    extern virtual task run_phase(uvm_phase phase); 
endclass : {project}_{testname}_c

{comment('new()', 'string and handle of parent class', 'none', 'test constructor')}
function {project}_{testname}_c::new(string str = "", uvm_component parent);
    super.new(str, parent);
endfunction : new

{comment('build_phase()', 'handle of class uvm_phase', 'none', 'for building components')}
function void {project}_{testname}_c::build_phase(uvm_phase phase);
    super.build_phase(phase);
    `uvm_info(get_type_name(), "build phase", {verbosity}){build_by_handles(handles)}
endfunction : build_phase

{comment('end_of_elaboration_phase()', 'handle of class uvm_phase', 'none', 'for printing hierarchy')}
function void {project}_{testname}_c::end_of_elaboration_phase(uvm_phase phase);
    `uvm_info(get_type_name(), $sformatf("end of elaboration phase\\n%s", sprint()), {verbosity})
endfunction : end_of_elaboration_phase

{comment('run_phase()', 'handle of class uvm_phase', 'none', 'post build/connect phase')}
task {project}_{testname}_c::run_phase(uvm_phase phase);
    super.run_phase(phase);
    `uvm_info(get_type_name(), "run phase", {verbosity})
endtask : run_phase
'''
    return test

# testclass skeleton core
# returns a fully created testclass in the
# form of string extended from base test
# only takes one argument, testcase name.
def create_testclass(testname):
    extend_type = f'{project}_base_test_c'
    test = f'''{header(f'{project}_{testname}', testname)}

class {project}_{testname}_c extends {extend_type};
    `uvm_component_utils({project}_{testname}_c)    
    
    // testclass constructor
    extern function new(string str = "", uvm_component parent);

    // testclass build phase
    extern virtual function void build_phase(uvm_phase phase);
    
    // testclass run phase
    extern virtual task run_phase(uvm_phase phase); 
endclass : {project}_{testname}_c

{comment('new()', 'string and handle of parent class', 'none', 'test constructor')}
function {project}_{testname}_c::new(string str = "", uvm_component parent);
    super.new(str, parent);
endfunction : new

{comment('build_phase()', 'handle of class uvm_phase', 'none', 'for building components')}
function void {project}_{testname}_c::build_phase(uvm_phase phase);
    `uvm_info(get_type_name(), "build phase", {verbosity})
    super.build_phase(phase);
endfunction : build_phase

{comment('run_phase()', 'handle of class uvm_phase', 'none', 'post build/connect phase')}
task {project}_{testname}_c::run_phase(uvm_phase phase);
    `uvm_info(get_type_name(), "run phase", {verbosity})
    super.run_phase(phase);
endtask : run_phase
    '''
    return test