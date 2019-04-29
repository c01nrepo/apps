from badge import oled, btn, wlan, wlanAP
from time import sleep_ms
from random import getrandbits
from uikit import getDualButton,selectVList
import ustruct as struct
#import #opy
import ubinascii


# 3 = king of 1
# 4 = king of 2
# 5 = selection

initBoard =[[1, 0, 1 ,0, 1, 0, 1, 0],
			[0, 1, 0 ,1, 0, 1, 0, 1],
			[1, 0, 1 ,0, 1, 0, 1, 0],
			[0, 0, 0 ,0, 0, 0, 0, 0],
			[0, 0, 0 ,0, 0, 0, 0, 0],
			[0, 2, 0 ,2, 0, 2, 0, 2],
			[2, 0, 2 ,0, 2, 0, 2, 0],
			[0, 2, 0 ,2, 0, 2, 0, 2]]


def drawBoard(board, selx, sely):
	for i in range(7):
		oled.vline(31+i*8 + 8 - 1,0,64,1)
		for j in range(7):
			oled.hline(31,0+i*8 + 8 - 1,64,1)
			pass
	for i in range(8):
		for j in range(8):
			if board[j][i] == 1:
				oled.rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
			elif board[j][i] == 2:
				oled.fill_rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
			elif board[j][i] == 3:
				oled.rect(31 + i*8 + 2, j*8 + 2, 3, 3, 1)
				oled.rect(31 + i*8 + 3, j*8 + 3, 1, 1, 1)
			elif board[j][i] == 4:
				oled.fill_rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
				oled.fill_rect(31 + i*8 + 3, j*8 + 3, 1, 1, 0)
			elif board[j][i] == 5:
				oled.fill_rect(31 + i*8 + 2, j*8 + 2, 3, 3, 1)

			#oled.rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
			#oled.fill_rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
			#oled.fill_rect(31 + i*8 + 1, j*8 + 1, 5, 5, 1)
			#if board[i][j]:
			#oled.fill_circle(32 + i*8 + 3, j*8 + 3, 3)
	if selx >= 0 and sely >= 0:
		oled.fill_rect(31 + selx * 8, sely * 8, 7, 7, 1)

def isRealPiece(num):
	if num <= 0 and num >= 5:
		return False
	else:
		return True

def isEnemy(num1, num2):
	if num1 <= 0 or num1 >= 5:
		return False
	if num2 <= 0 or num2 >= 5:
		return False
	if num1 > 2:
		num1 -= 2
	if num2 > 2:
		num2 -= 2
	if num1 == num2:
		return False
	else:
		return True

def isFriendly(num1, num2):
	if num1 <= 0 or num1 >= 5:
		return False
	if num2 <= 0 or num2 >= 5:
		return False
	if num1 > 2:
		num1 -= 2
	if num2 > 2:
		num2 -= 2
	if num1 == num2:
		return True
	else:
		return False

def isKing(num):
    return num < 5 and num > 2

def canPromote(num, selx, sely):
	if num == 1 and sely == 7:
		return True
	if num == 2 and sely == 0:
		return True
	return False

def getValidMoves(board, startx, starty):
	num = board[starty][startx]
	validMoves = []
	if num == 1: #look down
		for dx in [1, -1]:
			newx = startx + dx
			newy = starty + 1
			if newx < 0 or newy < 0 or newx > 7 or newy > 7:
				continue
			if board[newy][newx] == 0: #empty cell
				validMoves.append((newx, newy))
	elif num == 2: #look up
		for dx in [1, -1]:
			newx = startx + dx
			newy = starty - 1
			if newx < 0 or newy < 0 or newx > 7 or newy > 7: #invalid move
				continue
			if board[newy][newx] == 0: #empty cell
				validMoves.append((newx, newy))

	if not isKing(num): #we just skip one
		for dx in [1, -1]:
			for dy in [1, -1]:
				newx = startx + dx
				newy = starty + dy
				if newx < 0 or newy < 0 or newx > 7 or newy > 7: #invalid move
					continue
				if isEnemy(num, board[newy][newx]):
					enemyx = newx
					enemyy = newy
					newx = newx + dx
					newy = newy + dy
					if newx < 0 or newy < 0 or newx > 7 or newy > 7: #invalid move
						continue
					if board[newy][newx] == 0: #empty cell
						validMoves.append((newx, newy, enemyx, enemyy))

	else:
		for dx in [1, -1]:
			for dy in [1, -1]:
				encounteredEnemy = False
				enemyx = -1
				enemyy = -1
				for dmoves in range(8):
					newx = startx + dx * dmoves
					newy = starty + dy * dmoves
					if newx < 0 or newy < 0 or newx > 7 or newy > 7: #invalid move
						continue
					if isEnemy(num, board[newy][newx]):
						if encounteredEnemy:
							continue
						else:
							encounteredEnemy = True
							enemyx = newx
							enemyy = newy
					if board[newy][newx] == 0:
						if encounteredEnemy:
							validMoves.append((newx, newy, enemyx, enemyy))
						else:
							validMoves.append((newx, newy))
	return validMoves

