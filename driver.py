import sys
from Queue import *
import copy

#from lazyme.string import color_print

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

#SEARCH FOR '?'


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


def ac3(board, theSquares, thePeers):
	""" """

	#These copies are to avoid references and overwriting of squares and peers
	squares = copy.deepcopy(theSquares)
	peers = copy.deepcopy(thePeers)

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
	#print(outBoard)

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








def backTrackingSearch(board, theSquares, thePeers):
	"""Returns a solution or failure """

	squares = copy.deepcopy(theSquares)
	peers = copy.deepcopy(thePeers)
	assignedSquareList, squareAnswers = setModifiableSquareList(board, theSquares)

	#Collect originals set squares
	origSquares = []
	for i in squareAnswers:
		if squareAnswers[i] != False:
			origSquares.append(i)

	return backTrack(board, squares, peers, assignedSquareList, squareAnswers, origSquares)


def backTrack(board, squares, peers, currentlyAssigned1, squareAnswers1,origSquares):
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


	currentlyAssigned = copy.deepcopy(currentlyAssigned1)
	squareAnswers = copy.deepcopy(squareAnswers1)
	


	#printCurrentState(board, squares, squareAnswers, origSquares)

	#print("currAssign: ", currentlyAssigned)
	#print("\n")
	#Base Case: Return solution board if assignment worked and is complete
	assignedBoard = assignmentComplete(board, squares, squareAnswers)
	#print(squareAnswers)

	#print(assignedBoard)
	if assignedBoard:
		#print(len(assignedBoard))
		return assignedBoard #a string representation of complete sudoku board

	#Should this be in some particular order???
	aSquare = getNextEmptySquare(squares, currentlyAssigned) 
	domainOfSquare = board.dict[aSquare]

	for value in domainOfSquare:
		#Assign this value to the square-- otherwise a square is set to False
		#Will show as true when assigned(any int other than 0 is true & range is 1-9)
		currentlyAssigned[aSquare] = value
		squareAnswers[aSquare] = value

		#If conflict with this square value, try a new one
		if assignmentConflict(board, aSquare, peers, value, squareAnswers):
			#print("assignment conflict on:" + str(value) + ", for square: " + aSquare)
			continue
			

		else: #No conflicts with this assigned square value
			#print("Pass with: " + str(value) + ", for square: " + aSquare) 
			#Recursively call again to determine if this past assignement was
			# the last needed to complete the board and start process of recursing back.
			boardSolved = backTrack(board, squares, peers, currentlyAssigned, squareAnswers,origSquares)
			
			#if boardSolved != True:#==bool()
				#print("hi:",boardSolved)
			if boardSolved != False:#==bool()
				#print("HYHYHYHYH00000000000000000000000000000")
				return boardSolved

			#If we get here, then we thought some assigned value for square was
			# good as there were no conflicts. However, this deep in the 
			# recursive calls, we see that it eventually leads to a problem. 
			#So clear this value from square and try another.
			else:
				#print(" ------------------------------GO BACK IN RECURSE!!!!!!!!!!!!!!!!!!!----------------------------------")
				continue

	#If we try all values in domain of the square, and build off them and they
	# all fail, then return failure.
	#print("pls")
	return False







def assignmentConflict(board, square, peers, squareVal, squareAnswers):
	"""Rewrite fucntion to not check against domains, but rather actual values"""

	#Boolean to track if square has a conflict with a given peer
	conflict = False

	for peer in peers[square]:

		if squareAnswers[peer] !=False:

			#Fail if a set peer is the same value as the current used squareVal
			if squareVal == squareAnswers[peer]:
				return True

	return False



def assignmentConflict1(board, square, peers, squareVal):
	"""Function to determine if the given value in the square conflicts with
	 any of the squares peers.
	 If this assignment leads to no conflicts, return False. Else, return True.
	 """
	#Boolean to track if square has a conflict with a given peer
	conflict = False

	if square == 'I8':
		print("square: " + square +"with sqrVal: "+squareVal+ ", peers: "+str(peers[square]))
		print("-----------------------------------------------------")
		#return


	"""THIS SHOULDNT CHECK DOMAIN BUT RATHER JUST STRAIGHT UP hardCoded VALUES"""

	for peer in peers[square]:
		conflict = True
		peerDomain = board.dict[peer]

		if peer == 'I9':
			print("Peer: "+peer+"With domain: "+str(peerDomain))

		for peerVal in peerDomain:

			#If at least 1 peer domain value is different than the square val,
			# then there is no conflict with this specific peer
			# if square == 'I8':
			# 	print("squareVal: " + str(squareVal) +", peerDomVal: "+str(peerVal))
			if squareVal != peerVal:
				if square == 'I8':

					print("NOT EQUAL SO NO CONFLICT-- squareVal: " + str(squareVal) + ". With peer: "+str(peer)+", peerDomVal: "+str(peerVal))
				conflict = False
				break
		
		# if square == 'I8':
		# 	exit()
		#If there is a conflict with a single peer, return failure
		if conflict:
			print("assignment conflict on:" + str(squareVal) + ", for square: " + square + ", with: "+peer) 
			return True

	#If we iterated thru all peers and no conflicts, return success
	return False


