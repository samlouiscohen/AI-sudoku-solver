import sys
from Queue import *
import copy
import time
from ac3 import *
from bts import *


class Board:
	"""Class to represent the sudoku board"""

	def __init__(self, inputBoard):
		self.dict = dict()
		self.inputBoard = inputBoard


	def setDictionary(self):
		"""
		Class method to set the dictionary representing each square and its
		 domain of potential values.
		"""

		lenBoard = len(self.inputBoard)
		lenRow = 9

		#Set each box (A1-I9) to its corresponding domain as specified in input
		for i in range(1, 10):
			for j in range(1, 10):

				if i == 1:
					self.dict["A" + str(j)] = [self.inputBoard[0*lenRow + j-1]]

				elif i == 2:
					self.dict["B" + str(j)] = [self.inputBoard[1*lenRow + j-1]]
				
				elif i == 3:
					self.dict["C" + str(j)] = [self.inputBoard[2*lenRow + j-1]]

				elif i == 4:
					self.dict["D" + str(j)] = [self.inputBoard[3*lenRow + j-1]]

				elif i == 5:
					self.dict["E" + str(j)] = [self.inputBoard[4*lenRow + j-1]]

				elif i == 6:
					self.dict["F" + str(j)] = [self.inputBoard[5*lenRow + j-1]]

				elif i == 7:
					self.dict["G" + str(j)] = [self.inputBoard[6*lenRow + j-1]]

				elif i == 8:
					self.dict["H" + str(j)] = [self.inputBoard[7*lenRow + j-1]]

				elif i == 9:
					self.dict["I" + str(j)] = [self.inputBoard[8*lenRow + j-1]]


		#For any blank('0') box create a full 1-9 domain
		for key in self.dict:

			if self.dict[key] == ['0']:
				self.dict[key] = [str(i) for i in range(1,10)]



#Running Driver
argList = sys.argv
boardObj = Board(argList[1])
boardObj.setDictionary()

#Construct boards squares and peers for use in both methods
squares, peers = buildSquaresAndPeers()

startTime = time.clock()

solvedBoardString = backTrackingSearch(boardObj, squares, peers)
print(solvedBoardString)
print("Time taken: "+str(time.clock() - startTime))

outFile = open('output.txt', 'w')
outFile.write(solvedBoardString)
outFile.close()



# y = 0

# with open("assignment4/sudokus_start.txt") as f:
# 	for line in f:
# 		y = y+1
# 		startTime = time.clock()
# 		boardString = line[0:81] #Necessary>???????????
# 		board = Board(boardString)
# 		board.setDictionary()

# 		ans1 = backTrackingSearch(board, squares, peers)
# 		print(ans1)

# 		print("Time taken: "+str(time.clock() - startTime))


# print y














