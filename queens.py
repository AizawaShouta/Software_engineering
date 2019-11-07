# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:36:49 2019

@author: Marie
"""

#!/usr/bin/python3

# A solver for the n-queens problem
#
# It uses a recursive search algorithm with backtracking,
# and displays naively the current partial solution.
#
# Some background information on Wikipedia:
#   https://en.wikipedia.org/wiki/Eight_queens_puzzle
#
# Question 1
# ----------
# Modify the code to add a more graphical display of the current
# partial solution, using pygame [1] or curses [2].
# The "old" display should remain available and the search
# algorithm should not be duplicated. More specifically,
# search(size,G) should start the search with a graphical progress
# display, and start(size,O) should do the same with the old
# display, for some G and O. The two modes should be available to
# the user via the command-line.
#
# [1] https://docs.python.org/3/howto/curses.html
# [2] https://www.pygame.org/
"""as for this question, I used pygame and made the program show each partial
solution for half a second as it is progressing, then the final solution (if
there is one) for five seconds, before exit(0) is called"""

# Question 2
# ----------
# Modify the procedure so that it also allows to obtain
# the number of solutions instead of printing and exiting
# after having found the first solution.
# It should still be possible to obtain the old behaviour
# (which avoids exploring the whole solution space).
# The two modes should be available to the user via the
# command-line.
# Bonus points if other interesting uses are enabled by the
# modified procedure.

"""for this I modified the search code so it would look for all possible
solutions, and added a graphical function to display the growing number of
solutions. I left the waiting times so one can see what the program
is doing, so when searching for all possible answers for important size, it
takes some time"""

import pygame as pyg
import time

size_sq = 20
white, black, red, green = (255,255,255), (0,0,0), (255,0,0), (0,255,0)

def display_board(window, size, queens):
    #create the board
    for i in range(size):
        cnt = i % 2
        for z in range(size):
            if cnt % 2 == 0:
                pyg.draw.rect(window, white,[size_sq*z,size_sq*i,size_sq,size_sq])
            else:
                pyg.draw.rect(window, black, [size_sq*z,size_sq*i,size_sq,size_sq])
            cnt +=1
    #then add the queens
    for i in range(len(queens)):
        pyg.draw.circle(window, red, (i*size_sq+size_sq // 2, queens[i]*size_sq+size_sq // 2), size_sq // 2)
    #update the window
    pyg.display.flip()

def solution_text(nb_sol,size_w,window):
    font = pyg.font.Font('freesansbold.ttf', 16)
    text_sol=str(nb_sol)+" solutions"
    text = font.render(text_sol, True, green, white)  
    textRect = text.get_rect()  
    textRect.center = (size_w // 2, size_w // 2)
    window.blit(text, textRect)
    pyg.display.update()

def queens(size,opt,mode):
    if opt=='G':
        pyg.init()
        size_w=size_sq*size
        window=pyg.display.set_mode((size_w,size_w))
        running=True
        while running:
            display_board(window, size, [])
            search(size,opt,mode,window)
            event = pyg.event.wait ()
            if event.type == pyg.QUIT:
                running = False
                pyg.quit ()
    else:
        search(size,opt,mode)

def search(size,opt,mode,window=None):
    # The algorithm attempts to set one queen per line,
    # starting with line 0 and processing lines in order,
    # backtracking when it stuck.
    #
    # In order to test rapidly for possible positions, it
    # maintains tables of free columns and diagonals:
    #  - col[j] indicates that column j is free
    #  - up[k] indicates that the upward-going diagonal k is free
    #  - down[k] indicates that the downward-going diagonal k is free
    # Here j belongs to range(size) and k belong to range(2*size-1).
    col = [-1 for _ in range(size)]
    up = [-1 for _ in range(2*size-1)]
    down = [-1 for _ in range(2*size-1)]
    # The current solution is maintained for display as a list of
    # successive column indices.
    sol = []
    nb_sol=[0]
    def searchline(i):
        if i==size:
            nb_sol[0]+=1
            if mode=="one":
                if opt=='G':
                    time.sleep(5)
                else:
                    print("Solution found.")
                exit(0)
            if mode=="all":
                if opt=='G':
                    solution_text(nb_sol[0],size_sq*size,window)
                    time.sleep(1)
                else:
                    print(nb_sol[0]," solution(s) found")
                return 0
        for j in range(size):
            if col[j] and down[i+j] and up[i-j+size-1]:
                col[j] = down[i+j] = up [i-j+size-1] = False
                sol.append(j)
                if opt=='O':
                    print(sol)
                if opt=='G':
                    display_board(window, size, sol)
                    time.sleep(0.4)
                searchline(i+1)
                sol.pop()
                col[j] = down[i+j] = up [i-j+size-1] = True
    searchline(0)
    if mode=="one":
        print("No solution!")
        time.sleep(1)
        exit(0)
    if mode=="all":
        if opt=='O':
            print(nb_sol[0], "solutions for size = ",size)
        else:
            solution_text(nb_sol[0],size_sq*size,window)
            time.sleep(5)
        exit(0)

import sys

if __name__ == "__main__":
    size = 7
    opt = 'O'
    mode="one"
    if len(sys.argv)>1:
        try:
            size = int(sys.argv[1])
        except (IndexError,ValueError):
            print("Usage: %s <int>" % sys.argv[0])
            exit(1)
    if len(sys.argv)>2:
        try:
            opt = sys.argv[2]
        except (IndexError,ValueError):
            print("Usage: %s <char>" % sys.argv[0])
            exit(1)
    if len(sys.argv)>3:
        try:
            mode = sys.argv[3]
        except (IndexError,ValueError):
            print("Usage: %s <str>" % sys.argv[0])
            exit(1)
    print("Searching for size %d..." % size)
    queens(size,opt,mode)
