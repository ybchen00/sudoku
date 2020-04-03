## Sudoku Solver

This program solves sudoku puzzles by regarding it as a Constraint Satisfaction Problem (CSP). The solver implements backtracking search using the minimum remaining value heuristic. Forward checking is also applied to reduce variables domains.


Can run the solver by:
	
	1. python sudoku.py    
	
		- For solving boards in sudokus_start.txt
	        - Solutions can be found in sudokus_finish.txt
		
	2. python sudoku.py inputSudokuBoard
                
		- For example: python sudoku.py 800000000003600000070090200050007000000045700000100030001000068008500010090000400
		- Solution will be printed on terminal and output as a string in output.txt
		
For sample results, please refer to **SampleResults.txt**