#REMOVE SQAURES FROM PARAM LIST HERE, DNT need anymore
def getNextEmptySquare(squares, assigned):
	"""Return the first non-assigned square it iterates over."""
	#print("Called get next empty square()")
	#print(assigned)

	#Only want to iterate over things that werent initally set. 
	#So shouldn't look through "squares" dictionary in general here.
	for square in assigned:
		if not assigned[square]:
			return square

		#print("thing:",assigned[square])


	# for square in squares:
	# 	#print(squares)

	# 	print("square: ",square)
	# 	print()
	# 	if not assigned[square]:
	# 		return square



def setModifiableSquareList(board, squares):
	"""
	- Called once before other functions. Used to collect key values of
	all squares that can be modified.
	- Value is 'True' for 'assigned' and 'False' for 'not-assigned'.
	- To be used for function 'getNextEmptySquare()'.
	"""
	#Assigned is a dictionary that only includes squares that can be modified (not originals)
	assigned = dict()
	#answerSquares includes everything
	answerSquares = dict()

	#Add only square slots that were NOT set in inital board config
	for square in squares:

		if len(board.dict[square]) != 1:

			assigned[square] = False
			answerSquares[square] = False
		else:
			#print('\n---hhhhhghghghghghghghghhgghhg--------')
			#print board.dict[square]
			#print board.dict[square][0]
			#print type(board.dict[square][0])
			#This will always be a one element list, so safe to cast out to str
			answerSquares[square] = board.dict[square][0]

	#print("---------HELLOOOO-----------------------------")
	#print(answerSquares)
	#print(len(answerSquares))
	#print("---------HELLOOOO-----------------------------")
	return assigned, answerSquares



def assignmentComplete(board, squares, assigned):
	"""Returns true if every square has a single value filled in"""
	boardAssignment = ""
	#print assigned

	for square in squares:
		#print(square)
		#print("HELLLL___________EEEEE____________OOOO____",assigned[square])
		if assigned[square] == False:
			return False 
		else:
			boardAssignment += assigned[square]

	return boardAssignment


	#Not modifying the domain in this algorithm, so below doesnt make sense

	# for square in squares:

	# 	squareDomain = board.dict[square]
		
	# 	if len(squareDomain) != 1:
	# 		print(str(squareDomain)+" is len: " +str(len(squareDomain)))
	# 		return False
	# 	boardAssignment += squareDomain[0]

	# return boardAssignment












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




def buildSquaresAndPeers():
	"""Method to construct dictionaries for the squares and 
	their respective peers on the sudoku board"""

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


	return squares, peers

def printCurrentState(board, squares, assigned,origSquares):
	"""Function to assist in debugging of the recursive calls by assembling and
	printing the board configuration"""
	
	keyString = ""
	boardstring = ""

	for square in squares:
		keyString+=square

		if assigned[square] == False:
			#color empties red
			boardstring += '\x1b[0;30;41m'+"x"+ '\x1b[0m' + " "
		else:
			#print origSquares
			if square in origSquares:
				#print("7-1-1-1-1-1-1-1-1-1-1-==-==--=-=-=-=-=-=-=-=-=")
				
				boardstring += assigned[square] +  " "
			else:
				#color new green
				boardstring += '\x1b[6;30;42m'+ assigned[square] + '\x1b[0m' +" "

	print keyString
	print boardstring






"""----------Main method: Run both methods, AC3 and Back-Tracking----------"""
argList = sys.argv
board1 = Board(argList[1])
board1.setDictionary()

#Construct boards squares and peers for use in both methods
squares, peers = buildSquaresAndPeers()

#Call backTracking algorithm
# ans1 = backTrackingSearch(board1, squares, peers)
# print(ans1)

with open("assignment4/sudokus_start.txt") as f:
	for line in f:
		boardString = line[0:81] #Necessary>???????????
		board = Board(boardString)
		board.setDictionary()

		ans1 = backTrackingSearch(board, squares, peers)
		print(ans1)




# with open("assignment4/sudokus_start.txt") as f:
# 	for line in f:

# 		boardString = line[0:81] #Necessary>???????????

# 		board = Board(boardString)
# 		board.setDictionary()

# 		#print(board.dict)
# 		ans = ac3(board, squares, peers)














# """Runnning"""

# argList = sys.argv

# #inputBoard = argList[1]
# #print(len(inputBoard))



#board = Board(inputBoard)
#board.setDictionary()

#ac3(board)

#print(board.dict)


#print(board.dict)
#print(board.dict["I9"])




# """Test on total in file"""


# with open("assignment4/sudokus_start.txt") as f:
# 	for line in f:
# 		#print(line)
# 		boardString = line[0:81]
# 		#print(boardString,"\n")
# 		#print(boardString)
# 		#print(len(boardString))
# 		#print(len(line))

# 		board = Board(boardString)
# 		board.setDictionary()

# 		#print(board.dict)
# 		ans = ac3(board)





