def flipBoard(board):
	newBoard = [[0 for x in range(8)] for y in range(8)]
	for i in range(8):
		for j in range(8):
			newBoard[i][j] = board[7-i][7-j]
	return newBoard
def startSinglePlayer():
	selx = 0
	sely = 7
	turn = 2 #
	heldDown = False
	board = initBoard
	found = False
	pieceSelected = (-1, -1)
	while True:

		#find the first one if nothing is selected
		if selx == -1 and sely == -1:
			for i in range(8):
				for j in range(8):
					if board[i][j] == turn:
						selx = i
						sely = j
						found = True
						break
				if found:
					break

		oled.fill(0)
		drawBoard(initBoard, selx, sely)
		oled.show()

		if not btn.U.value():
			sely = max(0, sely - 1)
		if not btn.D.value():
			sely = min(7, sely + 1)
		if not btn.L.value():
			selx = max(0, selx - 1)
		if not btn.R.value():
			selx = min(7, selx + 1)


		if not btn.A.value():
            #selecting a piece
			if isFriendly(turn, board[sely][selx]):
				for i in range(8):
					for j in range(8):
						if board[i][j] == 5:
							board[i][j] = 0
				moves = getValidMoves(board, selx, sely)
				if len(moves) == 0:
					continue
				for move in moves:
					x = move[0]
					y = move[1]
					board[y][x] = 5
				pieceSelected = (selx, sely)

            #selecting a movement
			if board[sely][selx] == 5:
				for i in range(8):
					for j in range(8):
						if board[i][j] == 5:
							board[i][j] = 0
				x, y = pieceSelected
				board[sely][selx] = board[y][x]
				board[y][x] = 0

				if canPromote(turn, selx, sely):
					board[sely][selx] += 2

				enemyCaptured = False
				for move in moves:
					if len(move) > 2 and move[0] == selx and move[1] == sely:
						enemyx = move[2]
						enemyy = move[3]
						board[enemyy][enemyx] = 0
						enemyCaptured = True
						break

				if enemyCaptured:
					canCaptureMore = False
					moves = getValidMoves(board, selx, sely)
					for move in moves:
						if len(move) > 2:
							canCaptureMore = True

					if canCaptureMore:
						for move in moves:
							if len(move) > 2:
								x = move[0]
								y = move[1]
								board[y][x] = 5
						pieceSelected = (selx, sely)
					else:
						turn = 3 - turn
				else:
					turn = 3 - turn

		if not btn.B.value():
			for i in range(8):
				for j in range(8):
					if board[i][j] == 5:
						board[i][j] = 0
		holdCnt = 0
		while((not btn.U.value()) or (not btn.D.value()) or (not btn.L.value()) or (not btn.R.value()) or (not btn.A.value()) or (not btn.B.value())):
			sleep_ms(10)
			holdCnt += 1
			if heldDown:
				if holdCnt >= 5:
					break
			else:
				if holdCnt >= 50:
					heldDown = True

		if holdCnt < 5:
			heldDown = False


def numToSignedHex(num):
	if num < 0:
		hex = 256+num
	else:
		hex = num
	return ubinascii.hexlify(chr(int(hex)))

def signedHexToNum(hex):
	val = ord(ubinascii.unhexlify(hex))
	if val > 128:
		return val-256
	else:
		return val

def numToBin(num):
	if num < 0:
		bin = 256+num
	else:
		bin = num
	return chr(int(bin))

def binToNum(bin):
	try:
		(val, ) = struct.unpack('B', bin)
	except:
		val = bin
	#val = bin
	if val > 128:
		return val-256
	else:
		return val

def boardToBinary(board):
	bin = ""
	for i in range(8):
		for j in range(8):
			bin += numToBin(board[i][j])
	return bin

def binaryToBoard(bin):
	board = [[0 for x in range(8)] for y in range(8)]
	for i in range(8):
		for j in range(8):
			board[i][j] = binToNum(bin[i*8+j])
	return board

