max_score = 30  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import (
    normalize_text,
    load_student_code,
    format_error_message,
    exception_message_for_students,
    round_match,
    get_similarity_feedback,
    clear_database,
    pc_get_or_create,
    pc_finalize_and_maybe_fail
)
import re

# Checks if the expected printed messages actually appear, but doesn't check for specific inputs or correct calculations.
def test_01_input_prompts(current_test_name, input_test_cases):
    # NEW: set up recorder for partial credit
    rec = pc_get_or_create(current_test_name, max_score)

    try:
        # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_input_test_case": None}
            exception_message_for_students(ValueError("input_test_cases should be a list of dictionaries. Contact your professor."), input_test_case=input_test_case) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        for input_test_case in input_test_cases:
            case_id = input_test_case["id_input_test_case"]
            inputs = input_test_case["inputs"]
            expected_input_prompts = input_test_case["input_prompts"]
            invalid_input_prompts = input_test_case["invalid_input_prompts"]

            # Load in the student's code and capture output
            manager_payload = load_student_code(current_test_name, inputs, input_test_case)
            
            if not manager_payload:
                continue # if there was an error in running student code, it's already been logged. Just skip to the next test case.

            captured_input_prompts = manager_payload.get('captured_input_prompts')

            # Normalize the captured input prompts to remove spaces, punctuation, and symbols
            normalized_captured_input_prompts_list = [normalize_text(captured_prompt) for captured_prompt in captured_input_prompts]
            normalized_captured_input_prompts_list = list(dict.fromkeys(normalized_captured_input_prompts_list)) # gets rid of duplicates
            error_message_input_prompts = [f'{index}: "{prompt}"' for index, prompt in enumerate(normalized_captured_input_prompts_list, start=1)  if not prompt.isspace() and prompt != '']
            error_message_input_prompts_str = '\n'.join(error_message_input_prompts)
            normalized_captured_input_prompts_str = '\n'.join(normalized_captured_input_prompts_list)

            case_failed_messages = []

            # Check that each required phrase (regex pattern) is found in the normalized captured output
            for expected_phrase in expected_input_prompts:
                expected_phrase = normalize_text(expected_phrase)
                regex_pattern = expected_phrase.replace("<wildcard>", r".+?")
                match = re.search(regex_pattern, normalized_captured_input_prompts_str)

                if not match:
                    similarity_message = get_similarity_feedback(expected_phrase, normalized_captured_input_prompts_list)

                    formatted = format_error_message(
                        custom_message=("The expected input prompt (ignoring punctuation and capitalization):\n"
                                        f"```\n\"{expected_phrase}\"\n```\n"
                                        f"wasn't found in your code as an input() prompt.\n\n"
                                        f"### How to fix it:\n"
                                        f"Likely, the error is from one of 3 causes:\n"
                                        f"1. You made a spelling error.\n"
                                        f"2. You forgot to include the expected input prompt.\n"
                                        f"3. The logic in your code makes the correct prompt not appear or makes it include incorrect content.\n\n"
                                        f"#### Possible spelling mistakes:\n"
                                        f"To help you rule out possible cause #1, below are prompts that appear in your code that are really close the the prompt you're missing.\n"
                                        f"```\n{similarity_message}\n```\n"
                                        f"#### All your input prompts:\n"
                                        f"Below are all the unique input prompts from when the test ran your code (ignoring punctuation and capitalization). Make sure you are including the needed prompt and spelling it correctly!:\n\n"
                                        f"```\n{error_message_input_prompts_str}\n```\n"),
                        current_test_name=current_test_name,
                        input_test_case=input_test_case,
                        display_inputs=True,
                    )
                    case_failed_messages.append(formatted)

            # Ensure none of the invalid phrases are found in the normalized captured output
            for invalid_phrase in invalid_input_prompts:
                invalid_phrase = normalize_text(invalid_phrase)
                regex_pattern = invalid_phrase.replace("<wildcard>", r".+?")
                match = re.search(regex_pattern, normalized_captured_input_prompts_str)

                if match:
                    formatted = format_error_message(
                        custom_message=("You used an invalid input() prompt (ignoring punctuation and capitalization):\n\n"
                                        f"```\"{invalid_phrase}\"\n```\n"
                                        f"### How to fix it:\n"
                                        f"Most likely:\n"
                                        f"1. You are asking for an input that should be inside an if statement or while loop, but isn't.\n"
                                        f"2. You are asking for an input that IS in an if statement or while loop, but you wrote the logic incorrectly so it appears when it shouldn't.\n"
                                        f"#### All your input prompts:\n"
                                        f"Below are all the unique input prompts from when the test ran your code (ignoring punctuation and capitalization). Make sure you aren't including the invalid prompt!:\n\n"
                                        f"```\n{error_message_input_prompts_str}\n```\n"),
                        current_test_name=current_test_name,
                        input_test_case=input_test_case,
                        display_inputs=True
                    )
                    case_failed_messages.append(formatted)

            # Record the case result
            if case_failed_messages:
                rec.fail_case(case_id, reason="input prompt mismatch", custom_message="\n\n".join(case_failed_messages))
            else:
                rec.pass_case(case_id)

    # assert raises an AssertionError, but I don't want to actually catch it
    # this is just so I can have another Exception catch below it in case
    # anything else goes wrong.
    except AssertionError:
        raise
    
    except Exception as e:
        # Handle other exceptions
        exception_message_for_students(e, input_test_case, current_test_name)
    finally:
        pc_finalize_and_maybe_fail(rec)