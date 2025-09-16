#### Assignment 1
# Submitting to GitHub
The primary purpose of this assignment is to practice:
1. Running tests on your code, and
2. Uploading your assignments to GitHub

You can watch [this video](https://www.youtube.com/watch?v=yt-fd55CofY&ab_channel=ProfSteffen) for a guided tutorial. The actual code you will write and submit just involves gathering inputs, doing simple math, and printing out some statements. Put your code in the ***a01_submitting_to_github.py*** file. Do not edit or delete any other files.

## Logical Flow
1. Before starting, make sure you're following along with the video linked above so you understand how to run the tests included with the assignment and how to turn the assignment in.
2. Using the `input()` function, ask the user:
    - `Please enter a whole number: `
    - Assume that the user will always enter a valid whole number.
    - Store the number in a variable
3. Convert the number to an `int` datatype.
4. Divide the inputted number by 2 and store the result
    - You can do steps 2-4 each on separate lines, or combine multiple steps on a single line. In this class, there are almost always many ways you can write valid code. As long as it fulfills the requirements in the instructions, you'll get full points.
4. Print out the message:
    - `<number from input> divided by 2 is <new number>.`
    - But with actual values. For example, if the user entered *10*, then the message should display as:
    - `10 divided by 2 is 5.0.`

Be sure to include comments in your code. Be sure to run the tests in the testing tab to see what score you'll get.
Push your code to your GitHub repository in order to receive credit for the assignment.

## Rubric
- See `RUBRIC.md` for details on each of the tests you're scored on.
- To see what score you'll receive, run the tests using the testing tab (it looks like a beaker).
    - In the testing tab, press `Configure Python Tests`, then choose `pytest`, then `tests`, and then press the `Run Tests` button.
        - If you accidentally choose the wrong options for `Configure Python Tests`, to choose again, go to `View` > `Command Palette` and then type `Python: Configure Tests` and hit enter. Then choose the options above again.
- To see your results and any error messages, right click the `TEST_RESULTS_SUMMARY.md` file and choose `Open Preview`.

## Example Output
```
Please enter a whole number: 10
10 divided by 2 is 5.0.
```