"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now). 
See Courseworks for detailed instructions.

@author: Max Ogryzko (mvo2102)
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)
    

def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions. 
    The result should be a list containing (Action, state) tuples. 
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))), 
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))] 
    """
    child_states = []

    for i in range (0, 3):
        for j in range (0, 3):
            if(state[i][j] == 0):
                break
        if(state[i][j] == 0):
            break

    if (j == 0):
        child_states.append(["Left", swap_cells(state, i, j, i, j + 1)])
    elif (j == 1):
        child_states.append(["Left",swap_cells(state, i, j, i, j + 1)])
        child_states.append(["Right", swap_cells(state, i, j, i, j - 1)])
    else:
        child_states.append(["Right", swap_cells(state, i, j, i, j - 1)])

    if (i == 0):
        child_states.append(["Up", swap_cells(state, i, j, i + 1, j)])
    elif (i == 1):
        child_states.append(["Up", swap_cells(state, i, j, i + 1, j)])
        child_states.append(["Down", swap_cells(state, i, j, i - 1, j)])
    else:
        child_states.append(["Down", swap_cells(state, i, j, i - 1, j)])


    return child_states

            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """

    if state == ((0, 1, 2),(3, 4, 5),(6, 7, 8)):
        return True
    else:
        return False


   
def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    frontier = [state]
    parents = {}
    parents[state] = state
    actions = {}

    states_expanded = 0
    max_frontier = 1
    explored = set()
    seen = set()
    seen.add(state)

    #while frontier is not empty (frontier will be equivalent to boolean false if empty):
    while frontier:
        n = frontier[0]
        frontier.pop(0)
        max_frontier -= 1
        explored.add(n)
        states_expanded += 1

        if goal_test(n):
            return return_path(n, parents, actions), states_expanded, max_frontier


        successors = get_successors(n)
        for x in range(0, len(successors)):
            currentsuccessor = successors[x][1]
            if not((currentsuccessor in explored) or (currentsuccessor in seen)):
                frontier.append(successors[x][1])
                seen.add(successors[x][1])
                parents[successors[x][1]] = n #updates parent dictionary with key = child and value = parent
                actions[successors[x][1]] = successors[x][0] #updates action dictionary with key = child and value = action attatched to child (action that parent took to get to child)
                max_frontier += 1
    return None, states_expanded, max_frontier  # No solution found





def return_path(n, parents, actions):

    path = []
    current = n

    while parents[current] != current: # I set the first state as it's own key and value in parents dictionary
        path.insert(0, actions[current])
        current = parents[current]


    return path

                               
     
def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    frontier = [state]
    parents = {}
    parents[state] = state
    actions = {}

    states_expanded = 0
    max_frontier = 1
    explored = set()
    seen = set()
    seen.add(state)

    # while frontier is not empty (frontier will be equivalent to boolean false if empty):
    while frontier:
        n = frontier[0]
        frontier.pop(0)
        max_frontier -= 1
        explored.add(n)
        states_expanded += 1

        if goal_test(n):
            return return_path(n, parents, actions), states_expanded, max_frontier


        successors = get_successors(n)
        for x in range(0, len(successors)):
            currentsuccessor = successors[x][1]
            if not((currentsuccessor in explored) or (currentsuccessor in seen)):
                frontier.insert(0,successors[x][1])
                seen.add(successors[x][1])
                parents[successors[x][1]] = n # updates parent dictionary with key = child and value = parent
                actions[successors[x][1]] = successors[x][0] # updates action dictionary with key = child and value = action attatched to child (action that parent took to get to child)
                max_frontier += 1
    return None, states_expanded, max_frontier


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """
    counter = 0
    misplaced_tiles = 0
    for i in range (0, 3):
        for j in range (0, 3):
            if(state[i][j] == 0):
                misplaced_tiles += 0
            elif not(state[i][j] == counter):
                misplaced_tiles += 1
            counter += 1

    return misplaced_tiles


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the manhattan distance between the current
    position and the goal position. Then sum all distances.
    """
    heuristic_counter = 0
    counter = 0
    for i in range (0, 3):
        for j in range (0, 3):
            if not(state[i][j] == counter):
                if ((state[i][j] - counter == 1) and ((counter + 1) % 3 == 0)) or ((state[i][j] - counter == -1) and
                    (counter == 3 or counter == 6)) or (abs(state[i][j] - counter) == 7) or abs(state[i][j] - counter) == 5:
                    heuristic_counter += 3
                elif abs(state[i][j] - counter) == 1 or abs(state[i][j] - counter) == 3:
                    heuristic_counter += 1
                elif (state[i][j] - counter == 4 and counter == 2) or (state[i][j] - counter == -4 and counter == 6) \
                        or (abs(state[i][j] - counter) == 8):
                    heuristic_counter += 4
                elif abs(state[i][j] - counter) == 2 or abs(state[i][j] - counter) == 4 or abs(state[i][j] - counter) == 6:
                    heuristic_counter += 2
                else:
                    print("error")
            counter += 1


    return heuristic_counter # replace this


