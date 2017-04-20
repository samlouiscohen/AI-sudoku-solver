from Queue import *
import copy
from helper import *



def backTrackingSearch(board, theSquares, thePeers):
	""" 
	Wrapper function to house backtracking algorithm.
	Returns a solution or failure 'False'.
	"""
	#Deep copies to avoid altering arguments if BTS is called multiple times
	squares = copy.deepcopy(theSquares)
	peers = copy.deepcopy(thePeers)

	#Grab list of keys of original squares and dict. to track currently set squares
	origSquares, setSquares = setSquareInfo(board, theSquares)

	#Remove original square values from their peer's domains (these values will never be allowed)
	removeOrigValsFromAllPeerDomains(board, squares, peers, origSquares)

	#Start recursive call
	return backTrack(board, squares, peers, origSquares, setSquares)



def backTrack(board, squares, peers, origSquaresIn, setSquaresIn):
	"""
	Recursive method that essentially performs a DFS search to incrementally
	 build the board by assigning single values that don't currently cause
	 conflict. If we run into undeniable conflict later in the tree, we
	 return 'False' and "back-track" in the tree to assign a different value 
	 than the one that was initially thought was acceptable.

	 This is to say that it visits each empty square and tries assigning values 
	 to if from its domain. Whenever a conflict is apparent it trys the next.
	 If it succeeds but later we see another square has exhausted all of its
	 domain options, we know the previous value was a mistake. 
	 We then backtrack.
	"""

	#Original Squares is list of keys, setSquares is a full map of set squares
	originalSquares = copy.deepcopy(origSquaresIn)
	setSquares = copy.deepcopy(setSquaresIn)

	#Function I made that helped tremendously in debugging
	#printCurrentState(board, squares, setSquares, originalSquares)

	#Base Case: Return the completed board if the last assignment led completion
	assignedBoard = assignmentComplete(board, squares, setSquares)
	if assignedBoard:
		return assignedBoard #a string representation of complete sudoku board


	#Decide the next square to assign based on the MRV heuristic
	aSquare = MRVNextEmptySquare(board, squares, originalSquares, setSquares) 
	
	domainOfSquare = board.dict[aSquare]


	#Start iterating through all potential values to assign to the square 
	for value in domainOfSquare:

		#Update the set-square dictionary
		setSquares[aSquare] = value

		#If conflict between this square value and already set ones, try a new value
		if assignmentConflict(board, aSquare, peers, value, setSquares):
			continue
			
		else: #No conflicts with this assigned square value-- Move on.

			#After this past assignment, update domains and see if the board is invalid.
			#Important: 'newBoard' wont overwrite 'board' domains, if this turns out to be a bad value.
			anyZeroDomains, newBoard = forwardCheck(board, aSquare, setSquares, peers)

			if anyZeroDomains:
				continue

			#Recusive call to determine if the past assignment completed 
			# the board. If not, we ran into a problem later in the recursion 
			# even though this assigned value seemed to cause no immediate 
			# conflict. So we continue to the next possible assignement.
			boardSolved = backTrack(newBoard, squares, peers, originalSquares, setSquares)
			if boardSolved != False:
				return boardSolved
			else:
				continue

	#If we iterate through all possible domain values and no assignment works, 
	# we clearly assigned an incorrect value before. Return False and go back a 
	# layer of recursion to try a new a past value.
	return False



def removeOrigValsFromAllPeerDomains(board, squares, peers, origSquares):
	"""Remove originally set square values from all of their peer's domains."""

	for origSquare in origSquares:

		for peer in peers[origSquare]:

			origSquareVal = board.dict[origSquare][0]
			peerDomain = board.dict[peer]
			
			if origSquareVal in peerDomain:
				peerDomain.remove(origSquareVal)



def assignmentConflict(board, square, peers, squareVal, setSquares):
	"""
	Function to determine if a potential square value will cause a conflict
	with it's already-assigned peers.
	Return True if conflict. Otherwise, False.
	"""
	conflict = False

	for peer in peers[square]:

		#If the given peer IS in fact already set, check there's no conflict
		if setSquares[peer] != False:

			#Fail if a set peer is the same value as the current used squareVal
			if squareVal == setSquares[peer]:
				return True

	#If no peer causes conflict, return False-- no conflicts
	return False


