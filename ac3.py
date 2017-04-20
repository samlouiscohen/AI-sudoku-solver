from Queue import *
import copy
from helper import *


def ac3(board, theSquares, thePeers):
	""" 
	The Arc Consistency Algorithm(AC-3). This algorithm iterates through
	potential values for each square and reduces neighboring domains to
	avoid conflict between 'arcs'-relations
	"""

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

	while queueOfArcs.qsize() != 0:
		arc = queueOfArcs.get()
		#print(arc)
		square = arc[0]
		peer = arc[1]

		if revise(square, peer, board):

			domainI = board.dict[arc[0]]

			#Deleted too much without finding a solution (Can't be solved)
			if len(domainI) == 0:
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