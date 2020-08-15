# simple tic tac toe game
# moves from 0-8 , beggining with tile in top left
# player codes as 1 and 2
# empty tiles denote with 0


def newboard():
    board = [[0,0,0],
            [0,0,0],
            [0,0,0]]
    return board

def print_board(board):
    for row in board:
        print(row)

def check_valid(m, board):
    try:
        m = int(m)
    except:
        return False
    row = m // 3
    col = m % 3
    if board[row][col] != 0:
        return(False)
    return True
    
def move(m, player, board):
    m = int(m)
    if check_valid(m, board):
        row = m // 3
        col = m % 3
        board[row][col]  = player
        

def check_rows(board):
    for row in board:
        if row == [1,1,1]:
           return 1
        if row == [2,2,2]:   
            return 2
    return 0

def check_cols(board):
    for i in range(3):
        col = [r[i] for r in board]
        if col == [1,1,1]:
           return 1
        if col == [2,2,2]:   
            return 2
    return 0
        
def check_diag(board):
    d1 = [ board[0][0], board[1][1], board[2][2] ]
    d2 = [ board[0][2], board[1][1], board[2][0] ]
    if d1 == [1,1,1] or d2 == [1,1,1]:
        return 1
    if d1 == [2,2,2] or d2 == [2,2,2]:   
        return 2
    return 0

def check_gamestate(board):
    p = check_rows(board)
    if p != 0:
        return p
    p = check_cols(board)
    if p != 0:
        return p
    return check_diag(board)


def main():
    b = newboard()
    print_board(b)
    i = 1
    while True:
        i += 1

        m = int(input("Enter move: "))
        player = (i % 2) + 1
        move(m, player, b)

        print_board(b)

        p = check_gamestate(b)
        if p != 0:
            print(f"PLAYER {p} WINS")
            print_board(b)
            return

if __name__ == "__main__":
    main()