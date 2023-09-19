## Exercise 1

**Question 1**
before running:
10 loops, 1second
we predict it will take 10 seconds to run

actual output (sleep_time): 10.012 seconds

**Question 2**
Numbers with the int type can only be integer values. Float allows the program to use decimal values as well.

The program would not run if these notations were removed/incorrect because any non integer values would cause an error.

**Question 3**
time.ticks_diff(toc, tic) will not incorrectly calculate the elapsed time if zero wraps around

## Exercise 2
**Question 1**
The user may not have the access to input when the program is implemented on a chip like raspberry pi pico. A json file is needed for the parameters.  Additionally, it makes sure the parameters are set to usable values to prevent errors from user input.

**Question 2**
It is easier and more clear if we set the parameter in a separate file. This allows the parameters to be changes/updated later more easily if it becomes necessary to do so.

**Question 3**
Micropython has fewer built in libraries/functions than python normally does. Without checking with the is_regular_file() function, you can get an error message from the file not being found (essentially, os.path.isfile does not work on its own in micropython).

## Exercise 3
**Question 1**
If the sample time is increased too much the program can no longer differentiate between a dot and a dash input. It should be less than the dot_dash_threshold value.
