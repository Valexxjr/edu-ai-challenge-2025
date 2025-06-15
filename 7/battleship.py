import random

# Game constants
BOARD_SIZE = 10
NUM_SHIPS = 3
SHIP_LENGTH = 3

# Game state
player_ships = []
cpu_ships = []
player_num_ships = NUM_SHIPS
cpu_num_ships = NUM_SHIPS

guesses = []
cpu_guesses = []
cpu_mode = 'hunt'
cpu_target_queue = []

board = []
player_board = []

def create_board():
    global board, player_board
    for i in range(BOARD_SIZE):
        board.append(['~' for _ in range(BOARD_SIZE)])
        player_board.append(['~' for _ in range(BOARD_SIZE)])
    print('Boards created.')

def place_ships_randomly(target_board, ships_array, number_of_ships):
    placed_ships = 0
    while placed_ships < number_of_ships:
        orientation = 'horizontal' if random.random() < 0.5 else 'vertical'
        
        if orientation == 'horizontal':
            start_row = random.randint(0, BOARD_SIZE - 1)
            start_col = random.randint(0, BOARD_SIZE - SHIP_LENGTH)
        else:
            start_row = random.randint(0, BOARD_SIZE - SHIP_LENGTH)
            start_col = random.randint(0, BOARD_SIZE - 1)

        temp_locations = []
        collision = False

        for i in range(SHIP_LENGTH):
            check_row = start_row
            check_col = start_col
            if orientation == 'horizontal':
                check_col += i
            else:
                check_row += i
            
            location_str = f"{check_row}{check_col}"
            temp_locations.append(location_str)

            if check_row >= BOARD_SIZE or check_col >= BOARD_SIZE:
                collision = True
                break

            if target_board[check_row][check_col] != '~':
                collision = True
                break

        if not collision:
            new_ship = {'locations': [], 'hits': []}
            for i in range(SHIP_LENGTH):
                place_row = start_row
                place_col = start_col
                if orientation == 'horizontal':
                    place_col += i
                else:
                    place_row += i
                
                location_str = f"{place_row}{place_col}"
                new_ship['locations'].append(location_str)
                new_ship['hits'].append('')

                if target_board == player_board:
                    target_board[place_row][place_col] = 'S'
            
            ships_array.append(new_ship)
            placed_ships += 1

    print(f"{number_of_ships} ships placed randomly for {'Player' if target_board == player_board else 'CPU'}.")

def print_board():
    print('\n   --- OPPONENT BOARD ---          --- YOUR BOARD ---')
    header = '  ' + ' '.join(str(h) for h in range(BOARD_SIZE))
    print(f"{header}     {header}")

    for i in range(BOARD_SIZE):
        row_str = f"{i} "
        row_str += ' '.join(board[i])
        row_str += f"    {i} "
        row_str += ' '.join(player_board[i])
        print(row_str)
    print('\n')

def process_player_guess(guess):
    global cpu_num_ships
    if guess is None or len(guess) != 2:
        print('Oops, input must be exactly two digits (e.g., 00, 34, 98).')
        return False

    try:
        row = int(guess[0])
        col = int(guess[1])
    except ValueError:
        print('Oops, please enter valid numbers.')
        return False

    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        print(f'Oops, please enter valid row and column numbers between 0 and {BOARD_SIZE - 1}.')
        return False

    formatted_guess = guess

    if formatted_guess in guesses:
        print('You already guessed that location!')
        return False
    
    guesses.append(formatted_guess)
    hit = False

    for ship in cpu_ships:
        if formatted_guess in ship['locations']:
            index = ship['locations'].index(formatted_guess)
            if ship['hits'][index] != 'hit':
                ship['hits'][index] = 'hit'
                board[row][col] = 'X'
                print('PLAYER HIT!')
                hit = True

                if is_sunk(ship):
                    print('You sunk an enemy battleship!')
                    global cpu_num_ships
                    cpu_num_ships -= 1
                break
            else:
                print('You already hit that spot!')
                hit = True
                break

    if not hit:
        board[row][col] = 'O'
        print('PLAYER MISS.')

    return True

def is_valid_and_new_guess(row, col, guess_list):
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False
    guess_str = f"{row}{col}"
    return guess_str not in guess_list

def cpu_turn():
    global cpu_mode, cpu_num_ships, player_num_ships
    print("\n--- CPU's Turn ---")
    made_valid_guess = False

    while not made_valid_guess:
        if cpu_mode == 'target' and cpu_target_queue:
            guess_str = cpu_target_queue.pop(0)
            guess_row = int(guess_str[0])
            guess_col = int(guess_str[1])
            print(f'CPU targets: {guess_str}')

            if guess_str in cpu_guesses:
                if not cpu_target_queue:
                    cpu_mode = 'hunt'
                continue
        else:
            cpu_mode = 'hunt'
            guess_row = random.randint(0, BOARD_SIZE - 1)
            guess_col = random.randint(0, BOARD_SIZE - 1)
            guess_str = f"{guess_row}{guess_col}"

            if not is_valid_and_new_guess(guess_row, guess_col, cpu_guesses):
                continue

        made_valid_guess = True
        cpu_guesses.append(guess_str)
        hit = False

        for ship in player_ships:
            if guess_str in ship['locations']:
                index = ship['locations'].index(guess_str)
                ship['hits'][index] = 'hit'
                player_board[guess_row][guess_col] = 'X'
                print(f'CPU HIT at {guess_str}!')
                hit = True

                if is_sunk(ship):
                    print('CPU sunk your battleship!')
                    global player_num_ships
                    player_num_ships -= 1
                    cpu_mode = 'hunt'
                    cpu_target_queue.clear()
                else:
                    cpu_mode = 'target'
                    adjacent = [
                        {'r': guess_row - 1, 'c': guess_col},
                        {'r': guess_row + 1, 'c': guess_col},
                        {'r': guess_row, 'c': guess_col - 1},
                        {'r': guess_row, 'c': guess_col + 1}
                    ]
                    for adj in adjacent:
                        if is_valid_and_new_guess(adj['r'], adj['c'], cpu_guesses):
                            adj_str = f"{adj['r']}{adj['c']}"
                            if adj_str not in cpu_target_queue:
                                cpu_target_queue.append(adj_str)
                break

        if not hit:
            player_board[guess_row][guess_col] = 'O'
            print(f'CPU MISS at {guess_str}.')

            if cpu_mode == 'target' and not cpu_target_queue:
                cpu_mode = 'hunt'

def is_sunk(ship):
    return all(hit == 'hit' for hit in ship['hits'])

def game_loop():
    if cpu_num_ships == 0:
        print('\n*** CONGRATULATIONS! You sunk all enemy battleships! ***')
        print_board()
        return
    if player_num_ships == 0:
        print('\n*** GAME OVER! The CPU sunk all your battleships! ***')
        print_board()
        return

    print_board()
    guess = input('Enter your guess (e.g., 00): ')
    player_guessed = process_player_guess(guess)

    if player_guessed:
        if cpu_num_ships == 0:
            game_loop()
            return

        cpu_turn()

        if player_num_ships == 0:
            game_loop()
            return

    game_loop()

def main():
    create_board()
    place_ships_randomly(player_board, player_ships, player_num_ships)
    place_ships_randomly(board, cpu_ships, cpu_num_ships)

    print("\nLet's play Sea Battle!")
    print(f'Try to sink the {cpu_num_ships} enemy ships.')
    game_loop()

if __name__ == "__main__":
    main() 