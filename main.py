from typing import List, Callable
import random

def exception_handler(_prompt: str) -> int:
    while True:
        try:
            value: int = int(input(_prompt))
            while value < 3 or value > 9:
                print("Данное число не входит в заданный диапазон.")
                value: int = int(input(_prompt))
            return value
        except ValueError:
            print("Вы неправильно ввели значение.\n")

def move_handler(width: int, height: int, field: List[List[str]], is_X_turn: bool) -> List[int]:
    current_move_checker: Callable = lambda val: 'X' if val else 'O'
    while True:
        try:
            h, w = map(int, input(f'Сейчас ходит: {current_move_checker(is_X_turn)}.\tВведите индекс строки и столбца через пробел: \t').split())
            
            if not (1 <= h <= height and 1 <= w <= width):
                print('Значение вне пределов игрового поля. Попробуйте ещё раз.')
                continue
            
            if field[h - 1][w - 1] != '.':
                print(f"Данная клетка уже занята значением {field[h - 1][w - 1]}. Выберите другую клетку.")
                continue
            
            return [h, w]
        
        except ValueError:
            print('Недопустимое значение. Введите два целых числа через пробел.')

def build_field(width: int, height: int) -> List[List[str]]:
    return [['.' for _ in range(width)] for _ in range(height)]

def get_columns(field: List[List[str]]) -> List[List[str]]:
    return [list(col) for col in zip(*field)]

def is_draw(field: List[List[str]]) -> bool:
    return all(cell != '.' for row in field for cell in row)

def print_field(field: List[List[str]]) -> None:
    print("  ", end="")
    for col_index in range(1, len(field[0]) + 1):
        print(f'{col_index} ', end="")
    print()  
    
    for row_index, row in enumerate(field, 1): 
        print(f'{row_index}', ' '.join(row))

def commit_move(field: List[List[str]], pos: List[int], is_X_turn: bool) -> None:
    if is_X_turn:
        field[pos[0] - 1][pos[1] - 1] = 'X'
    else:
        field[pos[0] - 1][pos[1] - 1] = 'O'
    print_field(field=field)

def check_winner(field: List[List[str]]) -> bool:
    for row in field:
        if len(set(row)) == 1 and row[0] != '.':
            return True
    
    columns = get_columns(field)
    for column in columns:
        if len(set(column)) == 1 and column[0] != '.':
            return True

    if len(set(field[i][i] for i in range(len(field)))) == 1 and field[0][0] != '.':
        return True

    if len(set(field[i][len(field) - 1 - i] for i in range(len(field)))) == 1 and field[0][len(field) - 1] != '.':
        return True
    
    return False

def robot_move(width: int, height: int, field: List[List[str]]) -> List[int]:
    available_moves = [(r + 1, c + 1) for r in range(height) for c in range(width) if field[r][c] == '.']
    return random.choice(available_moves)

def start_game():
    while True:
        try:
            choice: int = int(input('Как вы хотите играть?\t1. Против другого игрока.\t2. Против робота\t3. Я хочу выйти\n'))
            if choice == 1:
                is_X_turn = random.randint(0, 1) == 1
                print("Первым ходит X!" if is_X_turn else "Первым ходит O!")
                break  
            elif choice == 2:
                is_X_turn = True  # игрок начинает первым
                break
            elif choice == 3:
                print("Спасибо за игру!")
                exit()  
            else:
                print("Недопустимый выбор. Пожалуйста, выберите 1, 2 или 3.")
        except ValueError:
            print("Вы неправильно ввели значение. Пожалуйста, введите целое число.")
    
    width = exception_handler('Введите ширину поля (3-9): \n')
    height = exception_handler('Введите длину поля (3-9): \n')
    field = build_field(width=width, height=height)
    print_field(field=field)
    
    while True:
        if is_X_turn:
            pos: List[int] = move_handler(width=width, height=height, field=field, is_X_turn=is_X_turn)
        else:
            pos = robot_move(width=width, height=height, field=field)
            print(f"Робот делает ход: {pos[0]} {pos[1]}")

        commit_move(field=field, pos=pos, is_X_turn=is_X_turn)
        
        if check_winner(field):
            print(f"Игрок {'X' if not is_X_turn else 'O'} победил!" if not is_X_turn else "Робот победил!")
            regenerate_game()
            break
        
        if is_draw(field):
            print("Ничья!")
            regenerate_game()
            break
        
        is_X_turn = not is_X_turn  # меняем ход

def regenerate_game():
    while True:
        try:
            choice: int = int(input('Хотите повторить игру или выйти?\n1. Продолжить\n2. Выйти из игры\n'))
            if choice == 1:
                start_game()
                break  
            elif choice == 2:
                print("Спасибо за игру!")
                exit()  
            else:
                print("Недопустимый выбор. Пожалуйста, выберите 1 или 2.")
        except ValueError:
            print("Вы неправильно ввели значение. Пожалуйста, введите целое число.")

def main():
    start_game()

if __name__ == "__main__":
    main()
