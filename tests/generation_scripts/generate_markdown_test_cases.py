import json
import os

# Load the JSON data
json_file = 'tests/test_cases/input_test_cases_final.json'
output_folder = "tests/generation_scripts"
output_file = 'markdown_generated.md'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the JSON content
with open(json_file, "r") as file:
    test_cases = json.load(file)

# Start the Markdown content
markdown_content = """## Test Cases
If you fail a test during a specific test case, see the `descriptions_of_test_cases` folder for the following:
<table border="1" style="width: 100%; text-align: left;">
  <tr>
    <th>Test Case</th>
    <th>Description</th>
  </tr>
"""

# Add rows for each test case
for idx, test_case in enumerate(test_cases, start=1):
    test_id = f"Input Test Case {idx:02d}"
    description = test_case.get("input_test_case_description", "No description available.")
    markdown_content += f"  <tr>\n    <td>{test_id}</td>\n    <td>{description}</td>\n  </tr>\n"

# Close the table
markdown_content += "</table>"

# Write the Markdown content to the file
output_path = os.path.join(output_folder, output_file)
with open(output_path, "w") as md_file:
    md_file.write(markdown_content)

print(f"Summary Markdown file has been successfully created at '{output_path}'.")