#import os
#os.chdir(r'C:\Users\45302\Desktop\Python')
from sokoban_robot_planning import run 
import timeit

moves = run()       
print(moves)