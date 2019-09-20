#coding:utf-8

"""
author: Yibing Chen 


Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")

    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i+j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    board = backtrack(board)
    solved_board = board
    return solved_board

def backtrack(board):
    if is_complete(board):
        #print("completed")
        return board
    var = select_unassigned_var(board)
    if var == None:
        return board
    #print("var: " + var)
    row = var[0]
    col = var[1]
    domain = [i+1 for i in range(9)]
    for d in domain:
        if is_consistent(row, col, d, board):
            board[var] = d
            #print(d)
            #print_board(board)
            #input()
            result = backtrack(board)
            if result != False:
                return result
            board[var]= 0
    return False
    
    
def is_complete(assignment):
    if len(assignment) == 0:
        return False
    for a in assignment:
        if assignment[a] == 0:
            return False
    return True

def select_unassigned_var(board):
    minCount = sys.maxsize
    minVar = None
    for a in board:
        if board[a] == 0:
            count = remaining_val(board, a)
            if count < minCount:
                minCount = count
                minVar = a
    return minVar

def remaining_val(board, key):
    row = key[0]
    col = key[1]
    count_c = 0
    count_r = 0
   
    for c in COL:
        key = row+c
        if board[key] == 0:
            count_r+=1
    for r in ROW:
        key = r+col
        if board[key] == 0:
            count_c+=1
            
    
    return min(count_c, count_r)
    
def is_consistent(row, col, value, board):

    for c in COL: # check consistency in row
        key = row+c
        if value == board[key]:
            return False
    for r in ROW: # check consistency in columns
        key = r+col
        if value == board[key]:
            return False
        
    row_square = ROW.find(row)//3*3
    col_square = (int(col)-1)//3*3
    #print("row_square = " + str(row_square) + " - " + str(row_square+2))
    #print("col_square = " + str(col_square) + " - " + str(col_square+2))
    #print("value = " + str(value))
    #print("value pos: " + row+col)
    for r in range(row_square, row_square+3):
        for c in range(col_square, col_square+3):
            #print("r = " + str(r))
            #print("c = " + str(c))
            if r == ROW.find(row) or c == int(col)-1:
                continue

            key = ROW[r]+COL[c]
            #print("checked key = " + key)
            if value == board[key]:
                return False
    return True

### Takes input from command line, prints the solved board, and outputs solution to output.txt ###
def input_from_cmd(argv):
    s=argv
    board = { ROW[r] + COL[c]: int(s[9*r+c])
              for r in range(9) for c in range(9)}

    # Solve with backtracking
    solved_board = backtracking(board)


    # Print solved board. 
    print_board(solved_board)
    
    sln_string = board_to_string(solved_board)
    
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    outfile.write(sln_string)        
    
### Takes input file of 400 unsolved Sudoku, then prints the unsolved and solved boards.### 
# Also records the time to solve each board in report_time.txt
def input_files(src_filename, ans_filename):
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
        ansfile = open(ans_filename, "r")
        ans_list = ansfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    #out_filename = 'output.txt'
    #outfile = open(out_filename, "w")

    # Solve each board using backtracking
    
    sudoku_list = sudoku_list.split("\n")
    ans_list = ans_list.split("\n")
    outfile = open("report_time.txt", "w").close()
    for i in range(len(sudoku_list)):     
        init_time = time.process_time()
        line = sudoku_list[i]
        ans_line = ans_list[i]
        if len(line) < 9:            
            continue
        # Parse boards to dict representation, scanning board L to R, Up to Down        
        board = { ROW[r] + COL[c]: int(line[9*r+c])                  
        for r in range(9) for c in range(9)}        
        # Print starting board.     
        print("Original Board " + str(i) + " : ")
        print_board(board)        
        
        # Solve with backtracking  
        solved_board = backtracking(board)        
        # Print solved board.   
        print("Solved: ")
        print_board(solved_board)   
        print("\n")
        
        # Write board to file   
        
        sln = board_to_string(solved_board)
        processed_time = time.process_time() - init_time
        outfile = open("report_time.txt", "a")
        write_line = "Board " + str(i+1) + ": " + str(processed_time) + "\n"
        outfile.write(write_line)
        outfile.flush()
        #print("sln : " + sln)
        #print("ans_line: " + ans_line)
        if sln != ans_line:
            raise Exception("wrong ans for board " + line)

    print("Finishing all boards in file.")

    
        
### Can either takes board from command line or file and output solved boards ###
if __name__ == '__main__':
    #  Read boards from source.
    if len(sys.argv) > 1:
        input_from_cmd(sys.argv[1])
    else:
        input_files("sudokus_start.txt", "sudokus_finish.txt")   
   