def best_first(state, heuristic = misplaced_heuristic):
    """
    Breadth first search using the heuristic function passed as a parameter.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """

    # You might want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    frontier = [(heuristic(state), state)]
    parents = {}
    parents[state] = state
    actions = {}

    states_expanded = 0
    max_frontier = 1
    explored = set()
    seen = set()
    seen.add(state)

    #while frontier is not empty (frontier will be equivalent to boolean false if empty):
    while frontier:
        n = frontier[0]
        heappop(frontier) #takes least cost value from list
        max_frontier -= 1
        explored.add(n[1])

        states_expanded += 1

        if goal_test(n[1]):
            return return_path(n[1], parents, actions), states_expanded, max_frontier


        successors = get_successors(n[1])
        for x in range(0, len(successors)):
            currentsuccessor = (heuristic(successors[x][1]), successors[x][1])
            if not((currentsuccessor[1] in explored) or (currentsuccessor[1] in seen)):
                heappush(frontier, currentsuccessor) #should put this state into list based on heuristic cost element
                seen.add(currentsuccessor[1])
                parents[currentsuccessor[1]] = n[1] #updates parent dictionary with key = child and value = parent
                actions[currentsuccessor[1]] = successors[x][0] #updates action dictionary with key = child and value = action attatched to child (action that parent took to get to child)
                max_frontier += 1
    return None, states_expanded, max_frontier



def astar(state, heuristic = misplaced_heuristic):
    """
    A-star search using the heuristic function passed as a parameter. 
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    # You might want to use these functions to maintain a priority queue

    from heapq import heappush
    from heapq import heappop

    frontier = [(heuristic(state), state)]
    parents = {}
    parents[state] = state
    actions = {}
    cost = {}
    cost[state] = 0

    states_expanded = 0
    max_frontier = 1
    explored = set()
    seen = set()
    seen.add(state)

    # while frontier is not empty (frontier will be equivalent to boolean false if empty):
    while frontier:
        n = frontier[0]
        heappop(frontier)  # takes least cost value from list
        max_frontier -= 1
        explored.add(n[1])

        states_expanded += 1

        if goal_test(n[1]):
            return return_path(n[1], parents, actions), states_expanded, max_frontier

        successors = get_successors(n[1])
        for x in range(0, len(successors)):
            currentcost = cost[n[1]] + 1 + heuristic(successors[x][1])
            currentsuccessor = (currentcost, successors[x][1])
            if not ((currentsuccessor[1] in explored) or (currentsuccessor[1] in seen)):
                seen.add(currentsuccessor[1])
                parents[currentsuccessor[1]] = n[1]  # updates parent dictionary with key = child and value = parent
                actions[currentsuccessor[1]] = successors[x][0]  # updates action dictionary with key = child
                                    # and value = action attatched to child (action that parent took to get to child)
                cost[currentsuccessor[1]] = cost[n[1]] + 1
                heappush(frontier, currentsuccessor)  # should put this state into list based on heuristic cost element
                max_frontier += 1

    return None, states_expanded, max_frontier


    # The following line computes the heuristic for a state
    # by calling the heuristic function passed as a parameter. 
    # f = heuristic(state) 
 
    # Use the following two lines to retreive and return the 
    # solution path:  
    #  solution = get_solution(state, parents, actions, costs)
    #  return solution, states_expanded, max_frontier


def print_result(solution, states_expanded, max_frontier):
    """
    Helper function to format test output. 
    """
    if solution is None: 
        print("No solution found.")
    else: 
        print("Solution has {} actions.".format(len(solution)))
    print("Total states exppanded: {}.".format(states_expanded))
    print("Max frontier size: {}.".format(max_frontier))



if __name__ == "__main__":

    #Easy test case
    #test_state = ((1, 4, 2),
     #             (0, 5, 8),
      #            (3, 6, 7))

    #test_state = ((1, 0, 2),
     #             (3, 4, 5),
      #            (6, 7, 8))

    #More difficult test case
    test_state = ((7, 2, 4),
                 (5, 0, 6),
                  (8, 3, 1))


    print(state_to_string(test_state))
    print(" ")

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_frontier = bfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print(" ")
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_frontier = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))


    print(" ")
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))
    
    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))
