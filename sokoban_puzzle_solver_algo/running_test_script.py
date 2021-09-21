from sokoban_robot_planning import *

moves = run()
print('BFS: '+str(breadthFirstSearch()))
print('Robot: '+str(states_converted_to_robot()))