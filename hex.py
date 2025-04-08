import os
import re
import random
from hexbot import HexBot

# region GLOBALS

# Variables globales para los colores
global RED
global BLUE
global RESET
global PLAYER_1
global PLAYER_2
global oo
oo = float('inf')

RED = '\033[31m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'
PLAYER_1 = 1
PLAYER_2 = 2
# endregion


# region UTILS
def clear_console():
    '''
    Permite limpiar la consola en dependencia del sistema operativo.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_board(board,msg=None,clear=True):
    '''
    Imprime el tablero en pantalla.\n
    msg: Mensaje opcional.\n
    clear: Limpia la pantalla de forma opcional (por defecto en True).
    '''
    if clear: clear_console()
    if msg: print(msg+'\n')
    board.pretty_print()

def game_selection():
    print('Selecciona el modo de juego:\n1 Jugador vs Jugador\n2 Jugador vs IA\n3 IA vs IA')
    choice = input('> ')
    while choice not in ['1','2','3']:
        clear_console()
        print(f'{RED}Entrada inválida{RESET}')
        print('Selecciona el modo de juego:\n1 Jugador vs Jugador\n2 Jugador vs IA\n3 IA vs IA')
        choice = input('> ')
    return int(choice)

def get_size() -> int:
    '''
    Obtiene la entrada del usuario correspondiente al tamaño del tablero.
    '''
    size_pattern = r'[1-9]+'
    size = re.search(size_pattern,(input("Introduce el tamaño del tablero:\n> ")))
    
    while not size:
        size = re.search(size_pattern,input('El tamaño introducido es inválido, por favor brinde un tamaño de tablero válido:\n> '))
        
    N = int(size.group())
    return N

def get_coords(player_id,board) -> tuple[int,int]:
    '''
    Obtiene la entrada del usuario correspondiente a la posición donde se colocará la ficha.
    '''
    tuple_pattern = r'(\d+)\s*\:\s*(\d+)'
    coords = re.search(tuple_pattern,input(f'Jugador {RED + 'rojo' if player_id == 1 else BLUE + 'azul'}{RESET} coloca ficha en:\n> '))
    while not coords:
        print_board(board,msg='--> Las coordenadas introducidas no son válidas.')
        coords = re.search(tuple_pattern,input(f'Jugador {RED + 'rojo' if player_id == 1 else BLUE + 'azul'}{RESET} coloca ficha en:\n> '))
    i,j = map(int,coords.groups())
    return i,j    

def check_win(board) -> bool:
    if board.check_connection(PLAYER_1):
        clear_console()
        print(f"\n--> Gana el jugador {RED}rojo{RESET}.")
        board.pretty_print()
        print_path(board,PLAYER_1)
        return True
    if board.check_connection(PLAYER_2):
        clear_console()
        print(f"\n--> Gana el jugador {BLUE}azul{RESET}.")
        board.pretty_print()
        print_path(board,PLAYER_2)
        return True
    return False

def human_vs_human():
    N = get_size()
    board = HexBoard(N)
    player_id = random.randint(1,2) # Decidimos de forma aleatoria el jugador que empieza
    while True: # Game Loop
        print_board(board)
        i,j = get_coords(player_id,board)
        while not board.place_piece(i,j,player_id):
            print_board(board,clear=False)
            i,j = get_coords(player_id,board)
        player_id = PLAYER_1 if player_id == PLAYER_2 else PLAYER_2
        if check_win(board): break

def human_vs_ai():
    N = get_size()
    board = HexBoard(N)
    human = random.randint(1,2)
    bot = HexBot(3-human)
    actual = random.randint(1,2)
    
    while True: # Game Loop
        print_board(board)
        i,j = get_coords(human,board) if human == actual else bot.play(board)
        while not board.place_piece(i,j,actual):
            print_board(board,clear=False)
            i,j = get_coords(actual,board)
        actual = PLAYER_1 if actual == PLAYER_2 else PLAYER_2
        if check_win(board): break

def ai_vs_ai():
    N = get_size()
    board = HexBoard(N)
    act = random.randint(1,2)
    bot1 = HexBot(PLAYER_1)
    bot2 = HexBot(PLAYER_2)

    while True:
        print_board(board)
        i,j = bot1.play(board) if act == PLAYER_1 else bot2.play(board)
        board.place_piece(i,j,act)
        act = PLAYER_2 if act == PLAYER_1 else PLAYER_1
        print_board(board)
        if check_win(board): break
        
def print_path(board,player_id):
    N = board.size
    _,parent = board.bfs(player_id)
    last = (0,N) if player_id is PLAYER_1 else (N,0)
    q = [parent[last]]
    while q:
        v = q.pop()
        if parent[v] is not None:
            q.append(parent[v])
            x,y = v
            board.board[x][y] = 'R' if player_id == PLAYER_1 else 'B'
    print_board(board,msg=f'\n--> Gana el jugador {RED + 'rojo' if player_id == PLAYER_1 else BLUE + 'azul'}{RESET}.')
# endregion


# region HEXBOARD
class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)

    def clone(self):
        """Devuelve una copia del tablero actual"""
        new_board = HexBoard(self.size)
        new_board.board = [l[:] for l in self.board]
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if row < 0 or row >= len(self.board) or col < 0 or col >= len(self.board[0]): 
            clear_console()
            print("--> Las coordenadas introducidas están fuera de los límites del tablero.\n")
            return False

        if self.board[row][col] != 0:
            clear_console()
            print(f"--> Ya existe una ficha de color {RED + 'rojo' if self.board[row][col] == 1 else BLUE + 'azul'}{RESET} en esa posición.\n")
            return False
        
        self.board[row][col] = player_id
        return True

    def get_possible_moves(self) -> list:
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        possible_moves = [(i,j) for i in range(len(self.board)) for j in range(len(self.board[i])) if self.board[i][j] == 0]
        return possible_moves
    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados"""
        if player_id != PLAYER_1 and player_id != PLAYER_2: raise Exception("El id de jugador es inválido.")
        N = self.size
        visited,_ = self.bfs(player_id)
        
        if player_id == PLAYER_1 and visited[(0,N)]:        # Si el jugador rojo visitó el vértice ficticio rojo significa que ganó
            return True
        if player_id == PLAYER_2 and visited[(N,0)]:        # Si el jugador azul visitó el vértice ficticio azul significa que ganó
            return True
        return False    
    
    def bfs(self,player_id) -> list[bool]:
        N = self.size
        visited = {(i,j):False for i in range(N) for j in range(N)}
        parent = {(i,j):None for i in range(N) for j in range(N)}
        visited[(0,N)] = visited[(N,0)] = False 
        
        # Los vértices ficticios sobre los que se hará el BFS son (0,N) y (N,0) respectivamente en dependencia de si el jugador es rojo o azul
        
        start = (0,-1) if player_id == PLAYER_1 else (-1,0)
        q = [start]
        parent[start] = None
        while q:
            v = q.pop()
            for neighbor in self.neighbors(v,player_id):
                if not visited[neighbor]:
                    q.append(neighbor)
                    parent[neighbor] = v
            visited[v] = True

        return visited,parent
        
    def neighbors(self,v,player_id) -> list[tuple]: # Devolvemos los vecinos en dependencia de la casilla actual y su posición par o impar.
            N = self.size
            if v == (0,-1) and player_id == PLAYER_1: return [(i,0) for i in range(N) if self.board[i][0] == player_id]
            if v == (-1,0) and player_id == PLAYER_2: return [(0,j) for j in range(N) if self.board[0][j] == player_id]
                
            vx,vy = v
            even = [(0,-1),(0,1),(-1,0),(1,0),(-1,1),(1,1)]
            odd =  [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1)]
            
            neighbors = []
            if vx % 2 == 0:
                for delta_x,delta_y in even:
                    nx,ny = vx + delta_x, vy + delta_y
                    if self.is_valid(nx,ny) and self.board[nx][ny] == player_id: neighbors.append((nx,ny))
            else:
                for delta_x,delta_y in odd:
                    nx,ny = vx + delta_x, vy + delta_y
                    if self.is_valid(nx,ny) and self.board[nx][ny] == player_id: neighbors.append((nx,ny))
            
            if vy == N-1 and player_id == PLAYER_1: neighbors.append((0,N))
            if vx == N-1 and player_id == PLAYER_2: neighbors.append((N,0))
            
            return neighbors
    
    def is_valid(self,nx,ny) -> bool:
        N = self.size
        return 0 <= nx < N and 0 <= ny < N
    
    def pretty_print(self) -> None:
        N = self.size
        tab = 1
        for i in range(N):
            print(' ' * tab,end='')
            for j in range(N):
                if self.board[i][j] == 0: print(f'{self.board[i][j]}{RESET} ', end='')          # Si no está tomada dejamos el '''''hexágono''''' en blanco
                elif self.board[i][j] == 1: print(f'{RED}{self.board[i][j]}{RESET} ', end='')   # Si está tomada por el jugador rojo imprimimos el '''''hexágono''''' en rojo
                elif self.board[i][j] == 'R': print(f'{YELLOW}1{RESET} ',end='')                # Camino de victoria del jugador rojo
                elif self.board[i][j] == 'B': print(f'{YELLOW}2{RESET} ',end='')                # Camino de victoria del jugador azul
                else: print(f'{BLUE}{self.board[i][j]}{RESET} ', end='')                        # Si está tomada por el jugador azul imprimimos el '''''hexágono''''' en azul
            tab += -1 if i%2 == 0 else 1
            print()     # Pasamos a la siguiente línea
        
        print() # Dejamos un espacio para el texto que siga
        
# endregion

# region PLAYER
class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
choice = game_selection()
match(choice):
    case 1: human_vs_human()
    case 2: human_vs_ai()
    case 3: ai_vs_ai()
# endregion