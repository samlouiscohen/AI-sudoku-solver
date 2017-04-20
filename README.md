# AI-sudoku-solver

This is an AI to solve sudoku boards. I implemented two main algorithms-- The Arc Consistency Algorithm #3 (AC-3) and The Back-Tracking Search Algorithm with two heuristic functions (Minimum Remaining Values and Forward Checking). 

I tested both algorithms on a sample file with 400 sudoku boards. I found that with just AC-3, the program could solve 3 out of the 400 and took an average time of 6 seconds to complete them. This algorithm alone generally failed.

On the other hand, BTS, augmented by both MRV and FC, was able to solve all valid sudoku boards it recieved. It took an average of 0.02 seconds to solve each one.

Further algorithm details and implementation is outlined in the source code.
