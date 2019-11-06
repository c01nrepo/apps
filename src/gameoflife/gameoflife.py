from time import sleep_ms,time
from badge import oled,np,connectWifi,btn
from utils import hsv_to_rgb
from random import random,randint
import math, utime

blkSize = 3
boardWidth = int(128/blkSize)
boardHeight = int(64/blkSize)
board1 = [[0 for x in range(boardWidth)] for y in range(boardHeight)]
board2 = [[0 for x in range(boardWidth)] for y in range(boardHeight)]
boardNum = 0

def drawBoard():
	oled.fill(0)
	for i in range(boardHeight):
		for j in range(boardWidth):
			oled.fill_rect(j*blkSize, i*blkSize, blkSize, blkSize, board1[i][j])
	oled.show()


lookup = [[0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0]]

def tickBoard():
	global board1, board2, lookup
	for i in range(boardHeight):
		for j in range(boardWidth):
			live = 0
			try:
				live += board1[i+1][j]
				live += board1[i-1][j]
				live += board1[i][j+1]
				live += board1[i][j-1]
				live += board1[i-1][j+1]
				live += board1[i+1][j+1]
				live += board1[i-1][j-1]
				live += board1[i+1][j-1]
			except:
				pass
			board2[i][j] = lookup[board1[i][j]][live]
	board1, board2 = board2, board1
	#for i in range(boardHeight):
	#    for j in range(boardWidth):
	#        board1[i][j] = board2[i][j]

def app_start():
	global board1
	board1[boardHeight//2][boardWidth//2] = 1
	board1[boardHeight//2-1][boardWidth//2] = 1
	board1[boardHeight//2+1][boardWidth//2] = 1
	board1[boardHeight//2][boardWidth//2-1] = 1
	board1[boardHeight//2-1][boardWidth//2+1] = 1
	timing = 0
	while btn.B.value():
		if not btn.A.value():
			board1 = [[0 for x in range(boardWidth)] for y in range(boardHeight)]
			board2 = [[0 for x in range(boardWidth)] for y in range(boardHeight)]
			for r in range(randint(10,int(boardHeight*boardWidth*0.6))): board1[randint(0,boardHeight-1)][randint(0,boardWidth-1)] = 1
			sleep_ms(50)
		drawBoard()
		tickBoard()