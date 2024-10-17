# Files sorter

Application sort files in folder. All files move to new folders grouped by file types.

Sorter run in command line. application receive 2 parameters. 
1-st is the path of an existing folder where all the files mixed up, and the 2nd parameter is a 
destination folder's path.

For an example, you can start application with command:

'python3 files_sorter.py ../garbage ../dist'

where '../garbage' is a path to existing folder
and '../dist' is a path to new well sorted folder.

Application sort the files asynchronously in few parallel Processes
