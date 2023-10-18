from tkinter import Canvas, PhotoImage, Label
from PIL import Image
class PipeUp:

    def __init__(self, canvas, X, hole):
        self.pipe = canvas.create_rectangle(X, 0, X + 100, hole, fill="#74BF2E", outline="#74BF2E")
    #def __new__(cls, canvas, X, hole):
     #   return canvas.create_rectangle(X, 0, X + 100, hole, fill="#74BF2E", outline="#74BF2E")
    def createPipe(self):
        return self.pipe

class PipeDown:
    def __new__(cls, canvas, X, hole):
        return canvas.create_rectangle(X, hole + 200, X + 100, 700, fill="#74BF2E", outline="#74BF2E")

class Factory:
    def create(pipeDirection, canvas, X, hole):
        directions = {
            "up" : PipeUp(canvas, X, hole),
            "down" : PipeDown(canvas, X, hole)
        }
        return directions[pipeDirection]


