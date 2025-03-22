import time

BASE = 3
BOARD_SIZE = 9


class SudokuSolver:
    @staticmethod
    def heuristic(board):
        """
        Heuristic function for A* search.
        Calculates the number of missing unique values in rows, columns, and 3x3 boxes.
        """
        conflicts = 0

        # Check rows
        for row in board:
            missing_values = 0
            for value in row:
                if value != 0:
                    missing_values += 1
            conflicts += BOARD_SIZE - missing_values

        # Check columns
        for col in range(BOARD_SIZE):
            missing_values = 0
            for row in range(BOARD_SIZE):
                if board[row][col] != 0:
                    missing_values += 1
            conflicts += BOARD_SIZE - missing_values

        # Check 3x3 boxes
        for subSudoku in range(0, BOARD_SIZE, BASE):
            for box_col in range(0, BOARD_SIZE, BASE):
                missing_values = 0
                for row in range(subSudoku, subSudoku + BASE):
                    for col in range(box_col, box_col + BASE):
                        if board[row][col] != 0:
                            missing_values += 1
                conflicts += BOARD_SIZE - missing_values

        return conflicts

    @staticmethod
    def find_most_constrained_cell(board):
        """
        Find the empty cell with the fewest valid numbers to choose from (most constrained).
        """
        min_number = 10  # min_number_of_possible_values for a cell 
        best_cell = None #contiendra les coordonnées (ligne, colonne) de la cellule la plus contrainte.
        valid_options = None  #variable qui contien l'ensemble des numéros valides pour la cellule best_cell

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == 0:
                    options = set()
                    for num in range(1, BOARD_SIZE + 1):
                        if SudokuSolver.is_valid_move(board, num, (row, col)):
                            options.add(num)
                    if len(options) < min_number:
                        min_number = len(options)
                        best_cell = (row, col)
                        valid_options = options
                        if min_number == 1:  # Short-circuit for the most constrained
                            return best_cell, valid_options

        return best_cell, valid_options

    @staticmethod
    def is_valid_move(board, num, pos):
        """
        Check if placing 'num' in 'pos' (row, col) is valid.
        """
        row, col = pos

        # Check row
        for value in board[row]:
            if value == num:
                return False

        # Check column
        for i in range(BOARD_SIZE):
            if board[i][col] == num:
                return False

        # Check 3x3 box
        box_x = 3 * (row // BASE)
        box_y = 3 * (col // BASE)
        for i in range(box_x, box_x + BASE):
            for j in range(box_y, box_y + BASE):
                if board[i][j] == num:
                    return False

        return True

    @staticmethod
    def solve_sudoku(board):
        # Add tracking variables just for output
        attempts = 0  #calculate how many boards we’ve processed
        max_queue_size = 0
        max_heuristic = 0

        # Priority queue for A* search using a sorted list
        Frontiere = [] #list that contains the input board with its heuristic score.
        initial_heuristic = SudokuSolver.heuristic(board)
        Frontiere.append((initial_heuristic, 0, board)) #0 here is g_cost (no moves yet).

        visited_boards = set()

        while Frontiere:
            # Find the board with the minimum f-cost (lowest cost)
            min_f_cost = float('inf')
            min_board_index = -1
            for i in range(len(Frontiere)):
                f_cost = Frontiere[i][0]  # f-cost is the first element of each tuple
                if f_cost < min_f_cost:
                    min_f_cost = f_cost
                    min_board_index = i

            # Get the board with the minimum f-cost
            current_heuristic, g_cost, current_board = Frontiere.pop(min_board_index)

            # Update tracking variables
            max_queue_size = max(max_queue_size, len(Frontiere))
            max_heuristic = max(max_heuristic, current_heuristic)
            attempts += 1

            # Check if the board has been visited before
            board_tuple = tuple(tuple(row) for row in current_board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Find the most constrained cell (empty cell with fewest valid options)
            empty_cell, options = SudokuSolver.find_most_constrained_cell(current_board)

            # If the board is solved (no empty cells), return the solution
            if not empty_cell:
                return {
                    'board': current_board,
                    'attempts': attempts,
                   
                    'max_heuristic': max_heuristic
                }

            # For each valid option for the empty cell, create a new board and add to the open set
            row, col = empty_cell
            for num in options:
                # Create a copy of the board and update the current empty cell
                new_board = []
                for row_values in current_board:
                     new_board.append(row_values.copy())
                new_board[row][col] = num

                # Calculate new costs
                new_g_cost = g_cost + 1
                new_h_cost = SudokuSolver.heuristic(new_board)
                new_f_cost = new_g_cost + new_h_cost

                # Add the new board to the open set
                Frontiere.append((new_f_cost, new_g_cost, new_board))
        return None
    
    
    
def print_board(board):
    """
    Print the Sudoku board in a formatted way.
    """
    for i in range(BOARD_SIZE):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(BOARD_SIZE):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def main():
    # Example with the hardest Sudoku board in the word (0 represents empty cells)
    sudoku_board = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]

    print("Original Sudoku Board:")
    print_board(sudoku_board)

    start_time = time.time()
    solution = SudokuSolver.solve_sudoku(sudoku_board)
    end_time = time.time()

    if solution:
        print("\nSolved Sudoku Board:")
        print_board(solution['board'])

        print("\nSolving Statistics:")
        print(f"Total Attempts: {solution['attempts']}")
       
        print(f"Maximum Heuristic Value: {solution['max_heuristic']}") #to see how much the board configuration is far from the solution
        print(f"Solving Time: {end_time - start_time:.4f} seconds")
    else:
        print("\nNo solution exists for this Sudoku board.")

if __name__ == "__main__":
    main()
