# importing required files
from globals import *
from component_functions import *
from select_components import *
from create_files import *
from run import create_run_file

# get current path
current_path = os.getcwd()

# decides the flow of the script
# -> VIP Generator Mode (default mode of script)
# -> Testcases Generator Mode (Have to be present in
# 'SIM' directory of given project folder and use '-t' cla.)
if args.testcases == False:
    testbench, objects, interface, prefix_list = ask_for_component_selection(args)
    comp_handles_dict = dict_recursion(comptree=testbench)
    create_from_dictionary(args, comp_handles_dict, testbench, objects, interface)
    project_path = os.path.join(current_path, project)
    dev_path = os.path.join(project_path, 'DEVELOPMENT')
    sim_path = os.path.join(dev_path, 'SIM')
    os.chdir(sim_path)
else:
    package_file = read_package_file()
    testcase_list = ask_for_testcases()
    print()
    test_path = current_path[:-len('SIM')] + 'TEST'
    src_path  = current_path[:-len('SIM')] + 'SRC'
    for name in testcase_list:
        file_name = f'{project}_{name}.sv'
        full_path = os.path.join(test_path, file_name)
        print(f'creating file : {project}_{name}.sv at {full_path}')
        with open(full_path, 'w') as file:
            file.write(create_testclass(name))
    package_file = add_testcases_to_package(package_file, testcase_list)
    full_path = os.path.join(src_path, f'{project}_package.sv')
    with open(full_path, 'w') as file:
        file.write(package_file)