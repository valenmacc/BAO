from Common.Choice import Choice

#This heuristic returns the relative size of a piece, favouring larger pieces.
def heuristic1(choice: Choice, x_dim: int, y_dim: int, board=None) -> float:
    size = choice.piece.x_dim * choice.piece.y_dim
    return size / (x_dim * y_dim)

#This heuristic favours placing pieces with greater shared borders relative to their size.
def heuristic2(choice: Choice, x_dim: int, y_dim: int, board: list) -> float:
    x_1 = choice.x_pos - 1
    x_2 = choice.x_pos + choice.piece.x_dim + 1
    y_1 = choice.y_pos - 1
    y_2 = choice.y_pos + choice.piece.y_dim + 1
    count = 0
    
    for x in range (choice.x_pos, x_2 - 1):
        if y_1 >= 0:
            if board[x][y_1] == True:
                count += 1
        else:
            count += 1
        
        if y_2 < y_dim:
            if board[x][y_2] == True:
                count += 1
        else:
            count += 1
    for y in range (choice.y_pos, y_2 - 1):
        if x_1 >= 0:
            if board[x_1][y] == True:
                count += 1
        else:
            count += 1
        if x_2 < x_dim:
            if board[x_2][y] == True:
                count += 1
        else:
            count += 1
    return count/(choice.piece.x_dim + choice.piece.y_dim)