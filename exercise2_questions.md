**Question 1**
The user may not have the access to input when the program is implemented on a chip like raspberry pi pico. A json file is needed for the parameters.  Additionally, it makes sure the parameters are set to usable values to prevent errors from user input.

**Question 2**
It is easier and more clear if we set the parameter in a separate file. This allows the parameters to be changes/updated later more easily if it becomes necessary to do so.

**Question 3**
Micropython has fewer built in libraries/functions than python normally does. Without checking with the is_regular_file() function, you can get an error message from the file not being found (essentially, os.path.isfile does not work on its own in micropython).
