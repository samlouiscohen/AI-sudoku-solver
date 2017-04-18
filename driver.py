import sys
from Queue import *
import copy

"""
Notes:
- 27 constraints to sudoku

- Variables are the "squares"-- A1, A2,...

- Domains are the values that the squares that the squares can take on: 1-9

- Constraints are: permuation of 1-9 in each row, column, and box


**Further strategies:

1) For next choice, choose the variable with the fewest legal states
 (smallest domain).

2) Pick least constraining values (Ones that least reduce domains of others)

3) Forward Checking: Heuristic to tell if eventual failure down a certain path.

"""




class Board:
	"""Class to represent the """

	def __init__(self, inputBoard):
		self.dict = dict()
		self.inputBoard = inputBoard


	def setDictionary(self):

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






def cross(A, B):
	"Cross product of elements in A and elements in B."
	return [a+b for a in A for b in B]


def ac3(board):
	""" """
	#print(board.dict,"-------")
	digits   = "123456789"
	rows     = "ABCDEFGHI"
	cols     = digits


	#List of all labeled "squares": 'A1', 'A2', ... ,'I9'
	squares  = cross(rows, cols)

	#List of "units", where a unit is a (column, row, box) that needs
	# all diff numbers 1-9 in each of its squares
	unitlist = ([cross(rows, c) for c in cols] +
				[cross(r, cols) for r in rows] +
	            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

	#Dictionary to give all units that a particular square lives in
	units = dict((s, [u for u in unitlist if s in u]) for s in squares)
	
	#Dictionary to tell you all "peers" of a given sqaure-- peers have to be different than the square
	peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)

	queueOfArcs = Queue()

	#Initialize queue with all arcs
	for s in squares:

		for peer in peers[s]:
			# Example: ('I9', 'E9')
			arc = (s, peer)

			queueOfArcs.put(arc)

	#print(queueOfArcs.qsize())


	while queueOfArcs.qsize() != 0:
		arc = queueOfArcs.get()
		#print(arc)
		square = arc[0]
		peer = arc[1]

		if revise(square, peer, board):

			domainI = board.dict[arc[0]]

			#Deleted too much without finding a solution (Can't be solved)
			if len(domainI) == 0:
				#print(domainI)
				return False

			peers[square].remove(peer)

			for neighbor in peers[square]:
				queueOfArcs.put((neighbor, square))

	#Build output string:
	outBoard = ""

	for square in squares:
		#print board.dict[square]
		if len(board.dict[square]) != 1:
			return True

	for square in squares:
		outBoard+=board.dict[square][0]
	print(outBoard)

	return True





def revise(square, peer, board):
	""" Returns True if we revise the domain of the square based on a peer"""

	revised = False

	domainI = board.dict[square]


	domainJ = board.dict[peer]

	passInner = False

	#Check each value in the domain of the square:
	for x in domainI:
		passInner = False
		# If there exists no y in domainJ that allows (x,y) to satisfies the constraint:
		# (So if there is no y different from the x then delete the x & revised = True)
		for y in domainJ:
			#If there is a single y thats different than x, then we can move on
			if x!=y:
				passInner = True
				break
		if not passInner:
			#If we went through all y with none different then delete the x:
			domainI.remove(x)
			revised = True

	return revised


	# #Check to see that the domains have different values-- allow for this combo
	# for x in domainI:

	# 	for y in domainJ:

	# 		if y != x:
	# 			revised = True
	# 			#return revised





	# 	#Got here so there are no different pairings between the two domains
	# 	#There does not exist a y in the domain of J that is not equal to x

	# 	#Delete x from domainI
	# 	#print("y: ",y)


	# 	#print(domainI)
	# 	domainI.remove(x)
	# 	#print(domainI)
	# 	#xrevised = True

	# 	return revised

		









def backTrackingSearch(board):
	"""Returns a solution or failure """
	return backTrack()


def backTrack():
	"""
	Algorithm:
	Visit each empty cell and try the next possible value in the cells domain,
	Whenever a conflict for the given value is apparent, then try the next value
	in the domain. 

	If it has exhausted all the values in the domain, it tracks
	back to the previously visited cell and tries new values.

	("Track Back" is done recurisively by returning False to the calling function)

	This will recurisively call until all cells are filled with no conflicts.

	"""

	#Base Case: Return solution board if assignment worked and is complete
	assignedBoard = assignmentComplete(board)
	if assignedBoard:
		return assignedBoard #a string representation of complete sudoku board

	aSquare = getNextEmptySquare() 

	domainOfSquare = board.dict[square]
	

	#----------------------------
	for value in domainOfSquare:
		#Assign this value to the square and see if contraints are violated

		#If any constraints with peers are violated, try next value
		for peer in peers[aSquare]:
			passThisPeer = False

			peerDomain = board.dict[peer]

			#needs to be at least one x != value to pass this peer constraint
			for x in peerDomain:

				if value != x:
					passThisPeer = True
					break

			if passThisPeer == False:
				#Have to assign a new value to square and restart
				break
			else: #This peer satisfied binary constraint with the square
				pass




def getNextEmptySquare(squares, assigned):
	"""Return the first non-assigned square it iterates over."""

	for square in squares:
		if not assigned[square]:
			return square



def setModifiableSquareList(squares):
	"""
	- Called once before other functions. Used to collect key values of
	all squares that can be modified.
	- Value is 'True' for 'assigned' and 'False' for 'not-assigned'.
	- To be used for function 'getNextEmptySquare()'.
	"""
	assigned = dict()

	#Add only square slots that were NOT set in inital board config
	for square in squares:

		if len(board.dict[square]) != 1:

			assigned[square] = False

	return assigned



def assignmentComplete(board):
	"""Returns true if every square has a single value filled in"""
	boardAssignment = ""

	for square in board:

		squareDomain = board.dict[square]
		
		if len(squareDomain) != 1:
			return False
		boardAssignment += squareDomain[0]

	return boardAssignment












# """---------------------------------"""

# 	#Return solution board if assignment worked and is complete
# 	assignedBoard = assignmentComplete(board)
# 	if assignedBoard:
# 		#Assigned board is a string representation of the complete sudoku board
# 		return assignedBoard


# 	aSquare = getNextEmptySquare() 

# 	domainOfSquare = board.dict[square]
	
# 	for value in domainOfSquare:
# 		#Assign this value to the square and see if contraints are violated

# 		#If any constraints with peers are violated, try next value
# 		for peer in peers[aSquare]:
# 			passThisPeer = False

# 			peerDomain = board.dict[peer]

# 			#needs to be at least one x != value to pass this peer constraint
# 			for x in peerDomain:

# 				if value != x:
# 					passThisPeer = True
# 					break

# 			if passThisPeer == False:
# 				#Have to assign a new value to square and restart
# 				break
# 			else: #This peer satisfied binary constraint with the square









"""Running 2"""





















"""Runnning"""

argList = sys.argv

#inputBoard = argList[1]
#print(len(inputBoard))



#board = Board(inputBoard)
#board.setDictionary()

#ac3(board)

#print(board.dict)


#print(board.dict)
#print(board.dict["I9"])




"""Test on total in file"""


with open("assignment4/sudokus_start.txt") as f:
	for line in f:
		#print(line)
		boardString = line[0:81]
		#print(boardString,"\n")
		#print(boardString)
		#print(len(boardString))
		#print(len(line))

		board = Board(boardString)
		board.setDictionary()

		#print(board.dict)
		ans = ac3(board)





























