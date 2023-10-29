import tkinter as tk
import random

MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

tiles_color = ['black', 'white']
class OthelloGame:

    board = [[0, 0, 0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 2, 1, 0, 0, 0],
         [0, 0, 0, 1, 2, 0, 0, 0], 
         [0, 0, 0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0, 0, 0, 0]]
    
    def __init__(self, pvp_mode=True):
        self.n = 8
        self._columns = self.n
        self._rows = self.n
        self._root = tk.Toplevel()
        self._root.geometry("1050x650") 
    
        self._board_frame = tk.Frame(self._root)
        self._board_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.create_new_frame()

        self._board_frame = tk.Frame(self._root)
        self._board_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self._rows_frame = tk.Frame(self._board_frame)
        self._rows_frame.pack(side=tk.LEFT)
        self._columns_frame = tk.Frame(self._board_frame)
        self._columns_frame.pack(side=tk.TOP)

        self._canvas = tk.Canvas(master=self._root, height=850, width=650, background='green')
        self._canvas.pack()

        self._canvas.bind('<Configure>', self.draw_handler)             
        self.column_width = 0
        self.row_height = 0
        self.current_player = 0
        self.pvp_mode = pvp_mode
        self.num_tiles = [2, 2]        
        self.move = ()

        self.column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def clicked(self, event: tk.Event):
        x = event.x
        y = event.y
        row, col = self.convert_xy_to_rowcol(x, y)
        self.move = (row, col)
        self.play()

    def create_new_frame(self):
        new_frame = tk.Frame(self._root)
        new_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        label = tk.Label(new_frame, text="New Frame")
        label.pack()
        button1 = tk.Button(new_frame, text="Restart", command=self.restart)
        button1.pack()
        button2 = tk.Button(new_frame, text="Newgame")
        button2.pack()

    def restart(self):
        self.num_tiles = [2, 2]        
        self.move = ()
        self.current_player = 0
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0]]
        self.draw()
        self.update_board()
        self.display_available_move()
        

