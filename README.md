# traceroute
some notes...

1. I used the zip() function to read all text files simultaneously.

2. Hosts contains all hosts for a hop across all .txt files.

3. You will have to delete the .json file before running the program again if you use the same name for -o arg.
   Otherwise the new run stats will append to the end of the .json file

4. If a hop contains '*', the entire hop is skipped from the final calculations
