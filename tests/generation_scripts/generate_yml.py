import os
import ast
from ruamel.yaml import YAML

def generate_classroom_yml(python_version='3.12.6'):
    # Initialize ruamel.yaml YAML instance
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 1000  # Prevent line breaks in long strings

    # Define the structure of the YAML file using regular dictionaries
    data = {}
    data['name'] = 'Autograding Tests'
    data['on'] = ['push', 'repository_dispatch']
    data['permissions'] = {
        'checks': 'write',
        'actions': 'read',
        'contents': 'read'
    }
    data['jobs'] = {}
    data['jobs']['run-autograding-tests'] = {}
    job = data['jobs']['run-autograding-tests']
    job['runs-on'] = 'ubuntu-latest'
    job['if'] = "github.actor != 'github-classroom[bot]' && github.actor != 'jacobsteffenBYU'"
    job['steps'] = []

    # Add initial steps
    job['steps'].append({
        'name': 'Checkout code',
        'uses': 'actions/checkout@v4'
    })
    job['steps'].append({
        'name': 'Set up Python',
        'uses': 'actions/setup-python@v3',
        'with': {'python-version': python_version}
    })

    # Add install dependencies step
    job['steps'].append({
        'name': 'Install dependencies',
        'run': 'python -m pip install --upgrade pip && pip install pandas openpyxl peewee pytest pytest-subtests \'black<=22.3.0\' \'tomli>=1.1.0\' \'timeout-decorator~=0.5.0\''
    })

    # Add test steps dynamically based on the test_*.py files in the tests/ folder
    test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]

    # Sort the test files by the number in the filename to ensure they are in order
    test_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    test_names = []
    for test_file in test_files:
        test_name = test_file.replace('.py', '').replace('_', '-')
        test_names.append(test_name)
        
        # Get max-score from the test file
        test_file_path = os.path.join('tests', test_file)
        max_score = get_max_score_from_test(test_file_path)
        
        # Use autograding-command-grader instead of autograding-python-grader
        job['steps'].append({
            'name': f'tests/{test_file}',
            'id': f'tests-{test_name}-py',
            'uses': 'classroom-resources/autograding-command-grader@v1',
            'with': {
                'test-name': f'{test_name}',
                'setup-command': '',
                'command': f'python -m pytest -v tests/{test_file}',
                'timeout': 30,
                'max-score': max_score
            }
        })

    # Add the reporter step with environment variables and the runners key
    env_vars = {}
    for test_name in test_names:
        env_var_name = f'TESTS-{test_name.upper()}-PY_RESULTS'
        env_vars[env_var_name] = f"${{{{steps.tests-{test_name}-py.outputs.result}}}}"

    runners = ','.join([f'tests-{test_name}-py' for test_name in test_names])

    job['steps'].append({
        'name': 'Autograding Reporter',
        'uses': 'classroom-resources/autograding-grading-reporter@v1',
        'env': env_vars,
        'with': {
            'runners': runners
        }
    })

    # Ensure the .github/workflows directory exists
    os.makedirs('.github/workflows', exist_ok=True)

    # Write the YAML data to the classroom.yml file
    with open('.github/workflows/classroom.yml', 'w') as file:
        yaml.dump(data, file)


def get_max_score_from_test(file_path):
    # Parse the test file to find the max_score variable
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'max_score':
                        # Check if the value is a constant (Python 3.8+ uses ast.Constant for literals)
                        if isinstance(node.value, ast.Constant):
                            return node.value.value  # Use the 'value' attribute of ast.Constant
                        elif isinstance(node.value, ast.Num):  # For compatibility with older Python versions
                            return node.value.n  # Extract and return max_score value
    return 10  # Default max score if not specified

if __name__ == '__main__':
    # Call the function with a default or custom Python version
    generate_classroom_yml()