#เดี๋ยวมาแก้
    def draw(self):
        self._canvas.delete(tk.ALL)
        self.column_width = self._canvas.winfo_width() / self._columns
        self.row_height = self._canvas.winfo_height() / self._rows
        for x in range(self._columns):
            for y in range(self._rows):
                x1 = x * self.column_width
                y1 = y * self.row_height
                x2 = x1 + self.column_width
                y2 = y1 + self.row_height
                r = self._canvas.create_rectangle(x1, y1, x2, y2, fill='Green')
                self._canvas.tag_bind(r, '<ButtonPress-1>', self.clicked)

        for y in range(self._rows):
            label = str(y + 1)
            y1 = y * self.row_height
            y2 = y1 + self.row_height
            label_x = 10
            label_y = (y1 + y2) / 2
            self._canvas.create_text(label_x, label_y, text=label, font=('Arial', 14), anchor='e')

        
        for x in range(self._columns):
            label = self.column_labels[x]
            x1 = x * self.column_width
            x2 = x1 + self.column_width
            label_x = (x1 + x2) / 2
            label_y = 10
            self._canvas.create_text(label_x, label_y, text=label, font=('Arial', 14))

    def draw_handler(self, event):
        self.draw()
        self.update_board()
        self.display_available_move()

    def convert_xy_to_rowcol(self, x, y):   
        col = int(x / self.column_width)
        row = int(y / self.row_height)
        # print(f'({row}, {col})')
        return row, col

    def flip_tiles(self):
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        self.set_tile_color(self.move, tiles_color[self.current_player])
                        self.update_board()
                        self._root.update_idletasks()
                        self._root.after(300)
                        i += 1
        if not self.pvp_mode:
            self.display_available_move()
        print(f"score [black, white] = {self.num_tiles}")

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0, 1) and self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False

    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves

    def is_legal_move(self, move):
        if move != () and self.is_valid_coord(move[0], move[1]) and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False
    
    def is_valid_coord(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False

    def make_move(self):
        if self.is_legal_move(self.move):
            print(f"{tiles_color[self.current_player]} select a move at", self.column_labels[self.move[1]] + str(self.move[0] + 1))
            self.clear_available_moves()
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.set_tile_color(self.move, tiles_color[self.current_player])
            self.update_board()
            self._root.update_idletasks()
            self._root.after(300)
            self.flip_tiles()

    def set_tile_color(self, position, color):
        row, col = position
        x1 = col * self.column_width
        y1 = row * self.row_height
        x2 = x1 + self.column_width
        y2 = y1 + self.row_height

        square_center_x = (x1 + x2) / 2
        square_center_y = (y1 + y2) / 2

        circle_radius = min(self.column_width, self.row_height) / 4  # Adjust the radius as needed

        circle_x1 = square_center_x - circle_radius
        circle_y1 = square_center_y - circle_radius
        circle_x2 = square_center_x + circle_radius
        circle_y2 = square_center_y + circle_radius

        if color != 0:
            self._canvas.create_oval(circle_x1, circle_y1, circle_x2, circle_y2, fill=color, outline=color)

    def update_board(self):         #update board whenever the size of window change
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] != 0:
                    self.set_tile_color((row, col), tiles_color[self.board[row][col]-1])

    def display_available_move(self):
        if self.pvp_mode == True or self.current_player == 0:
            # print(f"available move for {self.current_player} is ", self.get_legal_moves())
            for position in self.get_legal_moves():
                row, col = position
                x1 = col * self.column_width
                y1 = row * self.row_height
                x2 = x1 + self.column_width
                y2 = y1 + self.row_height

                square_center_x = (x1 + x2) / 2
                square_center_y = (y1 + y2) / 2

                circle_radius = min(self.column_width, self.row_height) / 8  # Adjust the radius as needed
                circle_x1 = square_center_x - circle_radius
                circle_y1 = square_center_y - circle_radius
                circle_x2 = square_center_x + circle_radius
                circle_y2 = square_center_y + circle_radius

                c = self._canvas.create_oval(circle_x1, circle_y1, circle_x2, circle_y2, fill='yellow', outline='yellow', tags="available_move")
                self._canvas.tag_bind(c, '<ButtonPress-1>', self.clicked)

    def clear_available_moves(self):
        self._canvas.delete("available_move")
    
    def make_random_move(self):
        moves = self.get_legal_moves()
        if moves:
            self.move = random.choice(moves)
            self.make_move()

    def run(self):
        self._root.mainloop()

        # if self.current_player not in (0, 1):
        #     print('Error: unknown player. Quit...')
        #     return
        # 
        # self.current_player = 0
        # print('Your turn.')

    def play(self):
        # Play the user's turn

        if self.has_legal_move() and self.current_player == 0:
            if self.is_legal_move(self.move):
                self.make_move()
            else:
                return
            if not self.pvp_mode:
                self.current_player = 1
            else:
                self.current_player = 1
                self.display_available_move()
                print(f"{tiles_color[self.current_player]}\'s turn")

        if self.pvp_mode == False:
            # Play the computer's turn
            while True:
                self.current_player = 1
                if self.has_legal_move():
                    print('Computer\'s turn.')
                    self.make_random_move()
                    self.current_player = 0
                    if self.has_legal_move():
                        break
                    print("Player have no available move, computer\'s turn")
                else:
                    break
        elif self.has_legal_move() and self.current_player == 1:        #player 2 (white) turn
                if self.is_legal_move(self.move):
                    self.make_move()
                else:
                    return
                self.current_player = 0
                self.display_available_move()
                print("---------------")
                print(f"{tiles_color[self.current_player]}\'s turn")
        
        if not self.has_legal_move() and self.pvp_mode == True and sum(self.num_tiles) != self.n ** 2:  #if there's no available move for player switch to another player
            print(f"Player {tiles_color[self.current_player]} has no available moves.")
            self.current_player = (self.current_player + 1) % 2
            print(f"{tiles_color[self.current_player]}\'s turn")
            self.display_available_move()
                
        # Switch back to the user's turn
        if not self.pvp_mode:
            self.current_player = 0
            print("---------------")
            print("Player\'s turn")
            self.display_available_move()
        
        # Check whether the game is over
        if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
            print(f'Color {tiles_color[self.current_player]} won the game with score {self.num_tiles}')
            # self.report_result()
            # name = input('Enter your name for posterity\n')
            # if not score.update_scores(name, self.num_tiles[0]):
                # print('Your score has not been saved.')
            # print('Thanks for playing Othello!')
            # close = input('Close the game screen? Y/N\n')
            # if close == 'Y':
            #     turtle.bye()
            # elif close != 'N':
            #     print('Quit in 3s...')
            #     turtle.ontimer(turtle.bye, 3000)
        # else:
        #     print('Your turn.')
            # turtle.onscreenclick(self.play)

class OthelloPage:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Othello")
        self._root.geometry("650x650")  
        self._root.resizable(False, False)  

        topic_label = tk.Label(self._root, text="Othello", font=("Arial", 50))
        topic_label.pack(pady=150)

        button_frame = tk.Frame(self._root)
        button_frame.pack()

        pvp_button = tk.Button(button_frame, text="Player vs. Player (PVP)", command=self.start_pvp_game)
        pva_button = tk.Button(button_frame, text="Player vs. AI (PVA)", command=self.start_pva_game)

        pvp_button.pack(side="left", padx=10)
        pva_button.pack(side="left", padx=10)

    def run(self):
        self._root.mainloop()

    def start_pvp_game(self):
        othello_game = OthelloGame(pvp_mode = True)
        # print(othello_game.pvp_mode)
        othello_game.restart()
        othello_game.run()

    def start_pva_game(self):
        othello_game = OthelloGame(pvp_mode = False)
        # print(othello_game.pvp_mode)
        othello_game.restart()
        othello_game.run()

if __name__ == "__main__":
    othello_page = OthelloPage()
    othello_page.run()