#packet:
# [OP] [DATA]
# ID: 0 ping
# [0]
# ID: 1 gameState
# [1] [8x8 board]
# ID: 2 changeTurn
# [2] [turnNum]
def isCurrentTurn(turnNum, isClient):
	if turnNum == 1 and isClient == True:
		return True
	elif turnNum == 2 and isClient == False:
		return True
	else:
		return False
def startSession(isClient):
	import uselect
	poller = uselect.poll()
	poller.register(gameSocket, uselect.POLLIN)
	heldDown = False
	turn = 2
	if isClient:
		board = [[0 for x in range(8)] for y in range(8)]
		selx = 0
		sely = 0
	else:
		board = initBoard
		selx = 0
		sely = 7
	found = False
	pieceSelected = (-1, -1)


	if not isClient:
		for i in range(10):
			gameSocket.sendto(numToBin(1) + boardToBinary(board), clientAddr)



	while True:
		while poller.poll(1):
			data, _ = gameSocket.recvfrom(200)
			cmd = binToNum(data[:1])
			data = data[1:]

			if cmd == 1:
				board = binaryToBoard(data)
			elif cmd == 2:
				turn = binToNum(data)

		'''
		for i in range(8):
			for j in range(8):
				if board[i][j] == turn:
					selx = i
					sely = j
					found = True
					break
			if found:
				break
		'''

			#board = binaryToBoard(boardData[1:])

		#find the first one if nothing is selected

		if isClient:
			boardDraw = flipBoard(board)
		else:
			boardDraw = board

		oled.fill(0)
		if isCurrentTurn(turn, isClient):
			if isClient:
				drawBoard(boardDraw, 7-selx, 7-sely)
			else:
				drawBoard(boardDraw, selx, sely)
			oled.text("GO", 102, 52, 1)
		else:
			drawBoard(boardDraw, -1, -1)
		oled.show()

		if isClient:
			if not btn.U.value():
				sely = min(7, sely + 1)
			if not btn.D.value():
				sely = max(0, sely - 1)
			if not btn.L.value():
				selx = min(7, selx + 1)
			if not btn.R.value():
				selx = max(0, selx - 1)
		else:
			if not btn.U.value():
				sely = max(0, sely - 1)
			if not btn.D.value():
				sely = min(7, sely + 1)
			if not btn.L.value():
				selx = max(0, selx - 1)
			if not btn.R.value():
				selx = min(7, selx + 1)


		if (not btn.A.value()) and isCurrentTurn(turn, isClient): #turn locked
            #selecting a piece
			if isFriendly(turn, board[sely][selx]):
				for i in range(8):
					for j in range(8):
						if board[i][j] == 5:
							board[i][j] = 0
				moves = getValidMoves(board, selx, sely)
				if len(moves) == 0:
					continue
				for move in moves:
					x = move[0]
					y = move[1]
					board[y][x] = 5
				pieceSelected = (selx, sely)

            #selecting a movement
			if board[sely][selx] == 5:
				for i in range(8):
					for j in range(8):
						if board[i][j] == 5:
							board[i][j] = 0
				x, y = pieceSelected
				board[sely][selx] = board[y][x]
				board[y][x] = 0

				if canPromote(turn, selx, sely):
					board[sely][selx] += 2

				enemyCaptured = False
				for move in moves:
					if len(move) > 2 and move[0] == selx and move[1] == sely:
						enemyx = move[2]
						enemyy = move[3]
						board[enemyy][enemyx] = 0
						enemyCaptured = True
						break

				if enemyCaptured:
					canCaptureMore = False
					moves = getValidMoves(board, selx, sely)
					for move in moves:
						if len(move) > 2:
							canCaptureMore = True

					if canCaptureMore:
						for move in moves:
							if len(move) > 2:
								x = move[0]
								y = move[1]
								board[y][x] = 5
						pieceSelected = (selx, sely)
					else:
						turn = 3 - turn
						for i in range(20):
							if isClient:
								gameSocket.send(numToBin(1) + boardToBinary(board))
								gameSocket.send(numToBin(2) + numToBin(turn))
							else:
								gameSocket.sendto(numToBin(1) + boardToBinary(board), clientAddr)
								gameSocket.sendto(numToBin(2) + numToBin(turn), clientAddr)
				else:
					turn = 3 - turn
					for i in range(20):
						if isClient:
							gameSocket.send(numToBin(1) + boardToBinary(board))
							gameSocket.send(numToBin(2) + numToBin(turn))
						else:
							gameSocket.sendto(numToBin(1) + boardToBinary(board), clientAddr)
							gameSocket.sendto(numToBin(2) + numToBin(turn), clientAddr)

		if not btn.B.value():
			for i in range(8):
				for j in range(8):
					if board[i][j] == 5:
						board[i][j] = 0
		holdCnt = 0
		while((not btn.U.value()) or (not btn.D.value()) or (not btn.L.value()) or (not btn.R.value()) or (not btn.A.value()) or (not btn.B.value())):
			sleep_ms(10)
			holdCnt += 1
			if heldDown:
				if holdCnt >= 5:
					break
			else:
				if holdCnt >= 50:
					heldDown = True

		if holdCnt < 5:
			heldDown = False


		#if isCurrentTurn(turn, isClient):
		#	boardSanitized = [[0 for x in range(8)] for y in range(8)]
		#	for i in range(10):
		#		for j in range(10):
		#			if board[i][j] < 5:
		#				boardSanitized[i][j] = board[i][j]
		#	if isClient:
		#		gameSocket.send(numToBin(1) + boardToBinary(boardSanitized))
		#		gameSocket.send(numToBin(2) + numToBin(turn))
		#	else:
		#		gameSocket.sendto(numToBin(1) + boardToBinary(boardSanitized), clientAddr)
		#		gameSocket.sendto(numToBin(2) + numToBin(turn), clientAddr)

