'''
DESCRIPTION:

Instead of manually writing out test cases, I opted to create this script
that will run my solution file and automatically store any inputs, printed
messages, and variables that are created during the run in a JSON file. Each
additional run will append the new data from that run in the JSON file.
'''
import builtins
import json
import os
import types
import sys
from datetime import date, datetime

# Name of the file that will be run to generate the test cases from:
solution_file_to_run = "a01_solution_submitting_to_github.py"
# Name of the JSON file that is created after running the script:
json_export_filename = r'input_test_cases_draft.json'

# List of data types to track
tracked_data_types = [
    bool,
    int,
    str,
    float,
    list,
    dict,
    # Custom classes will be handled dynamically, no need to list them here.
]

# Map data types to their corresponding key names
type_to_key = {
    bool: 'bools',
    int: 'ints',
    str: 'strings',
    float: 'floats',
    list: 'lists',
    dict: 'dicts',
    # Custom objects will have keys based on their class names
}

# Define the paths
CURRENT_DIR = os.path.dirname(__file__)
CURRENT_WORKING_DIR = os.getcwd()
CAPTURED_TEST_CASES_FILE = os.path.join(CURRENT_WORKING_DIR, 'tests', 'test_cases', json_export_filename)

# Initialize test_case_data
test_case_data = {}

# Save the original input and print functions
original_input = builtins.input
original_print = builtins.print


