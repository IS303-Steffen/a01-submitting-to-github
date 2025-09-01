from datetime import date, timedelta
from typing import Any, Optional

# ======================
# METHOD TEST CASE CLASS
# ======================

class MethodTestCase:
    def __init__(self, function_name: str, args: list, expected_return_value: Any,
                 expected_object_update: Optional[dict] = None, set_var_values: Optional[dict] = None, num_calls: int = 1):
        self.function_name = function_name
        self.args = args
        self.expected_return_value = expected_return_value
        self.expected_object_update = expected_object_update
        self.set_var_values = set_var_values
        self.num_calls = num_calls

    def to_dict(self):
        return {
            "function_name": self.function_name,
            "args": self.args,
            "expected_return_value": self.expected_return_value,
            "expected_object_update": self.expected_object_update,
            "set_var_values": self.set_var_values,
            "num_calls": self.num_calls
        }
    
# ======================
# CLASS TEST CASE CLASS
# ======================

class ClassTestCase:
    def __init__(self, class_name, init_args, init_expected_values, expected_function_names, method_test_cases):
        self.class_name = class_name
        self.init_args = init_args
        self.init_expected_values = init_expected_values
        self.expected_function_names = expected_function_names
        self.method_test_cases = [m.to_dict() for m in method_test_cases]

    def to_dict(self):
        return {
            "class_name": self.class_name,
            "init_args": self.init_args,
            "init_expected_values": self.init_expected_values,
            "expected_function_names": self.expected_function_names,
            "method_test_cases": self.method_test_cases
        }

    @classmethod
    def from_dict(cls, data):
        method_test_cases = [MethodTestCase(**m) for m in data["method_test_cases"]]
        return cls(
            class_name=data["class_name"],
            init_args=data["init_args"],
            init_expected_values=data["init_expected_values"],
            expected_function_names=data["expected_function_names"],
            method_test_cases=method_test_cases
        )
    
# ==============================
# CREATE TEST CASE OBJECTS BELOW
# ==============================
'''
MethodTestCase objects should be created first, then placed inside of ClassTestCase
objects in their method_test_cases attribute
'''

# ========================
# METHOD TEST CASE OBJECTS
# ========================

# Creating MethodTestCase objects for the 'SoccerTeam' class test cases
soccer_team_record_win = MethodTestCase(
    function_name='record_win',
    args=[],
    expected_return_value=None,
    expected_object_update={
        '_SoccerTeam__wins':{
            'initial_value': 0,
            'final_value': 1
        }
    }
)

soccer_team_record_loss = MethodTestCase(
    function_name='record_loss',
    args=[],
    expected_return_value=None,
    expected_object_update={
        '_SoccerTeam__losses':{
            'initial_value': 0,
            'final_value': 1
        }
    }
)

soccer_team_get_record_percentage_zero_games = MethodTestCase(
    function_name='get_record_percentage',
    args=[],
    expected_return_value=0,
    expected_object_update=None
)

soccer_team_get_record_percentage_67_percent = MethodTestCase(
    function_name='get_record_percentage',
    args=[],
    expected_return_value=0.67,
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 2,
        '_SoccerTeam__losses': 1,
    }
)

soccer_team_generate_score = MethodTestCase(
    function_name='generate_score',
    args=[],
    expected_return_value=(0,3),
    expected_object_update=None,
    set_var_values=None,
    num_calls=100
)

soccer_team_get_season_low = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='Your team needs to practice!',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 0,
        '_SoccerTeam__losses': 4,
    },
    num_calls=1
)

soccer_team_get_season_mid = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='You had a good season.',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 2,
        '_SoccerTeam__losses': 2,
    },
    num_calls=1
)

soccer_team_get_season_high = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='Qualified for the NCAA Soccer Tournament!',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 6,
        '_SoccerTeam__losses': 2,
    },
    num_calls=1
)

sponsored_team_generate_score = MethodTestCase(
    function_name='generate_score',
    args=[],
    expected_return_value=(1,3),
    expected_object_update=None,
    set_var_values=None,
    num_calls=100
)

sponsored_team_get_season_low = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='Your team needs to practice! You are in danger of Cosmo dropping you.',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 0,
        '_SoccerTeam__losses': 4,
    },
    num_calls=1
)