def startMultiPlayer(isClient):
	import network
	import usocket as socket
	global gameSocket, gameSocket, clientAddr
	import uos
	prefixlen = len("CoinGame-Checkers")
	if not isClient:
		gameName = ubinascii.hexlify(uos.urandom(4)).upper().decode()
		wlanAP.active(True)         # activate the interface
		wlanAP.config(essid='CoinGame-Checkers-' + gameName) # set the ESSID of the access point
		#ap.setNoDelay(1);

		sleep_ms(1000)
		gameSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		gameSocket.bind(('', 52354))


		oled.fill(0)
		oled.hctext("Waiting", 32-12, 1)
		oled.hctext("Checkers", 32-4, 1)
		oled.hctext("Game: " + gameName, 32+4, 1)
		oled.show()
		data, clientAddr = gameSocket.recvfrom(1)

	else:
		#wlan = network.WLAN(network.STA_IF) # create station interface
		wlan.active(True)
		dotcnt = 0
		validGames = []
		while len(validGames) == 0:
			oled.fill(0)
			oled.hctext("Scanning" + "."*(dotcnt+1), 32-4, 1)
			oled.show()
			dotcnt = (dotcnt+1)%3
			wlan.active(True)
			scanResults = wlan.scan()
			for ap in scanResults:
				ssid, bssid, channel, RSSI, authmode, hidden = ap
				if ssid.startswith("CoinGame-Checkers-"):
					validGames.append(ssid[18:])

		ap_name = validGames[selectVList("Select Game", validGames, 0)].decode()
		wlan.active(True)
		wlan.connect('CoinGame-Checkers-' + ap_name, '') # connect to an AP
		#wlan.setNoDelay(1);
		dotcnt = 0
		while not wlan.isconnected():
			oled.fill(0)
			oled.hctext("Connecting" + "."*(dotcnt+1), 22, 1)
			#oled.hctext("Channel: " + str(wlan.config("channel")), 32, 1)
			oled.hctext("Game: " + ap_name, 42, 1)
			oled.show()
			sleep_ms(500)
			dotcnt = (dotcnt+1)%3

		oled.fill(0)
		oled.hctext("WIFI: OK", 32, 1)
		oled.hctext("Game: ...", 42, 1)
		oled.show()

		gameSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockaddr = socket.getaddrinfo('192.168.4.1', 52354)[0][-1]
		gameSocket.connect(sockaddr)
		gameSocket.send(numToBin(0))
		#TODO: exchange names between devices

		oled.fill(0)
		oled.hctext("CONNECTED", 32, 1)
		oled.show()

	startSession(isClient)

def app_start():

	isMulti = getDualButton("CHECKERS", "SINGLE", "MULTI", 0)

	if not isMulti:
		startSinglePlayer()
	else:
		while(not btn.A.value()):
			sleep_ms(10)

		isClient = getDualButton("CHECKERS", "HOST", "CLIENT", 0)
		while(not btn.A.value()):
			sleep_ms(10)
		startMultiPlayer(isClient)
	return 0

app_start() #remove
