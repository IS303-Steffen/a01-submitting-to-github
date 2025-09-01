from datetime import date, timedelta
from typing import Any, Optional

# ========================
# FUNCTION TEST CASE CLASS
# ========================

class FunctionTestCase:
    def __init__(self, function_name: str, args: list, expected_return_value: Any,
                 set_var_values: Optional[dict] = None, num_calls: int = 1):
        self.function_name = function_name
        self.args = args
        self.expected_return_value = expected_return_value
        self.set_var_values = set_var_values
        self.num_calls = num_calls

    def to_dict(self):
        return {
            "function_name": self.function_name,
            "args": self.args,
            "expected_return_value": self.expected_return_value,
            "set_var_values": self.set_var_values,
            "num_calls": self.num_calls
        }
    
# ===============================
# CREATE FUNCTION TEST CASES HERE
# ===============================

# ===============
# welcome_message
# ===============

welcome_message_diego = FunctionTestCase(
    function_name='welcome_message',
    args=['Diego'],
    expected_return_value=None,
)

welcome_message_mai = FunctionTestCase(
    function_name='welcome_message',
    args=['Mai'],
    expected_return_value=None,
)

# ===============
# sum_two_numbers
# ===============

sum_two_numbers_1 = FunctionTestCase(
    function_name='sum_two_numbers',
    args=[1, 1],
    expected_return_value=2,
)

sum_two_numbers_2 = FunctionTestCase(
    function_name='sum_two_numbers',
    args=[-3, 7],
    expected_return_value=4,
)

sum_two_numbers_3 = FunctionTestCase(
    function_name='sum_two_numbers',
    args=[2000, 42],
    expected_return_value=2042,
)

# =======
# is_even
# =======

is_even_1 = FunctionTestCase(
    function_name='is_even',
    args=[1],
    expected_return_value=False,
)

is_even_2 = FunctionTestCase(
    function_name='is_even',
    args=[-3],
    expected_return_value=False,
)

is_even_3 = FunctionTestCase(
    function_name='is_even',
    args=[64],
    expected_return_value=True,
)

# =================
# get_number_parity
# =================

get_number_parity_1 = FunctionTestCase(
    function_name='get_number_parity',
    args=[1],
    expected_return_value="1 is odd.",
)

get_number_parity_2 = FunctionTestCase(
    function_name='get_number_parity',
    args=[-3],
    expected_return_value="-3 is odd.",
)

get_number_parity_3 = FunctionTestCase(
    function_name='get_number_parity',
    args=[64],
    expected_return_value="64 is even.",
)

# =====================
# fahrenheit_to_celsius
# =====================

fahrenheit_to_celsius_1 = FunctionTestCase(
    function_name='fahrenheit_to_celsius',
    args=[32],
    expected_return_value=0,
)

fahrenheit_to_celsius_2 = FunctionTestCase(
    function_name='fahrenheit_to_celsius',
    args=[122],
    expected_return_value=50,
)

fahrenheit_to_celsius_3 = FunctionTestCase(
    function_name='fahrenheit_to_celsius',
    args=[-13],
    expected_return_value=-25,
)

# ============
# min_max_mean
# ============

min_max_mean_1 = FunctionTestCase(
    function_name='min_max_mean',
    args=[[1,2,3]],
    expected_return_value=[1, 3, 2.0],
)

min_max_mean_2 = FunctionTestCase(
    function_name='min_max_mean',
    args=[[354, 87, -7, 92, 34]],
    expected_return_value=[-7, 354, 112.0],
)

# ===========
# dog_message
# ===========

dog_message_1 = FunctionTestCase(
    function_name='dog_message',
    args=["Jet"],
    expected_return_value="I am a dog named Jet and I'm 0 years old!",
)

dog_message_2 = FunctionTestCase(
    function_name='dog_message',
    args=["Poof", 92],
    expected_return_value="I am a dog named Poof and I'm 92 years old!",
)

# ============
# classify_age
# ============

classify_age_1 = FunctionTestCase(
    function_name='classify_age',
    args=[18],
    expected_return_value="Adult",
)

classify_age_2 = FunctionTestCase(
    function_name='classify_age',
    args=[1, 78],
    expected_return_value="Minor",
)

classify_age_3 = FunctionTestCase(
    function_name='classify_age',
    args=[70],
    expected_return_value="Senior",
)

classify_age_4 = FunctionTestCase(
    function_name='classify_age',
    args=[70,75],
    expected_return_value="Adult",
)

# ===============
# calculate_total
# ===============

calculate_total_1 = FunctionTestCase(
    function_name='calculate_total',
    args=[10, 9, .3],
    expected_return_value=63,
)

calculate_total_2 = FunctionTestCase(
    function_name='calculate_total',
    args=[10, 11, .3],
    expected_return_value=74.8,
)

calculate_total_3 = FunctionTestCase(
    function_name='calculate_total',
    args=[10, 11, .3, 120],
    expected_return_value=77,
)

calculate_total_4 = FunctionTestCase(
    function_name='calculate_total',
    args=[10, 11, .3, 90, .5],
    expected_return_value=22,
)

# ========================
# CREATING OUTPUT VARIABLE
# ========================

# creating a dictionary that will be pulled in by conftest.py to be available to all tests:
# The result is a dictionary called "test_cases_functions_dict" that has the name of each individual
# function as keys, with a list of test case data (arguments, expected return values) for each function.

# add each test case object to this list.
test_cases_functions_list = [
    welcome_message_diego,
    welcome_message_mai,
    sum_two_numbers_1,
    sum_two_numbers_2,
    sum_two_numbers_3,
    is_even_1,
    is_even_2,
    is_even_3,
    get_number_parity_1,
    get_number_parity_2,
    get_number_parity_3,
    fahrenheit_to_celsius_1,
    fahrenheit_to_celsius_2,
    fahrenheit_to_celsius_3,
    min_max_mean_1,
    min_max_mean_2,
    dog_message_1,
    dog_message_2,
    classify_age_1,
    classify_age_2,
    classify_age_3,
    classify_age_4,
    calculate_total_1,
    calculate_total_2,
    calculate_total_3,
    calculate_total_4,
]

test_cases_functions_list = [function_test_case.to_dict() for function_test_case in test_cases_functions_list]
unique_function_names = {function_name.get('function_name') for function_name in test_cases_functions_list}

test_cases_functions_dict = {}
for function_name in unique_function_names:
    subset_test_cases_function = [test_case_function for test_case_function in test_cases_functions_list if test_case_function.get('function_name') == function_name]
    test_cases_functions_dict[function_name] = subset_test_cases_function


