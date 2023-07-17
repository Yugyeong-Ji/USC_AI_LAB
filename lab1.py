
# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
from itertools import permutations
from lab1_utils import TextbookStack, apply_sequence
import copy
import numpy as np

def breadth_first_search(stack):
    flip_sequence = [] # Initialize an empty list to store the flip sequence

    visited = set() # Initialize a set to keep track of visited states
    queue = deque([(stack, [])]) # Initialize a queue with the initial stack and an empty sequence


    while queue:
        current_stack, current_sequence = queue.popleft()  # Get the next stack and sequence from the queue

        if current_stack.check_ordered():
            # If the current stack is ordered, update the flip sequence and break the loop
            flip_sequence = current_sequence
            break

        current_stack_tuple = (tuple(current_stack.order), tuple(current_stack.orientations))
        if current_stack_tuple not in visited:
            # If the current stack state has not been visited before, add it to the visited set
            visited.add(current_stack_tuple)

            # Generate new stacks by flipping individual sections of the current stack
            for idx in range(len(current_stack.order)):
                new_stack = current_stack.copy()  # Create a copy of the current stack
                new_stack.flip_stack(idx + 1) # Flip a section of the new stack
                new_sequence = current_sequence + [idx + 1] # Update the flip sequence
                queue.append((new_stack, new_sequence)) # Add the new stack and sequence to the queue

    return flip_sequence


def depth_first_search(stack):
    flip_sequence = [] # Initialize an empty list to store the flip sequence

    visited = set() # Initialize a set to keep track of visited states
    stack = [(stack, [])] # Initialize a stack with the initial stack and an empty sequence

    while stack:
        current_stack, current_sequence = stack.pop() # Get the next stack and sequence from the stack

        if current_stack.check_ordered():
            # If the current stack is ordered, update the flip sequence and break the loop
            flip_sequence = current_sequence
            break

        current_stack_tuple = (tuple(current_stack.order), tuple(current_stack.orientations))
        if current_stack_tuple not in visited:
            # If the current stack state has not been visited before, add it to the visited set
            visited.add(current_stack_tuple)

            # Generate new stacks by flipping individual sections of the current stack
            for idx in range(len(current_stack.order)):
                new_stack = current_stack.copy()  # Create a copy of the current stack
                new_stack.flip_stack(idx + 1)  # Flip a section of the new stack
                new_sequence = current_sequence + [idx + 1]  # Update the flip sequence
                stack.append((new_stack, new_sequence))  # Add the new stack and sequence to the stack

    return flip_sequence

def calculate_average_flips_and_nodes(n):
    total_flips_dfs = 0  # Initialize a counter for total flips in depth-first search
    total_nodes_dfs = 0  # Initialize a counter for total nodes explored in depth-first search
    total_flips_bfs = 0  # Initialize a counter for total flips in breadth-first search
    total_nodes_bfs = 0  # Initialize a counter for total nodes explored in breadth-first search

    num_configs = 2 ** n * np.math.factorial(n)  # Calculate the total number of configurations
    configs = list(permutations(range(n))) # Generate all possible configurations of the stack

    for config in configs:
        initial_order = list(config)
        initial_orientations = [0] * n
        stack = TextbookStack(initial_order, initial_orientations) # Create a new stack with the given configuration

        # Depth First Search
        sequence_dfs = depth_first_search(stack) # Perform depth-first search on the stack
        new_stack_dfs = apply_sequence(stack, sequence_dfs) # Apply the flip sequence to the stack
        total_flips_dfs += len(sequence_dfs) # Update the total flips counter for depth-first search
        total_nodes_dfs += len(sequence_dfs) + 1 # Update the total nodes counter for depth-first search

        # Breadth First Search
        sequence_bfs = breadth_first_search(stack) # Perform breadth-first search on the stack
        new_stack_bfs = apply_sequence(stack, sequence_bfs) # Apply the flip sequence to the stack
        total_flips_bfs += len(sequence_bfs)  # Update the total flips counter for breadth-first search
        total_nodes_bfs += len(sequence_bfs) + 1  # Update the total nodes counter for breadth-first search

    avg_flips_dfs = total_flips_dfs / num_configs  # Calculate the average flips for depth-first search
    avg_nodes_dfs = total_nodes_dfs / num_configs  # Calculate the average nodes explored for depth-first search
    avg_flips_bfs = total_flips_bfs / num_configs  # Calculate the average flips for breadth-first search
    avg_nodes_bfs = total_nodes_bfs / num_configs  # Calculate the average nodes explored for breadth-first search

    return avg_flips_dfs, avg_nodes_dfs, avg_flips_bfs, avg_nodes_bfs