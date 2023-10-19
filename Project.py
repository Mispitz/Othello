import tkinter


class RA:
    def __init__(self):
        self._columns = 8
        self._rows = 8
        self._root = tkinter.Tk()
        self._canvas = tkinter.Canvas(master = self._root,
                                      height = 500, width = 500,
                                      background = 'green')
        self._canvas.pack(fill = tkinter.BOTH, expand = True)
        self._canvas.bind('<Configure>',self.draw_handler)


    def run(self):
        self._root.mainloop()

    def draw(self):
        for c in range(self._columns):
            for r in range(self._rows):
                x1 = c * (column_width)
                y1 = r * (row_height)
                x2 = x1 + (column_width)
                y2 = y1 + (row_height)

    def clicked(self,event: tkinter.Event):
        x = event.x
        y = event.y
        coordinates = self._canvas.coords("current")
        print(coordinates)

    def draw(self):
        self._canvas.delete(tkinter.ALL)
        column_width = self._canvas.winfo_width()/self._columns
        row_height = self._canvas.winfo_height()/self._rows
        for  x in range(self._columns):
            for y in range(self._rows):
                x1 = x * column_width
                y1 = y * row_height
                x2 = x1 + column_width
                y2 = y1 + row_height
                r = self._canvas.create_rectangle(x1,y1,x2,y2,fill = 'Green')
                self._canvas.tag_bind(r,'<ButtonPress-1>',self.clicked)

                self._canvas.create_rectangle(x1,y1,x2,y2)
        self._canvas.bind('<Configure>',self.draw_handler)


    def draw_handler(self,event):
        self.draw()


r = RA()
r.run()

 
