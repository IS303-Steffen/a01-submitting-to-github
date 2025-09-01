max_score = 5 # This value is pulled by yml_generator.py to assign a score to this test.
import re
from conftest import default_module_to_test, format_error_message, exception_message_for_students

def test_03_sufficient_comments(current_test_name):
    try:
        required_num_comments = 3
        num_comments = 0
        modules_to_open = [default_module_to_test]

        # Regex to match single-line comments (#) and multi-line comments (''' ''' or """ """)
        # . is any character except new line
        # * means 0 or many occurrences of the previous character
        # \s means spaces \S is any non-space character, meaning it gets everything including new lines
        # *? is a non-greedy match
        comment_pattern = r"(#.*)|('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"

        for module in modules_to_open:
            # Open and read the student's script as a string
            with open(f"{module}.py", "r") as file:
                script_content = file.read()

            # Find all matches for comments
            comments = re.findall(comment_pattern, script_content)

            # Count total number of comments
            num_comments += len(comments)

        # Ensure there are at least X comments
        assert num_comments >= required_num_comments,format_error_message(
            custom_message=f"Not enough comments found. You need at least {required_num_comments}. "
                           f"Only {num_comments} comment(s) detected.",
            current_test_name=current_test_name,
            input_test_case= None)
    
    except AssertionError:
        raise
    
    except Exception as e:
        input_test_case = None
        exception_message_for_students(e, input_test_case, current_test_name)