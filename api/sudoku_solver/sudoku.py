from api.sudoku_solver.utils import *
#from search import *
import sys
from collections import deque
from copy import deepcopy
import time

class SudoKu:
    size=9
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.nodes_generated=0
        self.nodes_expanded=0
        

    def actions(self, state):
        list1=[]
        row,col=self.find_next_empty(state)
        actions_row=self.row_options(state,row)
        actions_col=self.col_options(state,col)
        actions_block=self.block_options(state,row,col)
        intersection1=[x for x in actions_row if x in actions_col]
        intersection2=[x for x in actions_block if x in intersection1]
        return intersection2

    def result(self, state, action):
        number_list=[1,2,3,4,5,6,7,8,9]
        row,col=self.find_next_empty(state)
        updated_state=deepcopy(state)
        if(action in number_list):
            updated_state[row][col]=action
            return updated_state
        
    def find_next_empty(self,state):
        for i in range(0,self.size):
            for j in range(0,self.size):
                if(state[i][j]==0):
                    return i,j
        return -1,-1

    def goal_test(self, state):
        if(state==self.initial):
            return False
        if(state is None):
            return False
        for i in range(0,self.size):
            if(self.row_check(state,i) is False):
                return False
            if(~self.col_check(state,i) is False):
                return False
            if(~self.block_check(state,i) is False):
                return False
        row,col=self.find_next_empty(state)
        if(row==-1):
            return True
        else:
            return False

    def row_check(self,state,row):
        check=[]
        for i in range(0,self.size):
            if(state[row][i] in check):
                return False
            if(state[row][i]!=0):
                check.append(state[row][i])
        return True

    def col_check(self,state,col):
        check=[]
        for i in range(0,self.size):
            if(state[i][col] in check):
                return False
            if(state[i][col]!=0):
                check.append(state[i][col])
        return True

    def block_check(self,state,id):
        check=[]
        tmp_row=3*(id%3)
        tmp_col=3*(int)(id/3)
        for r1 in range(0,3):
            for c1 in range(0,3):
                curr=state[r1+tmp_row][c1+tmp_col]
                if curr in check:
                    return False
                if curr!=0:
                    check.append(curr)
        return True

    def row_options(self,state,row):
        check=[1,2,3,4,5,6,7,8,9]
        for i in range(0,self.size):
            if state[row][i]==0:
                continue
            if state[row][i] in check:
                check.remove(state[row][i])
        return check

    def col_options(self,state,col):
        check=[1,2,3,4,5,6,7,8,9]
        for i in range(0,self.size):
            if state[i][col]==0:
                continue
            if state[i][col] in check:
                check.remove(state[i][col])
        return check

    def block_options(self,state,row,col):
        check=[1,2,3,4,5,6,7,8,9]
        tmp_row=row-row%3
        tmp_col=col-col%3
        for r1 in range(0,3):
            for c1 in range(0,3):
                curr=state[r1+tmp_row][c1+tmp_col]
                if curr==0:
                    continue
                if curr in check:
                    check.remove(curr)
        return check
    
    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        pass
    def inc_nodes_gen(self,val):
        self.nodes_generated=self.nodes_generated+val
    def inc_nodes_exp(self,val):
        self.nodes_expanded=self.nodes_expanded+val

# ______________________________________________________________________________

class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        problem.inc_nodes_exp(1)
        problem.inc_nodes_gen(len(problem.actions(self.state)))
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


# ______________________________________________________________________________


def breadth_first_tree_search(problem):
    frontier = deque([Node(problem.initial)])  # FIFO queue
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None


def depth_first_tree_search(problem):

    frontier = [Node(problem.initial)]  # Stack

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def depth_limited_search(problem, limit=50):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result

# # ______________________________________________________________________________
# test_puzzle=[
# [0, 3, 7, 0, 0, 5, 0, 0, 6],
# [0, 3, 8, 1, 0, 0, 7, 0, 9],
# [0, 6, 0, 0, 0, 0, 1, 5, 3],
# [0, 5, 0, 0, 2, 7, 8, 6, 4],
# [6, 2, 4, 8, 0, 0, 5, 0, 7],
# [0, 8, 0, 6, 0, 4, 9, 0, 2],
# [0, 9, 6, 5, 7, 1, 2, 0, 8],
# [0, 0, 1, 4, 0, 2, 3, 0, 5],
# [0, 0, 0, 0, 8, 3, 0, 0, 1]
# ]
# print("Initial Unsolved state: ")
# print(test_puzzle)
# print("-----------------------------------------------------")
# print("BFS Analysis: ")
# sudoku_solve=SudoKu(test_puzzle)
# start_time=time.time()
# solved=breadth_first_tree_search(sudoku_solve)
# end_time=time.time()
# time_taken=end_time-start_time
# print("Solved State: ")
# print(solved.state)
# print("Time Taken: ",time_taken)
# print("Nodes Generated: ",sudoku_solve.nodes_generated)
# print("Nodes Expanded: ",sudoku_solve.nodes_expanded)
# trace_nodes=solved.path()
# print("Total steps: ",len(trace_nodes))
# print("-----------------------------------------------------")
# print("DFS Analysis: ")
# sudoku_solve=SudoKu(test_puzzle)
# start_time=time.time()
# solved=depth_first_tree_search(sudoku_solve)
# end_time=time.time()
# time_taken=end_time-start_time
# print("Solved State: ")
# print(solved.state)
# print("Time Taken: ",time_taken)
# print("Nodes Generated: ",sudoku_solve.nodes_generated)
# print("Nodes Expanded: ",sudoku_solve.nodes_expanded)
# trace_nodes=solved.path()
# print("Total steps: ",len(trace_nodes))
# print("-----------------------------------------------------")
# print("DLS Analysis: ")
# sudoku_solve=SudoKu(test_puzzle)
# start_time=time.time()
# solved=depth_limited_search(sudoku_solve)
# end_time=time.time()
# time_taken=end_time-start_time
# print("Solved State: ")
# print(solved.state)
# print("Time Taken: ",time_taken)
# print("Nodes Generated: ",sudoku_solve.nodes_generated)
# print("Nodes Expanded: ",sudoku_solve.nodes_expanded)
# trace_nodes=solved.path()
# print("Total steps: ",len(trace_nodes))
# print("-----------------------------------------------------")
# print("IDS Analysis: ")
# sudoku_solve=SudoKu(test_puzzle)
# start_time=time.time()
# solved=iterative_deepening_search(sudoku_solve)
# end_time=time.time()
# time_taken=end_time-start_time
# print("Solved State: ")
# print(solved.state)
# print("Time Taken: ",time_taken)
# print("Nodes Generated: ",sudoku_solve.nodes_generated)
# print("Nodes Expanded: ",sudoku_solve.nodes_expanded)
# trace_nodes=solved.path()
# print("Total steps: ",len(trace_nodes))
# print("-----------------------------------------------------")
