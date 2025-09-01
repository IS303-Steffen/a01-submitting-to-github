import json
import os

# Load the JSON data
json_file = r"tests/test_cases/input_test_cases_final.json"
output_folder = r"descriptions_of_test_cases"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the JSON content
with open(json_file, "r") as file:
    test_cases = json.load(file)

# Generate Markdown files
for idx, test_case in enumerate(test_cases, start=1):
    file_name = f"input_test_case_{idx:02d}.md"
    file_path = os.path.join(output_folder, file_name)
    
    # Extract data for the Markdown file
    test_id = test_case.get("id_input_test_case", "N/A")
    description = test_case.get("input_test_case_description", "N/A")

    inputs = test_case.get("inputs", [])
    inputs = [f'{index}: "{input}"' for index, input in enumerate(inputs, start=1)]
    inputs = '\n'.join(inputs)

    input_prompts = test_case.get("input_prompts", [])
    input_prompts = [f'{index}: "{input_prompt.replace('\n', '').replace('\t','')}"' for index, input_prompt in enumerate(input_prompts, start=1) if not input_prompt.isspace() and input_prompt != '']
    input_prompts = '\n'.join(input_prompts)

    printed_messages = test_case.get("printed_messages", [])
    printed_messages = [f'{index}: "{printed_message.replace('\n', '').replace('\t','')}"' for index, printed_message in enumerate(printed_messages, start=1) if not printed_message.isspace() and printed_message != '']
    printed_messages = '\n'.join(printed_messages)

    example_output = test_case.get("example_output", "N/A")
    
    # Create the Markdown content
    markdown_content = f"""# Test Case {test_id}

## Description
{description}

## Inputs
The inputs below (without the quotes) will be entered one by one each time an `input()` function is found in your code.
```
{inputs if inputs else "No inputs used in this test case"}
```

## Example Output
This is what your terminal should look like if you use the inputs above when running your code.
```
{example_output.strip() if example_output else "No output found"}
```
"""

    # Write the content to the Markdown file
    with open(file_path, "w") as md_file:
        md_file.write(markdown_content)

print(f"Markdown files have been successfully created in the '{output_folder}' folder.")




'''
If I want to put these sections back in, reference the below. I'm taking them out just to simplify the file for
students.


## Expected Input Prompts
```
{input_prompts if input_prompts else "No input prompts used in this test case"}
```

## Expected Printed Messages
```
{printed_messages if printed_messages else "No printed messaged in this test case"}
```





'''