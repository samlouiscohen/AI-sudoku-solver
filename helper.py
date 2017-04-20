def cross(A, B):
	"Cross product of elements in A and elements in B."
	return [a+b for a in A for b in B]


def printCurrentState(board, squares, assigned, origSquares):
	"""
	Function to assist in debugging of the recursive calls by assembling and
	printing the board configurations.
	"""
	
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
				
				boardstring += assigned[square] +  " "
			else:
				#color new green
				boardstring += '\x1b[6;30;42m'+ assigned[square] + '\x1b[0m' +" "

	print keyString
	print boardstring