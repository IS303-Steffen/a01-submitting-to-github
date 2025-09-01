list_of_test_cases = [
            # function test cases. Inputs in first position, expected output in second position.
            # If a function takes only a single input, be sure to include a comma after the value so that
            # python recognizes it as a tuple.
            [(18,), "Adult"],
            [(1, 78), "Minor"],
            [(70,), "Senior"],
            [(70,75), "Adult"],
            ]

# Generate HTML table
html_table = (f'<table border="1" style="width: 100%; text-align: center;">\n'
              f'\t<thead>\n'
              f'\t\t<tr>\n'
              f'\t\t\t<th style="text-align: center;">Arguments</th>\n'
              f'\t\t\t<th style="text-align: center;">Return Values</th>\n'
              f'\t\t</tr>\n'
              f'\t</thead>\n'
              f'\t<tbody>\n')

for test_case in list_of_test_cases:
    # Unpack the tuple of arguments and expected output
    arguments, return_value = test_case
    arguments_str = ', '.join(map(str, arguments))  # Convert tuple to comma-separated string
    html_table += (f'\t\t<tr>\n'
                   f'\t\t\t<td><code>{arguments_str}</code></td>\n'
                   f'\t\t\t<td><code>{return_value}</code></td>\n'
                   f'\t\t</tr>\n')

# Closing the table tag
html_table += "\t</tbody>\n</table>"

# Output the HTML table
print(html_table)