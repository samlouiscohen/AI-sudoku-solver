# AI-sudoku-solver

This is an AI to solve sudoku boards. I implemented two main algorithms-- The Arc Consistency Algorithm #3 (AC-3) and The Back-Tracking Search Algorithm(BTS) with two heuristic functions: Minimum Remaining Values(MRV) and Forward Checking(FC). 

I tested both algorithms on a sample file with 400 sudoku boards. I found that with just AC-3, the program could solve a meager 3 out of  400 and took an average time of 6 seconds to complete them.

On the other hand, BTS, augmented by both MRV and FC, was able to solve all valid sudoku boards in the sample file and was even able to solve one of the world's "hardest" board configurations in just a few seconds. It took an average of 0.02 seconds to solve each one in the sample file.

Further algorithm details and implementation is outlined in the source code.
