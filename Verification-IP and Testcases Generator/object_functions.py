# importing dependancies
from globals import *

# object core function
# returns the content of object class
# in the string format
def create_object(obj_name=''):
    object = f"""{header(f'{project}_{obj_name}.sv', obj_name)}
class {project}_{obj_name}_c extends {lookup_for_comp_type(obj_name)};
    `uvm_object_utils({project}_{obj_name}_c)

    // object constructor
    extern function new(string str = "");
endclass : {project}_{obj_name}_c

{comment('new()', 'string and handle of parent class', 'none', 'component constructor')}
function {project}_{obj_name}_c::new(string str = "");
    super.new(str);
endfunction : new
"""
    return object