import tkinter as tk

class OthelloGame:
    def __init__(self):
        self._columns = 8
        self._rows = 8
        self._root = tk.Toplevel()
        self._root.geometry("650x650") 
        self._root.resizable(False, False)  
        self._canvas = tk.Canvas(master=self._root, height=500, width=500, background='green')
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind('<Configure>', self.draw_handler)

    def run(self):
        self._root.mainloop()

    def draw(self):
        column_width = self._canvas.winfo_width() / self._columns
        row_height = self._canvas.winfo_height() / self._rows
        for x in range(self._columns):
            for y in range(self._rows):
                x1 = x * column_width
                y1 = y * row_height
                x2 = x1 + column_width
                y2 = y1 + row_height
                r = self._canvas.create_rectangle(x1, y1, x2, y2, fill='Green')
                self._canvas.tag_bind(r, '<ButtonPress-1>', self.clicked)

    def damier(width, height, size_case, rayon):
##### Création du rectangle général #####
        can.create_rectangle(0, 0, width, height,fill="forest green")
  
##### Quadrillage #####
        for x in range(size_case, width, size_case):
            can.create_line(x, 0, x, height)
        for y in range(size_case, height, size_case):
                can.create_line(0, y, width, y)
  
        pions = ((175, 175, "white"), (225, 175, "black"),
                (175, 225, "black"), (225, 225, "white"))
        for x_center, y_center, color in pions:
            can.create_oval(x_center - rayon, y_center - rayon,
                        x_center + rayon, y_center + rayon, fill=color)
        


    def clicked(self, event: tk.Event):
        x = event.x
        y = event.y
        coordinates = self._canvas.coords("current")
        print(coordinates)

    def draw_handler(self, event):
        self.draw()


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
        othello_game = OthelloGame()
        othello_game.run()

    def start_pva_game(self):
        othello_game = OthelloGame()
        othello_game.run()

if __name__ == "__main__":
    othello_page = OthelloPage()
    othello_page.run()