def safe_serialize(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    elif isinstance(value, (list, tuple)):
        return [safe_serialize(v) for v in value]
    elif isinstance(value, dict):
        return {safe_serialize(k): safe_serialize(v) for k, v in value.items()}
    elif hasattr(value, '__dict__'):
        return {
            '__class__': type(value).__name__,
            '__attributes__': safe_serialize(value.__dict__)
        }
    else:
        try:
            json.dumps(value)
            return value  # If serialization succeeds, return the value.
        except (TypeError, OverflowError, ValueError):
            # For other non-serializable objects, return a string representation
            return repr(value)

# Function to capture global variables at the end of execution
def capture_global_variables(test_case_id, new_global_vars):
    global test_case_data
    for var_name, value in new_global_vars.items():
        if (
            var_name.startswith("__") or
            callable(value) or
            isinstance(value, types.ModuleType)
        ):
            continue
        serialized_value = safe_serialize(value)
        # Determine the type key for the variable
        for data_type in tracked_data_types:
            if isinstance(value, data_type):
                type_key = type_to_key.get(data_type, 'others')
                test_case_data.setdefault(type_key, {})[var_name] = serialized_value
                break
        else:
            # For custom objects, use their class name as the key
            if isinstance(serialized_value, dict) and '__class__' in serialized_value:
                class_name = serialized_value['__class__']
                test_case_data.setdefault(class_name, {})[var_name] = serialized_value
            else:
                # Store other types under 'others'
                test_case_data.setdefault('others', {})[var_name] = serialized_value

# Function to remove duplicates from lists while preserving order
def remove_duplicates(lst):
    seen = set()
    new_lst = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            new_lst.append(item)
    return new_lst

# Function to save the test case data to a JSON file
def save_test_case(test_cases):
    global test_case_data

    # Append the new test case
    test_cases.append(test_case_data)

    # Build a set of all input prompts and printed messages across all test cases
    all_input_prompts = set()
    all_printed_messages = set()
    for tc in test_cases:
        all_input_prompts.update(tc.get("input_prompts", []))
        all_printed_messages.update(tc.get("printed_messages", []))

    # Now, for each test case, compute invalid_input_prompts and invalid_printed_messages
    for tc in test_cases:
        existing_input_prompts = set(tc.get("input_prompts", []))
        existing_printed_messages = set(tc.get("printed_messages", []))

        tc["invalid_input_prompts"] = list(all_input_prompts - existing_input_prompts)
        tc["invalid_printed_messages"] = list(all_printed_messages - existing_printed_messages)

        # Remove duplicates and sort if necessary
        tc["input_prompts"] = remove_duplicates(tc["input_prompts"])
        tc["printed_messages"] = remove_duplicates(tc["printed_messages"])
        tc["invalid_input_prompts"] = remove_duplicates(tc["invalid_input_prompts"])
        tc["invalid_printed_messages"] = remove_duplicates(tc["invalid_printed_messages"])

    # Save back to the JSON file
    with open(CAPTURED_TEST_CASES_FILE, 'w') as f:
        json.dump(test_cases, f, indent=4)

def run_and_capture(solution_file):
    global test_case_data
    # Re-initialize test_case_data
    test_case_data = {
        "id_input_test_case": None,
        "input_test_case_description": "",
        "inputs": [],
        "input_prompts": [],
        "printed_messages": [],
        "invalid_input_prompts": [],
        "invalid_printed_messages": []
    }
    # Initialize example_output as a list
    example_output = []

    # Initialize keys for the tracked data types
    for data_type in tracked_data_types:
        type_key = type_to_key.get(data_type, 'others')
        test_case_data[type_key] = {}

    # Define the wrapped input and print functions
    def input(prompt=""):
        nonlocal example_output
        global test_case_data
        # Get actual user input
        user_input = original_input(prompt)
        # Append prompt and user input together
        example_output.append(f"{prompt}{user_input}")
        # Capture the prompt
        test_case_data.setdefault("input_prompts", []).append(prompt)
        # Log the input
        test_case_data.setdefault("inputs", []).append(user_input)
        return user_input

    def print(*args, **kwargs):
        nonlocal example_output
        global test_case_data
        # Capture the printed messages
        message = " ".join(str(arg) for arg in args)
        test_case_data.setdefault("printed_messages", []).append(message)
        # Append message to example_output
        example_output.append(message)
        # Call the original print function
        original_print(*args, **kwargs)

    # Inject our input/print hooks into the global namespace
    builtins.input = input
    builtins.print = print

    # Capture existing global variables before execution
    pre_existing_globals = set(globals().keys())

    # Add the root directory to sys.path
    root_dir = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
    sys.path.append(root_dir)

    try:
        # Run the solution file
        solution_path = os.path.abspath(os.path.join(CURRENT_DIR, '../..', solution_file))
        with open(solution_path, 'r') as f:
            exec(f.read(), globals())
    finally:
        # Clean up the path change
        if root_dir in sys.path:
            sys.path.remove(root_dir)

    # Identify new global variables introduced by the solution file
    new_global_vars = {k: v for k, v in globals().items() if k not in pre_existing_globals}

    # Load existing test cases to assign id_test_case
    if os.path.exists(CAPTURED_TEST_CASES_FILE):
        with open(CAPTURED_TEST_CASES_FILE, 'r') as f:
            test_cases = json.load(f)
    else:
        test_cases = []

    # Assign id_test_case
    if test_cases:
        last_id = max(tc.get("id_input_test_case", 0) for tc in test_cases)
    else:
        last_id = 0
    test_case_data["id_input_test_case"] = last_id + 1
    test_case_id = test_case_data["id_input_test_case"]

    # Capture global variables at the end
    capture_global_variables(test_case_id, new_global_vars)

    # Restore original input and print functions before asking for description
    builtins.input = original_input
    builtins.print = original_print

    # Use original_input directly to avoid capturing this prompt
    description = original_input("Please provide a description for this input test case: ")
    test_case_data["input_test_case_description"] = description

    # Join example_output into a string and store it
    test_case_data["example_output"] = "\n".join(example_output)

    # Save the test case data to a JSON file
    save_test_case(test_cases)

    # Restore original input and print functions
    builtins.input = original_input
    builtins.print = original_print

if __name__ == '__main__':
    # Replace with the name of the file to collect test cases from
    run_and_capture(solution_file_to_run)
