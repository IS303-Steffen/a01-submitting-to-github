import inspect

# put the class to generate tests for here:

class Pokemon:
    # Initialize a new Pokemon object with name, type, hit points, offensive move name, and offensive move points
    def __init__(self, name, elemental_type, hit_points):
        self.name = name
        self.elemental_type = elemental_type
        self.hit_points = hit_points

    # Display information about the Pokemon
    def get_info(self):
        return f"{self.name} - Type: {self.elemental_type} - Hit Points: {self.hit_points}"
    
    # Heal the Pokemon by increasing its hit points
    def heal(self):
        self.hit_points += 15
        print(f"{self.name} has been healed to {self.hit_points} hit points.")


def generate_class_tests(cls):
    class_name = cls.__name__
    # Get __init__ parameters
    init_signature = inspect.signature(cls.__init__)
    init_params = list(init_signature.parameters.values())
    # Exclude 'self'
    init_params = [p for p in init_params if p.name != 'self']
    # Prompt the user for init_args
    init_args = []
    print(f"Generating tests for class '{class_name}'")
    print("Provide initialization arguments:")
    for param in init_params:
        default = param.default if param.default != inspect.Parameter.empty else 'No default'
        value = input(f"Value for '{param.name}' (default: {default}): ")
        if value == '':
            if param.default != inspect.Parameter.empty:
                init_args.append(param.default)
            else:
                init_args.append(None)
        else:
            # Try to evaluate the input
            try:
                evaluated_value = eval(value)
            except:
                evaluated_value = value
            init_args.append(evaluated_value)
    # Build the methods dict
    methods = {}
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name == '__init__':
            continue
        method_signature = inspect.signature(method)
        method_params = list(method_signature.parameters.values())
        # Exclude 'self'
        method_params = [p for p in method_params if p.name != 'self']
        # For each method, prompt the user for test cases
        print(f"\nProvide test cases for method '{name}'")
        test_cases = []
        while True:
            print(f"Enter arguments for method '{name}' (or press Enter to finish):")
            args = []
            for param in method_params:
                default = param.default if param.default != inspect.Parameter.empty else 'No default'
                value = input(f"Value for '{param.name}' (default: {default}): ")
                if value == '':
                    if param.default != inspect.Parameter.empty:
                        args.append(param.default)
                    else:
                        args.append(None)
                else:
                    # Try to evaluate the input
                    try:
                        evaluated_value = eval(value)
                    except:
                        evaluated_value = value
                    args.append(evaluated_value)
            if args == []:
                break
            # Try to call the method and get expected output
            try:
                obj = cls(*init_args)
                actual_output = getattr(obj, name)(*args)
                print(f"Expected output: {actual_output}")
            except Exception as e:
                print(f"Error calling method: {e}")
                actual_output = None
            test_cases.append({'args': args, 'expected': actual_output})
            cont = input("Add another test case for this method? (y/n): ")
            if cont.lower() != 'y':
                break
        methods[name] = test_cases
    class_tests = {
        class_name: {
            'init_args': init_args,
            'methods': methods
        }
    }
    return class_tests




tests = generate_class_tests(Pokemon)
print("\nGenerated class_tests dictionary:")
print(tests)