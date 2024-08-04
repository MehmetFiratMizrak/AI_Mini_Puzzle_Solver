import random
import copy
import time


# State Class represents a given state of the board
class State:
    # Goal State is stored in a variable for comparison
    goal = {1: 1, 2: 2, 3: 3, 4: 4,
            5: 2, 6: 3, 7: 4, 8: 3,
            9: 3, 10: 4, 11: 3, 12: 2,
            13: 4, 14: 3, 15: 2, 16: 0}

    # The default constructor creates a finished puzzle
    def __init__(self):
        self.items = {1: 1, 2: 2, 3: 3, 4: 4,       # Items are stored in a dictionary
                      5: 2, 6: 3, 7: 4, 8: 3,
                      9: 3, 10: 4, 11: 3, 12: 2,
                      13: 4, 14: 3, 15: 2, 16: 0}
        self.index = 16                             # Index is the index of the empty square (0)

    # Prints a grid that represents the physical state of the puzzle
    def main_frame(self):
        d = self.items
        print('+-----+-----+-----+-----+')
        print('|  %s  |  %s  |  %s  |  %s  |' % (d[1], d[2], d[3], d[4]))
        print('+-----+-----+-----+-----+')
        print('|  %s  |  %s  |  %s  |  %s  |' % (d[5], d[6], d[7], d[8]))
        print('+-----+-----+-----+-----+')
        print('|  %s  |  %s  |  %s  |  %s  |' % (d[9], d[10], d[11], d[12]))
        print('+-----+-----+-----+-----+')
        print('|  %s  |  %s  |  %s  |  %s  |' % (d[13], d[14], d[15], d[16]))
        print('+-----+-----+-----+-----+')

    # Makes '#number' of random moves to shuffle a given state
    def puzzle_gen(self, number):
        for _ in range(number):
            lst1 = self.valid_moves()
            self.move(lst1[random.randint(0, len(lst1) - 1)])

    # Returns a list of all possible new states that can be reached from the current state
    def create_new_states(self):
        to_return = []
        moves = self.valid_moves()
        for i in moves:
            temp = copy.deepcopy(self)
            temp.move(i)
            to_return.append(temp)
        return to_return

    # Changes the position of square with entered index and the empty square
    def move(self, to):
        fro = self.index
        temp = self.items[to]
        self.items[to] = self.items[fro]
        self.items[fro] = temp
        self.index = to

    # Returns a list of integers that represents all valid moves
    def valid_moves(self):
        pos = self.index
        if pos in [6, 7, 10, 11]:
            return pos - 4, pos - 1, pos + 1, pos + 4
        elif pos in [5, 9]:
            return pos - 4, pos + 4, pos + 1
        elif pos in [8, 12]:
            return pos - 4, pos + 4, pos - 1
        elif pos in [2, 3]:
            return pos - 1, pos + 1, pos + 4
        elif pos in [14, 15]:
            return pos - 1, pos + 1, pos - 4
        elif pos == 1:
            return pos + 1, pos + 4
        elif pos == 4:
            return pos - 1, pos + 4
        elif pos == 13:
            return pos + 1, pos - 4
        elif pos == 16:
            return pos - 1, pos - 4

    # Heuristic function for ranking new states
    def heuristic(self):
        sum = 0
        for i in range(1, len(self.items)+1):
            sum = sum + self.items[i] * self.goal[i]    # Dot product of the goal and the current state
        return 135 - sum    # Is 0 when goal is achieved

    # Returns True if goal is achieved, False o.w.
    def is_goal(self):
        return self.items == self.goal

    # Returns True if entered state and the current state are equivalent, False o.w.
    def is_equal(self, other):
        return self.items == other.items


S1 = State()            # Creating puzzle
S1.puzzle_gen(100)      # Making 100 random moves
queue = list()          # Empty queue created
extended_list = list()  # Extended list to prevent loops and unnecessary node extensions
queue.append([S1])      # Queue initialized with the starting path (contains only the starting state)
w = 8                   # Beam width is set, w = 6-8 achieves relatively consistent results

print('Starting State: ')   # Printing the starting state
S1.main_frame()

path = list()           # Path will be the list of states that achieves the goal
t0 = time.time()        # Start time of the search algorithm
tolerance = 20          # Parameter to control how long to wait (in seconds)  before auxiliary exiting the loop

while True:             # Start of the Beam search algorithm
    break_ctrl = False  # Add hoc variable to print the correct output (Not important for the algorithm)
    t1 = time.time()    # Stores the time at each iteration
    correct = True      # Variable to show if the search worked as intended
    next_queue = []     # Used to set the new queue after extending all nodes at the current depth

    # Loop below is used to extend all paths in the queue and putting the extended paths into the new queue
    while len(queue) != 0:          # Until the queue is empty
        temp = queue.pop(0)         # Temporarily stores the first path in the queue and removes it from the queue
        if temp[-1].is_goal():      # If the final state in the path is goal, stop all search and return path
            output = "Goal found"
            path = copy.deepcopy(temp)
            break_ctrl = True
            break
        new_states = temp[-1].create_new_states()   # If not, extend the node and store new states
        extended_list.append(temp[-1])  # Add extended node to the extended list

        # This loop checks if the new states are in the extended list,
        # if not, creates new paths by adding the new states to the old paths
        # and adds the new paths to the new queue
        for s in new_states:
            check = True
            for st in extended_list:
                if s.is_equal(st):
                    check = False
            if check:
                temp2 = copy.copy(temp)
                temp2.append(s)
                next_queue.append(temp2)  # Adding the paths to new queue, which contains paths that are 1 level deeper

    if break_ctrl:       # The goal is reached, search is terminated
        output = "Goal found"
        break

    # Sorts the added paths according the heuristic values of their final node
    next_queue.sort(key=lambda x: x[-1].heuristic())
    queue = next_queue[:w]  # Sets the empty queue to be the best w of the new paths

    if len(queue) == 0:  # If the queue is empty there exist no solution
        output = "Goal not found"
        break

    if t1-t0 > tolerance:   # If time limit is extended, terminates the search
        correct = False
        output = "Time extended spent tolerance: " + str(t1-t0)
        break


if correct:
    old_index = 16
    for s in path:
        print('Square at index ' + str(old_index) + ' moved to index ' + str(s.index) + ':')
        s.main_frame()
        print()
        old_index = s.index
else:
    print("Time extended spent tolerance: " + str(t1-t0))

print(output)
print('Nodes extended: ' + str(len(extended_list)))
print('Queue length left: ' + str(len(queue)))