sponsored_team_get_season_mid = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='You had a good season. Cosmo hopes you can do better.',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 2,
        '_SoccerTeam__losses': 2,
    },
    num_calls=1
)

sponsored_team_get_season_high = MethodTestCase(
    function_name='get_season_message',
    args=[],
    expected_return_value='Qualified for the NCAA Soccer Tournament! Cosmo is very happy.',
    expected_object_update=None,
    set_var_values={
        '_SoccerTeam__wins': 6,
        '_SoccerTeam__losses': 2,
    },
    num_calls=1
)

game_play_game = MethodTestCase(
    function_name='play_game',
    args=[],
    expected_return_value=None,
    expected_object_update=None,
    num_calls=1
)

# =======================
# CLASS TEST CASE OBJECTS
# =======================

UVU_soccer_team = ClassTestCase(
    class_name='SoccerTeam',
    init_args={
        'team_number': 1,
        'team_name': 'UVU',
    },
    init_expected_values={
        'team_number': 1,
        'team_name': 'UVU',
        '_SoccerTeam__wins': 0,
        '_SoccerTeam__losses': 0,
        'goals_scored': 0,
        'goals_allowed': 0
    },
    expected_function_names=['record_win', 'record_loss', 'get_record_percentage', 'get_team_info', 'generate_score', 'get_season_message'],
    method_test_cases=[soccer_team_record_win,
                       soccer_team_record_loss,
                       soccer_team_get_record_percentage_zero_games,
                       soccer_team_get_record_percentage_67_percent,
                       soccer_team_generate_score,
                       soccer_team_get_season_low,
                       soccer_team_get_season_mid,
                       soccer_team_get_season_high,
    ]
)

BYU_sponsored_team = ClassTestCase(
    class_name='SponsoredTeam',
    init_args={
        'team_number': 2,
        'team_name': 'BYU',
        'sponsor_name': 'Cosmo'
    },
    init_expected_values={
        'team_number': 2,
        'team_name': 'BYU',
        'sponsor_name': 'Cosmo',
        '_SoccerTeam__wins': 0,
        '_SoccerTeam__losses': 0,
        'goals_scored': 0,
        'goals_allowed': 0
    },
    expected_function_names=['record_win', 'record_loss', 'get_record_percentage', 'get_team_info', 'generate_score', 'get_season_message'],
    method_test_cases=[sponsored_team_generate_score,
                       sponsored_team_get_season_low,
                       sponsored_team_get_season_mid,
                       sponsored_team_get_season_high,
    ]
)

game_1 = ClassTestCase(
    class_name='Game',
    init_args={
        'game_number': 1,
        'home_team': {'class_name': 'SoccerTeam', 'init_args': [1, 'UVU']},
        'away_team': {'class_name': 'SponsoredTeam', 'init_args': [2, 'BYU', 'Cosmo']}
    },
    init_expected_values={
        'game_number': 1,
        'game_date': date.today() + timedelta(days=1),
        'home_team': {'team_number': 1, 'team_name': 'UVU', '_SoccerTeam__wins': 0, '_SoccerTeam__losses': 0, 'goals_scored': 0, 'goals_allowed': 0},
        'away_team': {'team_number': 2, 'team_name': 'BYU', 'sponsor_name': 'Cosmo', '_SoccerTeam__wins': 0, '_SoccerTeam__losses': 0, 'goals_scored': 0, 'goals_allowed': 0},
        'home_team_score': 0,
        'away_team_score': 0
    },
    expected_function_names=['get_game_status', 'play_game'],
    method_test_cases=[game_play_game]
)

# Update the list of test cases
test_cases_classes_list = [UVU_soccer_team, BYU_sponsored_team, game_1]

test_cases_classes_list = [class_test_case.to_dict() for class_test_case in test_cases_classes_list]
unique_class_names = {class_name.get('class_name') for class_name in test_cases_classes_list}

test_cases_classes_dict = {}
for class_name in unique_class_names:
    subset_test_cases_classes = [test_case_class for test_case_class in test_cases_classes_list if test_case_class.get('class_name') == class_name]
    test_cases_classes_dict[class_name] = subset_test_cases_classes