def MRVNextEmptySquare(board, squares, originalSquares, setSquares):
	"""
	Function to choose the next square on the board to assign a value to.
	Utalizes the "Minimum Remaining Values" (MRV) heuristic, in which it 
	 chooses the square with a domain containing the fewest legal values.
	Also only searches through those squares that are not yet assigned.

	Returns a square (key).
	"""
	#We know that the largest a domain value can be is 9. 10 guarantees a choice.
	smallestDomain = 10
	minRemainValueSquare = None
	
	for square in squares:
		if square not in originalSquares and setSquares[square]==False:
			
			squareDomainSize = len(board.dict[square])

			if squareDomainSize < smallestDomain:
				smallestDomain = squareDomainSize
				minRemainValueSquare = square

	return minRemainValueSquare


def forwardCheck(board, newlyAssignedSquare, setSquares, peers):
	"""
	Multi-purpose function, called after a new square is assigned a value. It:
	1. Removes this newly-set square value from all of the squares peer domains.
	2. Checks if any given square has no more values in its domain-- conflict.

	Overall, forwardCheck both updates the dictionary and ends early if it 
	 determines that a conflict will soon be present. If this function is called,
	 the new square value doesnt conflict with any already set values. Then, 
	 the only option for failure is if any unassigned square has a 0-domain.

	Returns tuple: boolean (if conflict due to zero-domain) and the updated board.

	Important Note: This makes a deep copy of its argument board. This is so
	 that in the case of a backtrack, the old board is intact--unmodified.
	"""

	updatedBoard = copy.deepcopy(board)
	anyZeroDomains = False

	#Stage 1:
	newAssignedVal = setSquares[newlyAssignedSquare]

	for peer in peers[newlyAssignedSquare]:

		if newAssignedVal in updatedBoard.dict[peer]:
			
			updatedBoard.dict[peer].remove(newAssignedVal)

			#Stage 2
			if len(board.dict[peer]) == 0:
				anyZeroDomains = True
				#print("Hit a zero domain for: " + peer+". Backtrack?")
				return anyZeroDomains, updatedBoard

	return anyZeroDomains, updatedBoard



def setSquareInfo(board, squares):
	"""
	Called once in the wrapper function of BTS. This function does two things:
	1. Creates a list of keys representing all the initially filled squares.
	2. Creates a dictionary that stores which squares are "set" with a value.
		Value is 'True'(some int) for 'assigned' and 'False' for 'not-assigned'.
		To be used in functions such as getNextEmptySquare().
	Returns a list and a dictionary
	"""

	#Key values (A1-I9) of original squares
	origSquares = []
	#Dictionary to hold all 'set' values
	setSquares = dict()


	for square in squares:

		#If it isn't initially len=1, it wasn't initially set
		if len(board.dict[square]) != 1:
			setSquares[square] = False
		else:
			#This will always be a one element list, so safe to cast to string
			setSquares[square] = board.dict[square][0]
			origSquares.append(square)

	return origSquares, setSquares


def assignmentComplete(board, squares, assigned):
	"""
	Function to determine if a board configuration is completely filled in.
	Returns a string representing the board if every square is assigned a single value.
	Otherwise, returns False.
	"""

	boardAssignment = ""

	for square in squares:

		if assigned[square] == False:
			return False 
		else:
			boardAssignment += assigned[square]

	return boardAssignment



def buildSquaresAndPeers():
	"""
	Method to construct dictionaries for the squares and their respective
	 peers on the sudoku board. To be used essentially all helper functions.
	"""
	#A suduko board is numbered 1-9 and A-I
	columns  = "123456789"
	rows     = "ABCDEFGHI"

	#List of all labeled "squares": 'A1', 'A2', ... ,'I9'
	squares  = cross(rows, columns)

	#List of "units", where a unit is a (column, row, box) that requires all 
	# unique assignments to be avoid conflict.
	unitlist = ([cross(rows, c) for c in columns] +
				[cross(r, columns) for r in rows] +
				[cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

	#Dictionary to hold all units that a particular square lives in
	units = dict((s, [u for u in unitlist if s in u]) for s in squares)
	
	#Dictionary maps squares to their respective peers
	peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)

	return squares, peers











