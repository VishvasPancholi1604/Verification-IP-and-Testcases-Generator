# importing dependancies
from globals import *

# askes user for selecting the components
# returns a dictionary which contains the entire
# architecture of components to be created along with
# list of objects and interfaces
def ask_for_component_selection(args):
    print()
    print('Below are the list of components which can be created: ')
    print()
    for idx, name in enumerate(component_list):
        print(f'{idx+1}. {name}')
    selected_comp_idx = input(f'Enter the components to be created seperated by comma\n\n[Options : {component_selection_note}]\n>> ')
    selected_components = []
    if selected_comp_idx != '':
        if selected_comp_idx == 'all':
            selected_components = component_list
        else:
            if selected_comp_idx.startswith('!'):
                actual_idx_to_be_ignored = []
                selected_comp_idx = selected_comp_idx[1:].replace(' ', '').split(',')
                for idx in selected_comp_idx:
                    actual_idx_to_be_ignored.append(int(idx)-1)
                for id, name in enumerate(component_list):
                    if id not in actual_idx_to_be_ignored:
                        selected_components.append(name)
            else:
                actual_idx_to_be_created = []
                selected_comp_idx = selected_comp_idx.replace(' ', '').split(',')
                for idx in selected_comp_idx:
                    actual_idx_to_be_created.append(int(idx)-1)
                for id, name in enumerate(component_list):
                    if id in actual_idx_to_be_created:
                        selected_components.append(name)
    print()
    environments = []
    if 'environment' in selected_components:
        if args.environment == True:
            ask_for_env = input(f'Enter environment names to be created seperated by comma\n[NOTE : {environment_name_note}]\n>> ')
            if ask_for_env != '':
                environments = ask_for_env.replace(' ', '').split(',')
            else:
                environments.append('environment')
                print()
        else:
            environments.append('environment')
    objects = []
    interface = []
    prefix_list = []
    debug(environments)
    environments_dict = {}
    if len(environments) > 0:
        for name in environments:
            env_prefix = name[:-len('environment')] if name != 'environment' else ''
            if env_prefix != '':
                prefix_list.append(env_prefix)
            if 'interface' in selected_components:
                interface.append(f'{env_prefix}interface')
            if 'transaction' in selected_components:
                objects.append(f'{env_prefix}transaction')
            ask_for_agent = input(f'Enter agent names to be created for environment \'{name}\' seperated by comma \n[NOTE : {agent_name_note}]\n>> ')
            agents_dict = {}
            agent_name = f'{env_prefix}agent'
            if ask_for_agent != '':
                agents_name = [(f'{env_prefix}{item}') if env_prefix != None else item
                               for item in ask_for_agent.replace(' ', '').split(',')]
                print(f'\nEnter the agent type for each agents below\nNOTE : {agent_type_note}\n')
                for agent_name in agents_name:
                    handles = []
                    agent_prefix = agent_name[:-len("_agent")]
                    agent_type = input(f'Enter agent type for \'{agent_name}\': ')
                    if agent_type != '':
                        if agent_type == 'passive':
                            handles = [f'{agent_prefix}_monitor']
                        elif agent_type == 'active':
                            handles = [f'{agent_prefix}_sequencer', f'{agent_prefix}_driver' , f'{agent_prefix}_monitor']
                        elif agent_type == 'noseqr':
                            handles = [f'{agent_prefix}_driver' , f'{agent_prefix}_monitor']
                        else:
                            print('INVALID AGENT TYPE')
                            return
                    else:
                        handles = [f'{agent_prefix}_sequencer', f'{agent_prefix}_driver', f'{agent_prefix}_monitor']
                    agents_dict.update({agent_name : handles})
            else:
                agent_type = input(f'Enter agent type for \'{agent_name}\': ')
                handles = []
                if agent_type != '':
                    if agent_type == 'passive':
                        handles = [f'{env_prefix}monitor']
                    elif agent_type == 'active':
                        handles = [f'{env_prefix}sequencer', f'{env_prefix}driver', f'{env_prefix}monitor']
                    elif agent_type == 'noseqr':
                        handles = [f'{env_prefix}driver', f'{env_prefix}monitor']
                    else:
                        print('INVALID AGENT TYPE')
                        return
                agents_dict.update({name : {f'{env_prefix}agent' : handles}})
            if 'scoreboard' in selected_components:
                agents_dict.update({f'{env_prefix}scoreboard' : []})
            if 'subscriber' in selected_components:
                agents_dict.update({f'{env_prefix}subscriber' : []})
            if 'reference_model' in selected_components:
                agents_dict.update({f'{env_prefix}reference_model' : []})
            environments_dict.update({name : agents_dict})
    if 'sequence' in selected_components:
        objects.append('base_sequence')
    return environments_dict, objects, interface, prefix_list

# asks user to enter testcase names seperated by comma
# returns the list of testcase names along with proper formatting
# such as adding a suffix '_test'
def ask_for_testcases():
    #print()
    print('Enter testcase(s) names seperated by comma')
    print(f'[NOTE : \'{project}_\' will be appended to each testcase name by default '
          f'also \'_c\' will be appended\nat the end of class name as a suffix (not in the file name). '
          f'prefix \'{project}_\' and suffix \'_c\' will be\nignored if it\'s already present in user input string '
          f'It is advised to end testcase name with \'_test\'.]')
    testcases_list_string = input('\n>> ')
    if testcases_list_string != '':
        testcases_list = testcases_list_string.replace(' ', '').split(',')
        testcases_list = [(item.replace(project+'_', '')) for item in testcases_list]
        testcases_list = [(item.replace('_c', '')) for item in testcases_list]
        testcases_list = [(f'{item}_test' if '_test' not in item else item) for item in testcases_list]
        debug(testcases_list)
        return testcases_list
