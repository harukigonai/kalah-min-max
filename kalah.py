MAX_INT = 99999999
MIN_INT = -MAX_INT

def turn(pit, board, player):
    board_cpy = board.copy()

    last_pit = -1

    curr_pit = (pit + 1) % 14
    count = board_cpy[pit]
    board_cpy[pit] = 0
    while count != 0:
        # if curr_pit is not opponent's store, deposit
        if not ((player == 0 and curr_pit == 13) or
                (player == 1 and curr_pit == 6)):
            board_cpy[curr_pit] += 1
            count -= 1

            last_pit = curr_pit
        curr_pit = (curr_pit + 1) % 14

    # if the last pit was empty and is ours and the opposite pit is not empty,
    # then steal all seeds
    if board_cpy[last_pit] == 1 and board_cpy[12 - last_pit] != 0:
        if 0 <= last_pit and last_pit <= 5 and player == 0:
            board_cpy[6] += board_cpy[last_pit] + board_cpy[12 - last_pit]
            board_cpy[12 - last_pit] = 0
            board_cpy[last_pit] = 0
        elif 7 <= last_pit and last_pit <= 13 and player == 1:
            board_cpy[13] += board_cpy[last_pit] + board_cpy[12 - last_pit]
            board_cpy[12 - last_pit] = 0
            board_cpy[last_pit] = 0

    # if the last pit was our store, we can move again
    move_again = False
    if (last_pit == 6 and player == 0) or \
       (last_pit == 13 and player == 1):
        move_again = True
    return move_again, board_cpy

def successors(board, player):
    if player == 0:
        pits = list(range(0, 6))
    else:
        pits = list(range(7, 13))

    successor_li = []
    for pit in pits:
        if board[pit] != 0:
            move_again, board_cpy = turn(pit, board, player)
            successor_li.append((pit, move_again, board_cpy))

    return successor_li

def max_value(board, k, a, b):
    if k == 0 or is_terminal(board):
        return utility(board), None
    v = MIN_INT
    for succ in successors(board, 0):
        pit, move_again, board_cpy = succ
        if move_again:
            v2, _ = max_value(board_cpy, k - 1, a, b)
        else:
            v2, _ = min_value(board_cpy, k - 1, a, b)
        if v2 > v:
            v, move = v2, pit
            a = max(a, v)
        if v >= b:
            return v, move
    return v, move

def min_value(board, k, a, b):
    if k == 0 or is_terminal(board):
        return utility(board), None
    v = MAX_INT
    for succ in successors(board, 1):
        pit, move_again, board_cpy = succ
        if move_again:
            v2, _ = min_value(board_cpy, k - 1, a, b)
        else:
            v2, _ = max_value(board_cpy, k - 1, a, b)
        if v2 < v:
            v, move = v2, pit
            b = min(b, v)
        if v <= a:
            return v, move
    return v, move
        
def is_terminal(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0

def utility(board):    
    return sum(board[0:7]) - sum(board[7:14])

def main():
    # board[0:6] are player 0's houses
    # board[6] is player 0's store

    # board[7:13] are player 1's houses
    # board[13] is player 1's store
    board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    _, move = max_value(board, 12, MIN_INT, MAX_INT)
    print("Best move is", move)

if __name__ == "__main__":
    main()
