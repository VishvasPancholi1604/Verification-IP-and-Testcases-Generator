# Verification-IP-and-Testcases-Generator

This Python script facilitates the creation of a Verification IP (VIP) or UVC (Universal Verification Component) for various architectures. The script currently supports two modes: VIP Generator and Testcase Generator.

## VIP Generator

### Usage

The default mode of the script is the VIP Generator. It prompts the user to enter the project name and select components from the following list:

- transaction
- sequence
- sequencer
- driver
- monitor
- agent
- scoreboard
- subscriber
- reference_model
- environment
- base_test
- interface

#### Environment Support

Users can create multiple environments by using the `-e` command line argument. If provided, the script will prompt the user to enter the names of the environments, and for each environment, the names and types of agents.

- Active (creates sequencer, driver, and monitor files in the agent)
- Passive (creates only a monitor file in the agent)
- Noseqe (creates driver and monitor files without a sequencer)

If the `-e` command line argument is not used, a single environment will be created in the testbench, and users can create any number of agents within it.

### Directory Structure

The script automatically organizes files into the following structure:

```
.
└── project_name/
    └── DEVELOPMENT/
        ├── ENV/
        │   └── environment_files.sv
        ├── RTL/
        │   └── dut_folder_if_required_by_user
        ├── SIM/
        │   └── compilation_and_simulation_script.py
        ├── SRC/
        │   ├── transaction_files.sv
        │   ├── sequence_files.sv
        │   ├── sequencer_files.sv
        │   ├── driver_files.sv
        │   ├── monitor_files.sv
        │   ├── agent_files.sv
        │   ├── package_file.sv
        │   └── interface_file.sv
        ├── TEST/
        │   ├── base_test_file.sv
        │   └── testcases_files.sv
        └── TOP/
            └── top_module.sv
```

The script also generates a VIP compilation and simulation Python script in the SIM directory.

## Testcase Generator

### Usage

To use the Testcase Generator mode, use the `-t` switch and run the script from the SIM directory.

The script will prompt the user to enter testcase names separated by commas. Each generated testcase file will follow the format: `prefix + project name + testcase name + '_test' + '.sv'`. The class name within the file will be `prefix + project name + testcase name + '_test_c'`.

The script ignores the prefix, project name, and the '_test' suffix if they are already present in the user-provided testcase names to prevent duplication.

All testcases are extended from the base test class, eliminating the need to recreate environment components for each testcase.

### Example

If the prefix is 'ei_' and the project name is 'axi4', the generated file name for a testcase named 'single_write' will be `ei_axi4_single_write_test.sv`, and the class name will be `ei_axi4_single_write_test_c`.
