from tkinter import *
from PIL import Image, ImageTk
import random
import os
import sys
from Skull import Skull
from factory import Factory

FRAMERATE = 20
SCORE = -1
SKULL_Y = 200
PIPE_X = 550
PIPE_HOLE = 0
BEST_SCORE = 0
COLLISION = False

def center(toplevel):
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2 - 35
	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def checkScore():
	global BEST_SCORE
	if os.path.isfile("score.txt"):
		scoreFile = open('score.txt')
		BEST_SCORE = int(scoreFile.read())
		scoreFile.close()
	else:
		scoreFile = open('score.txt', 'w')
		scoreFile.write(str(BEST_SCORE))
		scoreFile.close()

def genPipeHole():
	global PIPE_HOLE
	global SCORE
	global FRAMERATE

	SCORE += 1
	w.itemconfig(score_w, text=str(SCORE))
	PIPE_HOLE = random.randint(90, 500)
	if SCORE + 1 % 7 == 0 and SCORE != 0: 
		FRAMERATE-=1

def birdUp(event = None):
	global SKULL_Y
	global up_count
	global COLLISION

	if not COLLISION:
		SKULL_Y -= 20
		if SKULL_Y <= 0: SKULL_Y = 0
		w.coords(bird, 100, SKULL_Y)
		if up_count < 5:
			up_count += 1
			main.after(FRAMERATE, birdUp)
		else:
			up_count = 0

def birdDown():
	global SKULL_Y

	SKULL_Y += 8
	if SKULL_Y >= 700: SKULL_Y = 700
	w.coords(bird, 100, SKULL_Y)
	main.after(FRAMERATE,birdDown)

def pipesMotion():
	global PIPE_X
	global PIPE_HOLE
	global COLLISION

	PIPE_X -= 3
	#w.coords(pipeUp, PIPE_X, 0, PIPE_X + 100, PIPE_HOLE)
	w.coords(pipeDown, PIPE_X, PIPE_HOLE + 200, PIPE_X + 100, 700)
	w.move(pipeUp, PIPE_X, 0)

	
	if PIPE_X < -100: 
		PIPE_X = 550
		genPipeHole()

	if not COLLISION: main.after(FRAMERATE, pipesMotion)

def restart_program():
	python = sys.executable
	os.execl(python, python, *sys.argv)
def endGameScreen():
	#global endScore
	#global endBest

	endScore = w.create_text(15, 200, text="Your score: " + str(SCORE), font='Helvetica 40 bold', fill='#ffffff', anchor=W)
	endBest = w.create_text(15, 280, text="Best score: " + str(BEST_SCORE), font='Helvetica 40 bold', fill='#ffffff', anchor=W)
	btn = Button(w, text = "Restart", command=restart_program)
	w.create_window(500,650, window=btn)

def endGame():
	global BEST_SCORE
	global COLLISION
	global FRAMERATE

	COLLISION = True
	FRAMERATE = 10
	if SCORE > BEST_SCORE:
		BEST_SCORE = SCORE
		scoreFile = open('score.txt', 'w')
		scoreFile.write(str(BEST_SCORE))
		scoreFile.close()
	endGameScreen()
def detectCollision():
	global COLLISION

	if not COLLISION:
		if (PIPE_X < 150 and PIPE_X + 100 >= 55) and (SKULL_Y < PIPE_HOLE + 45 or SKULL_Y > PIPE_HOLE + 175):
			endGame()
		else:
			main.after(1, detectCollision)

		if SKULL_Y < 20 or SKULL_Y > 680:
			endGame()

def ConfigMain(main):
	main.resizable(width=False, height=False)
	main.title("Flappy Skull")
	main.geometry('550x700')


if __name__ == "__main__":
	up_count = 0
	endBest = endScore = None
	checkScore()
	main = Tk()
	ConfigMain(main)
	center(main)

	bg = PhotoImage(file="images/background.png")
	w = Canvas(main, width=550, height=700)
	w.pack(fill="both", expand=False)
	w.create_image(0, 0, image=bg, anchor="nw")
	score_w = w.create_text(15, 45, text="0", font='Helvetica 40 bold', fill='#ffffff', anchor=W)

	skullInstance = Skull.getInstance()
	birdImg = skullInstance.getSkull()
	bird = w.create_image(80, SKULL_Y, image=birdImg)

	pipetemp = Factory.create("up",w, PIPE_X, PIPE_HOLE)
	pipeUp = pipetemp.createPipe()
	pipeDown = Factory.create("down", w, PIPE_X, PIPE_HOLE)
	genPipeHole()

	main.after(FRAMERATE, birdDown)
	main.after(FRAMERATE, pipesMotion)
	main.after(1, detectCollision)
	main.bind("<space>", birdUp)
	main.mainloop()
