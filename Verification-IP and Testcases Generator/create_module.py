# importing dependancies
from globals import *

# returns `include string for each file
# used for including files in package
def create_includes(list_):
    include_str = ''
    for idx, name in enumerate(list_):
        tab = '' if idx == 0 else '\t'
        enter = '' if idx == len(list_) - 1 else '\n'
        include_str += f'{tab}`include "{project}_{name}.sv"{enter}'
    return include_str

# create package takes component list, object list and
# interface list to create a package file
def create_package(comp_list=[], obj_list=[], interface=[]):
    intf_str = ''
    for name in interface:
        intf_str += f'`include "{project}_{name}.sv"\n'
    package = f'''package {project}_package;
    import uvm_pkg::*;
    `include "uvm_macros.svh"
    {create_includes(obj_list)}
    {create_includes(comp_list)}
endpackage : {project}_package
'''
    return intf_str + package

# used for interface handele declaration in
# top module and setting up in configDB
def interface_decl(intf):
    comment = ''
    return_intf_handles = ''
    intf_set = ''
    if len(intf) > 0:
        comment = '\n\n\t//interface handle declaration'
        for idx, name in enumerate(intf):
            return_intf_handles += f'\n\t{project}_{name} pif{idx}();'
            intf_set += f'\n\t\tuvm_config_db#(virtual {project}_{name})::set(null, "*", "pif{idx}", pif{idx});'
        return comment + return_intf_handles + '\n', intf_set

# top module core function
# returns the content of top module in
# string format
def top_module(interface=[]):
    intf_handles, set_intf = interface_decl(interface)
    top = f'''{header(f'{project}_top.sv', 'top module', is_module=True)}

import uvm_pkg::*;
`include "uvm_macros.svh"

`include "{project}_package.sv"
import {project}_package::*;

module {project}_top;{intf_handles}
    initial
    begin{set_intf}
        run_test();
    end
endmodule
'''
    return top

# interface core function
# returns the content of interface in string format
def create_interface(name):
    interface = f'''{header(f'{project}_{name}.sv', name, is_module=True)}

interface {project}_{name};
endinterface : {project}_{name}
'''
    return interface