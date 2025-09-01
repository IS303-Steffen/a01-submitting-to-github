#### Assignment 2
# Submitting to GitHub
The primary purpose of this assignment is to practice:
1. Running tests on your code, and
2. Uploading your assignments to GitHub

You can watch [this video](https://www.youtube.com/watch?v=8Kue74yURcQ&ab_channel=JacobSteffen) or read [this tutorial](https://www.dropbox.com/scl/fi/tuug12w6d38frqzyjsseo/Running-Tests-Uploading-Assignments-to-GitHub.pdf?rlkey=u7lcb5gknx9xao9o8in26vgi3&st=tjwu1tr6&dl=0) for instructions on both of those. The actual code you will write and submit just involves gathering inputs, doing simple math, and printing out some statements. Put your code in the ***a01_submitting_to_github.py*** file. Do not edit or delete any other files.

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

Be sure to include comments in your code. Push your code to your GitHub repository in order to receive credit for the assignment

## Example Output

```
Please enter a whole number: 10
10 divided by 2 is 5.0.
```

## Rubric
This assignment contains 4 automated tests. The tests will ignore spacing, capitalization, and punctuation, but you will fail the tests if you spell something wrong or calculate something incorrectly.
<table>
<thead>
    <tr>
        <th>Test</th>
        <th>Description</th>
        <th>Points</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>1. Input Prompts</td>
        <td>You must use <code>input()</code> to ask the user <code>Please enter a whole number:</code></td>
        <td>30</td>
    </tr>
    <tr>
        <td>2. Printed Messages</td>
        <td>Your printed output must contain the phrase <code>divided by 2 is</code></td>
        <td>30</td>
    </tr>
    <tr>
        <td>3. Correct Calculations</td>
        <td>Your printed output must accurately calculate a number being divided by 2.
        The following cases will be tested<br><br>
        <table border="1">
          <thead>
            <tr>
              <th>Input</th>
              <th>Expected Output</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>'10'</code></td>
              <td><code>'5.0'</code></td>
            </tr>
            <tr>
              <td><code>'0'</code></td>
              <td><code>'0.0'</code></td>
            </tr>
            <tr>
              <td><code>'15'</code></td>
              <td><code>'7.5'</code></td>
            </tr>
            <tr>
              <td><code>'-100'</code></td>
              <td><code>'-50.0'</code></td>
            </tr>
          </tbody>
        </table>
        </td>
        <td>30</td>
    </tr>
    <tr>
        <td>4. Sufficient Comments </td>
        <td>Your code must include at least <code>3</code> comments. You can use <code>#</code>, <code>''' '''</code>, or <code>""" """</code></td>
        <td>10</td>
    </tr>
    <tr>
        <td colspan="2">Total Points</td>
        <td>100</td>
  </tr>
</tbody>
</table>