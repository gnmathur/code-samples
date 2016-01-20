#!/usr/bin/env python

# The MIT License (MIT)
# 
# Copyright (c) [2016] [Gaurav Mathur]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import math

"""
Boogle solver class
"""
class BoggleSolver:
    def __init__(self, dict_file, board_letters):
        # The problem board
        self.grid = []
        # A set to mark visited cells
        self.visited = set()
        # This set will hold all dictionary words
        self.complete_dict = set()
        # This set will hold all prefixes of words in the dictionary
        self.prefix_dict = set()
        # This set will hold the result
        self.result = set()
        # Derive the board dimension
        self.dimension = int(math.sqrt(len(board_letters)))

        # The program supports only square grids
        if self.dimension*self.dimension != len(board_letters):
            raise Exception("Board needs to be NxN!")

        # Create the boggle grid
        for letter in board_letters:
           self.grid.append(letter)
       
         
        # Read in the dictionary. We will create two sets, one for holding 
        # all the dictionary words and the other for all the prefixes. 
        # Obviously the prefixes set will be (large) mutiple of the words in 
        # the dictionary. 
        for line in open(dict_file, "r"):
            l = line.rstrip()
            self.complete_dict.add(l)
            self.prefix_dict.add(l)
            while True:
                l = l[:-1]
                if len(l) == 0: 
                   break
                self.prefix_dict.add(l)

    # Solve the problem!
    def solve(self):
        for X in range(0, self.dimension):
            for Y in range(0, self.dimension):
                word = ""
                self.visit_cell(X, Y, word)
        return list(self.result)

    """
    Core logic - a DFS-like traversal on a undirected graph with cycles
    """
    def visit_cell(self, X, Y, word):
        # Check if these X and Y coordinates are valid, we might be 
        # going off the grid
        if X < 0 or Y < 0 or X >= self.dimension or Y >= self.dimension:
            return
       
        # Break the traversal cycle 
        if (X, Y) in self.visited:
            return
        
        # We are at a cell, add this letter to the word being built in this 
        # traversal
        word += self.grid[X+Y*self.dimension]
        if word not in self.prefix_dict:
            return

        if len(word) >= 2 and word in self.complete_dict:
            self.result.add(''.join(word))

        # Mark a cell as visited
        self.visited.add((X, Y))

        # Now visit all adjacent cells
        self.visit_cell(X-1, Y-1, word)
        self.visit_cell(X-1, Y, word)
        self.visit_cell(X-1, Y+1, word)
        self.visit_cell(X, Y-1, word)
        self.visit_cell(X, Y+1, word)
        self.visit_cell(X+1, Y-1, word)
        self.visit_cell(X+1, Y, word)
        self.visit_cell(X+1, Y+1, word)

        # Unmark a cell as visited
        self.visited.remove((X, Y))
"""
Usage:  python boggle.py <dictionary file> <list of characters>

        Dictionary file is a text file with a list of dictionary words, one word
        per line, and 

        Where a N*N list of characters represents a NxN board

Example:

>> python boggle.py dict.txt f e t a p o l k m
['feal', 'alk', 'tea', 'pot', 'tef', 'palk', 'pom', 'apo', 'et', 'alp', 'ape', 'la', 'pet', 'top', 'to', 'pa', 'tom', 'poet', 'tepal', 'pal', 'pea', 'toe', 'opt', 'mote', 'mop', 'mot', 'falk', 'toea', 'peal', 'apt', 'mope', 'tope', 'lap', 'oka', 'om', 'ope', 'opal', 'km', 'teak', 'tepa', 'teal', 'op', 'peak']
"""
if __name__ == "__main__":
    solver = BoggleSolver(sys.argv[1], sys.argv[2:])
    print solver.solve()

