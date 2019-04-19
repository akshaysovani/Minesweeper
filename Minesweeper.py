# Minesweeper

#from __future__ import print_function
import random
import numpy as np
import math
from tkinter import *
from statistics import mean
import itertools
from collections import OrderedDict
import queue

class Cell:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.isFlaggedMine = False
        self.isMine = False
        self.indicator = 0
        self.explored = False

    def Cell_setindicator(self,indicator):
        self.indicator = indicator

    def Cell_getindicator(self):
        return self.indicator

    def Cell_flagmine(self):
        self.isFlaggedMine = True

    def Cell_SetMine(self):
        self.isMine = True

    def Cell_IsMine(self):
        return self.isMine

    def Cell_IsFlaggedMine(self):
        return self.isFlaggedMine

    def Cell_setexplored(self):
        self.explored = True

    def Cell_isexplored(self):
        return self.explored

    def Cell_getrowcol(self):
        return self.row,self.col

    def Cell_GetNeighbourCells(self, row, col, dim_x, dim_y, order):
        child_nodes = []
        cell_value = []
        if col > order - 1:
            child_nodes.append([row,col-order])
        if col < dim_y - order:
            child_nodes.append([row,col+order])
        if row > order - 1:
            child_nodes.append([row-order,col])
            if col > order - 1:
                child_nodes.append([row-order,col-order])
            if col < dim_y - order:
                child_nodes.append([row-order,col+order])
        if row < dim_x - order:
            child_nodes.append([row+order,col])
            if col > order - 1:
                child_nodes.append([row+order,col-order])
            if col < dim_y - order:
                child_nodes.append([row+order,col+order])
        
        for child in child_nodes:
            cell_value.append(child[0]*dim_y + child[1])
        return cell_value

class BoardDesign:
    def __init__(self, dim_x, dim_y, no_of_mines, uncertainty_type):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.mine_count = no_of_mines
        self.uncertainty_type = uncertainty_type
        self.solved = False
        self.success_rate = 0
        self.cell_array = [Cell(int(num/self.dim_y), (num % self.dim_y)) for num in range(0,self.dim_x*self.dim_y)]

    def BoardDesign_CreateBoard(self):
        #count = self.mine_count
        #while count > 0:
        #    val = random.randint(0,(self.dim_x*self.dim_y)-1)
        #    if not self.cell_array[val].Cell_IsMine() and val != 0:
        #        self.cell_array[val].Cell_SetMine()
        #        count -= 1

        self.cell_array[4].Cell_SetMine()
        self.cell_array[8].Cell_SetMine()
        self.cell_array[11].Cell_SetMine()
        self.cell_array[20].Cell_SetMine()
        self.cell_array[35].Cell_SetMine()
        self.cell_array[38].Cell_SetMine()
        self.cell_array[40].Cell_SetMine()
        self.cell_array[42].Cell_SetMine()
        self.cell_array[49].Cell_SetMine()
        self.cell_array[58].Cell_SetMine()

        #self.cell_array[12].Cell_SetMine()
        #self.cell_array[30].Cell_SetMine()
        #self.cell_array[35].Cell_SetMine()
        #self.cell_array[36].Cell_SetMine()
        #self.cell_array[37].Cell_SetMine()
        #self.cell_array[39].Cell_SetMine()
        #self.cell_array[45].Cell_SetMine()
        #self.cell_array[49].Cell_SetMine()
        #self.cell_array[72].Cell_SetMine()
        #self.cell_array[79].Cell_SetMine()

    def BoardDesign_CreateMineIndicator(self):
        for val in range(self.dim_x*self.dim_y):
            if not self.cell_array[val].Cell_IsMine():
                mine_count = 0
                neighbour = self.cell_array[val].Cell_GetNeighbourCells(int(val/self.dim_y), (val % self.dim_y), dim_x, dim_y, 1)
                for cell in neighbour:
                    if self.cell_array[cell].Cell_IsMine():
                        mine_count += 1
                self.cell_array[val].Cell_setindicator(mine_count)
            else:
                self.cell_array[val].Cell_setindicator(9)   # Already a mine. Set invalid value

    def BoardDesign_generatepermutations(self):
        permutation_list = []
        for i in range(2,9):
            permutation_list.append(list(map(list, itertools.product([0, 1], repeat=i))))

        return permutation_list

    def ExploreAllOpenBlocks(self,node,KB,explored_cells):
        # Solve it as a BFS.
        Node_queue = queue.Queue()
        open_cells = []
        edge_cells = []
        indicator = 0
        Do_reduction = False
        neighbour_1 = []
        local_node = node
        Node_queue.put(local_node)
        while not Node_queue.empty():
            local_node = Node_queue.get()
            indicator = self.cell_array[local_node].Cell_getindicator()
            neighbour = KB.KnowledgeBase_GetUnexploredNeighbours(local_node,1,True)
            if indicator == 0:
                for cell in neighbour:
                    if not self.cell_array[cell].Cell_isexplored():
                        #self.cell_array[cell].Cell_setexplored()
                        KB.KnowledgeBase_add_entry(tuple([cell]),0)
                        KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
                        #if cell not in open_cells:
                        #    open_cells.append(cell) # Add to opened cells list
                        indicator = self.cell_array[cell].Cell_getindicator()
                        if indicator == 0:
                            neighbour_1 = KB.KnowledgeBase_GetUnexploredNeighbours(cell,1,False)
                            for n in neighbour_1:
                                if n not in Node_queue.queue and n not in neighbour:
                                    Node_queue.put(n)
                        #else:
                        #    neighbour_1 = KB.KnowledgeBase_GetUnexploredNeighbours(cell,1,True)
                        #    if len(neighbour_1) > 0:
                        #        Do_reduction = True
                        #        KB.KnowledgeBase_add_entry(tuple(neighbour_1),indicator)
                        #        KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
                        #        if cell not in edge_cells:
                        #            edge_cells.append(cell) # Add to edge cells list

            elif indicator == len(neighbour):
                for n in neighbour:
                    self.cell_array[n].Cell_flagmine()
                    if n not in KB.mine_cells:
                        KB.mine_cells.append(n)
                    KB.KnowledgeBase_add_entry(tuple([n]),1)
                    KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
            elif len(neighbour) > 0:
                Do_reduction = True
                KB.KnowledgeBase_add_entry(tuple(neighbour),indicator)
                KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
                if local_node not in edge_cells:
                    edge_cells.append(local_node) # Add to edge cells list
                    
            assert(not self.cell_array[local_node].Cell_IsFlaggedMine()) # Check valid cell
            self.cell_array[local_node].Cell_setexplored()
            KB.KnowledgeBase_add_entry(tuple([local_node]),0)
            KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
            if local_node not in open_cells and local_node not in explored_cells:
                open_cells.append(local_node) # Add to opened cells list
            if Do_reduction:
                # When we are at edge cells, reduce the current knowledge base
                KB.KnowledgeBase_solve()

        return open_cells,edge_cells

    def StartExploration(self,start,master,w):
        self.cell_array[start].Cell_setexplored()
        hit_mine = False
        KB = KnowledgeBase(self)
        explored_cells = []
        assert (not self.cell_array[start].Cell_IsMine())
        # Update knowledge base
        KB.KnowledgeBase_add_entry(tuple([start]),0)
        self.cell_array[start].Cell_setexplored()
        explored_cells.append(start)
        node = start
        # Start exploration
        while (len(explored_cells) != ((self.dim_x*self.dim_y) - self.mine_count)) and not hit_mine:
            n = 0
            edge_cells = []
            indicator = self.cell_array[node].Cell_getindicator()
            neighbour = KB.KnowledgeBase_GetUnexploredNeighbours(node,1,True)
            if indicator == 0:
                new_explored,edge_cells = self.ExploreAllOpenBlocks(node,KB,explored_cells)
                explored_cells.extend(new_explored)
                n += len(new_explored)
            elif indicator == len(neighbour):
                for cell in neighbour:
                    self.cell_array[cell].Cell_flagmine()
                    if cell not in KB.mine_cells:
                        KB.mine_cells.append(cell)
                    KB.KnowledgeBase_add_entry(tuple([cell]),1)
                    KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
            elif len(neighbour) > 0:
                KB.KnowledgeBase_add_entry(tuple(neighbour),indicator)
                KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))

            if len(explored_cells) < ((self.dim_x*self.dim_y) - self.mine_count):   # Check if all nodes are already explored
                random_choice = False
                # Get next safe cell to explore using equation reductions
                node = KB.KnowledgeBase_solve()
                if node == -1:  # No safe cell found using reductions. 
                    # Try substitution
                    node = KB.KnowledgeBase_substitution()
                    if node == -1:
                        # Try random exploration
                        node = KB.KnowledgeBase_random_explore(edge_cells,explored_cells,neighbour)
                        random_choice = True

                assert(node != -1)
                self.cell_array[node].Cell_setexplored()

                # Confirm if the choice was correct
                if self.cell_array[node].Cell_IsMine():
                    # Hit a mine
                    hit_mine = True
                else:
                    if tuple([node]) not in KB.kb.keys():
                        KB.KnowledgeBase_add_entry(tuple([node]),0)
                        KB.kb = OrderedDict(sorted(KB.kb.items(), key=lambda x: len(x[0])))
                    explored_cells.append(node) # Add explored cell to list

                    if random_choice:
                        # If we have successfully selected a node based on random choice, try some reductions here 
                        KB.KnowledgeBase_solve()

            if explored_cells:
                master.after(1000,self.color_cell(explored_cells,w,'red'))
            if KB.mine_cells:
                master.after(1000,self.color_cell(KB.mine_cells,w,'yellow'))

            # Explored count exceeded number of cells
            assert(len(explored_cells) <= ((self.dim_x*self.dim_y) - self.mine_count))
            master.update_idletasks()
            master.update()
            #print(KB.kb)
 
        #print(KB.kb)
        #print("Node hit - %d"%node)
        return hit_mine, len(explored_cells), explored_cells


    def PrintBoard(self):
        # Print values
        print("Board")
        for cell_x in range(0,self.dim_x):
            for cell_y in range(0, self.dim_y):
                print("%d  "%int(self.cell_array[cell_x * self.dim_y + cell_y].Cell_IsMine()),end="")
            print()

        # Print indicators
        print("Mine indicators")
        for cell_x in range(0,self.dim_x):
            for cell_y in range(0, self.dim_y):
                print("%d  "%self.cell_array[cell_x * self.dim_y + cell_y].Cell_getindicator(),end="")
            print()

    def color_cell(self,explored_cells,w,color):
        for each_cell in explored_cells:
                w.itemconfigure(each_cell+1, fill=color)

class KnowledgeBase:
    def __init__(self, BoardDesign):
        self.board = BoardDesign
        self.kb = {}
        self.permuation_list = BoardDesign.BoardDesign_generatepermutations()
        self.mine_cells = []

    def KnowledgeBase_add_entry(self,key,value):
        assert(value <= 8)
        assert(len(key) > 0)
        assert(len(key) >= value)
        key_list = [(len(key) == len(k) and sorted(key) == sorted(k)) for k in self.kb.keys()]
        if not self.kb or not any(k is True for k in key_list):
            self.kb.update({key:value})

    def KnowledgeBase_remove_entry(self,key):
        try:
            self.kb.pop(key)
        except KeyError:
            print("Key not found")
            assert(0)

    def KnowledgeBase_getkey(self,index):
        assert(index < len(self.kb))
        return list(self.kb.keys())[index]

    def KnowledgeBase_getvalue(self,index):
        assert(index < len(self.kb))
        return list(self.kb.values())[index]

    def KnowledgeBase_setvalue(self,index,value):
        assert(index < len(self.kb))
        list(self.kb.values())[index] = value

    def KnowledgeBase_getpermutations(self,key_length):
        assert(key_length <= 6 and key_length >= 0)
        return self.permuation_list[key_length]

    def KnowledgeBase_discardpermutationsforValue(self,permutations,value):
        valid_permutations = []
        for entry in permutations:
            entry = str(''.join(str(i) for i in entry))
            if entry.count("1") == value:
                valid_permutations.append(str(entry).zfill(len(permutations[0])))

        return valid_permutations

    def KnowledgeBase_GetMissingSecondOrderNeighbours(self,node,row,col,dim_x,dim_y):
        n1 = []
        n2 = []
        n3 = []
        n4 = []
        if row > 0:
            node_1 = (row - 1) * dim_y + col
            n1 = self.board.cell_array[node_1].Cell_GetNeighbourCells(int(node_1/dim_y),node_1%dim_y,dim_x,dim_y,1)

        if row < dim_x - 1:
            node_1 = (row + 1) * dim_y + col
            n2 = self.board.cell_array[node_1].Cell_GetNeighbourCells(int(node_1/dim_y),node_1%dim_y,dim_x,dim_y,1)

        if col > 0:
            node_1 = row * dim_y + (col - 1)
            n3 = self.board.cell_array[node_1].Cell_GetNeighbourCells(int(node_1/dim_y),node_1%dim_y,dim_x,dim_y,1)

        if col < dim_y - 1:
            node_1 = row * dim_y + (col + 1)
            n4 = self.board.cell_array[node_1].Cell_GetNeighbourCells(int(node_1/dim_y),node_1%dim_y,dim_x,dim_y,1)

        n1 = list(set(n1).union(set(n2),set(n3),set(n4)))
        return n1

    def KnowledgeBase_GetUnexploredNeighbours(self,node,order,Include_mine):
        unexplored = []
        # First order neighbours
        neighbours = self.board.cell_array[node].Cell_GetNeighbourCells(int(node/self.board.dim_y),node%self.board.dim_y,self.board.dim_x,self.board.dim_y,1)
        if order == 2:
            # Second order neighbours
            neighbours_1 = self.board.cell_array[node].Cell_GetNeighbourCells(int(node/self.board.dim_y),node%self.board.dim_y,self.board.dim_x,self.board.dim_y,order)

        if order == 1:
            for n in neighbours:
                if not self.board.cell_array[n].Cell_isexplored() and (Include_mine or not self.board.cell_array[n].Cell_IsFlaggedMine()):
                    unexplored.append(n)
        else:
            neighbours_2 = self.KnowledgeBase_GetMissingSecondOrderNeighbours(node,int(node/self.board.dim_y),node%self.board.dim_y,self.board.dim_x,self.board.dim_y)
            neighbours_2 = list(set(neighbours_2).union(set(neighbours_1)))
            for n in neighbours_2:
                if not self.board.cell_array[n].Cell_isexplored() and n != node and n not in neighbours:
                    unexplored.append(n)

        return unexplored

    def KnowledgeBase_solve(self):
        index = 0
        reduction = True
        safe_node = []
        while reduction:
            reduction_count = 0
            reduction_dict = {}
            redundancy_list = []
            for index in range(0,len(self.kb)-1):
                entry = self.KnowledgeBase_getkey(index)
                value_org = self.KnowledgeBase_getvalue(index)

                # Check if we already have a unexplored safe cell
                if len(entry) == 1 and value_org == 0 and not self.board.cell_array[entry[-1]].Cell_isexplored() \
                    and entry[-1] not in safe_node:
                    safe_node.append(entry[-1])

                for index_1 in range(index+1,len(self.kb)):
                    next_entry = self.KnowledgeBase_getkey(index_1)
                    if set(entry).issubset(next_entry):
                        # Use set intersection for speed
                        new_key = list(set(next_entry) - set(entry))
                        new_val = self.KnowledgeBase_getvalue(index_1) - value_org
                        assert (len(new_key) > 0) # No duplicate entries in the KB
                        assert (new_val >= 0)    # Check value range. Should be positive
                        assert (new_val <= 8)
                        # If the new value is 0, each node in the key is 0
                        # If the new value is equal to the number of nodes in the key, each node in the key is 1
                        # i.e A + B + C = 0 => A=0, B=0, C=0
                        # and A + B + C = 3 => A=1, B=1, C=1
                        reduction_dict = {}
                        if new_val == 0 or new_val == len(new_key):
                            for key_1 in new_key:
                                # Check for safe node and update
                                if new_val == 0 and not self.board.cell_array[key_1].Cell_isexplored():
                                    if key_1 not in safe_node:
                                        safe_node.append(key_1)
                                    reduction_dict.update({tuple([key_1]):0})
                                    #print("Node S = %d"%key_1)
                                elif new_val == len(new_key) and not self.board.cell_array[key_1].Cell_IsFlaggedMine():
                                    self.board.cell_array[key_1].Cell_flagmine()
                                    if key_1 not in self.mine_cells:
                                        self.mine_cells.append(key_1)
                                    reduction_dict.update({tuple([key_1]):1})         
                        else:
                            if tuple(new_key) not in reduction_dict:
                                reduction_dict.update({tuple(new_key):new_val})

                        # Update redundant elements in the KB(using reduction done above)
                        if next_entry not in redundancy_list: # Avoid duplication
                            redundancy_list.append(next_entry)
                        reduction_count += 1

            if not reduction_count:
                reduction = False
            else:
                # Remove all the redundant entries from KB
                for key in redundancy_list:
                    self.KnowledgeBase_remove_entry(key)
                for key,value in reduction_dict.items():
                    self.KnowledgeBase_add_entry(key,value)
                self.kb = OrderedDict(sorted(self.kb.items(), key=lambda x: len(x[0])))

        node = -1
        if safe_node:
            # Find a safe node with minimum surrounding mines
            node = safe_node[0]
            indicator = self.board.cell_array[node].Cell_getindicator()
            for s in safe_node:
                if self.board.cell_array[s].Cell_getindicator() < indicator:
                    node = s
                    indicator = self.board.cell_array[node].Cell_getindicator()
        return node

    def KnowledgeBase_substitution(self):
        index = 0
        safe_node = []
        safe_cell = -1
        Found_eq = False
        Update = False

        for index in range(0,len(self.kb)-1):
            entry = self.KnowledgeBase_getkey(index)
            if len(entry) > 1:
                Found_eq = True
                break

        if Found_eq:
            Found_permutation = False

            while (index < len(self.kb) - 1) and not Found_permutation and not Update:
                permutations = self.KnowledgeBase_getpermutations(len(entry)-2)
                permutations = self.KnowledgeBase_discardpermutationsforValue(permutations,self.KnowledgeBase_getvalue(index))

                lst = []
                conflict = False
                Overlap = False

                for pr in permutations:
                    lst = [int(d) for d in str(pr)]
                    conflict = False
                    Overlap = False
                    Overlap_count = 0
                    substitution = {}
                    intersecting = ()
                    not_intersecting = ()
                    for k,v in zip(entry,lst):
                        substitution.update({k:v})

                    for i in range(index+1,len(self.kb)):
                        new_entry = self.KnowledgeBase_getkey(i)
                        intersecting = list(set(new_entry).intersection(set(entry)))
                        not_intersecting = list(set(new_entry) - set(intersecting))
                        if intersecting:
                            Overlap_count += 1
                            accumulated_sum = 0
                            Overlap = True
                            for key in intersecting:
                                accumulated_sum += substitution.get(key)
                            if (self.KnowledgeBase_getvalue(i) - accumulated_sum) < 0:
                                # Conflict detected, check if we can get a concrete observation
                                if len(intersecting) == (len(new_entry) - 1): # n-1 intersecting nodes
                                    not_intersecting_curr = list(set(entry) - set(intersecting))
                                    safe_node.insert(0,not_intersecting[-1])
                                    self.KnowledgeBase_add_entry(tuple([not_intersecting[-1]]),0)
                                    self.board.cell_array[not_intersecting_curr[-1]].Cell_flagmine()
                                    if not_intersecting_curr[-1] not in self.mine_cells:
                                        self.mine_cells.append(not_intersecting_curr[-1])
                                    self.KnowledgeBase_add_entry(tuple([not_intersecting_curr[-1]]),1)
                                    self.kb = OrderedDict(sorted(self.kb.items(), key=lambda x: len(x[0])))
                                    Update = True
                                conflict = True
                                break
                            elif (self.KnowledgeBase_getvalue(i) - accumulated_sum) > len(not_intersecting):
                                # Conflict detected, check if we can get a concrete observation
                                if len(intersecting) == (len(new_entry) - 1): # n-1 intersecting nodes
                                    not_intersecting_curr = list(set(entry) - set(intersecting))
                                    safe_node.insert(0,not_intersecting_curr[-1])
                                    self.KnowledgeBase_add_entry(tuple([not_intersecting_curr[-1]]),0)
                                    self.board.cell_array[not_intersecting[-1]].Cell_flagmine()
                                    if not_intersecting[-1] not in self.mine_cells:
                                        self.mine_cells.append(not_intersecting[-1])
                                    self.KnowledgeBase_add_entry(tuple([not_intersecting[-1]]),1)
                                    self.kb = OrderedDict(sorted(self.kb.items(), key=lambda x: len(x[0])))
                                    Update = True
                                conflict = True
                                break

                    if Overlap_count >= 3 and not conflict:
                        # Found the permutation
                        Found_permutation = True
                        break
                    elif not Overlap or Update:
                        # No overlap found. Move to the next equation
                        break

                if Found_permutation:    # Use substitutions with no conflicts with the KB
                    #assert(lst)
                    for key,value in substitution.items():
                        if value == 1:
                            self.board.cell_array[key].Cell_flagmine()
                            if key not in self.mine_cells:
                                self.mine_cells.append(key)
                        else:
                            safe_node.append(key)
                        self.KnowledgeBase_add_entry(tuple([key]),value)

                    self.kb = OrderedDict(sorted(self.kb.items(), key=lambda x: len(x[0])))
                    self.KnowledgeBase_remove_entry(entry)
                    Update = True

                index += 1
                if (index < len(self.kb) - 1):
                    entry = self.KnowledgeBase_getkey(index)

        # Check if an update was made to the knowledge base. If yes then do reduction
        if Update:
            safe_cell = self.KnowledgeBase_solve()

        if safe_node and safe_cell == -1:
            safe_cell = safe_node[0]
        return safe_cell

    def KnowledgeBase_ChooseRandomNode(self,neighbour_edge,neighbour_exp):
        # Choose a random cell to explore
        Found_Cell = False
        while not Found_Cell:
            safe_node = random.randint(0,(self.board.dim_x * self.board.dim_y) - 1)
            if not self.board.cell_array[safe_node].Cell_isexplored() and not self.board.cell_array[safe_node].Cell_IsFlaggedMine():# \
                #and safe_node not in neighbour_edge and safe_node not in neighbour_exp:
                Found_Cell = True

        return safe_node

    def KnowledgeBase_random_explore(self,edge_cells,explored_cells,neighbour_cells):
        # Random exploration
        #neighbours = []
        #neighbours_sec = []
        safe_node = -1
        if edge_cells:
            for edge in edge_cells:
                indicator = self.board.cell_array[edge].Cell_getindicator()
                assert(indicator > 0)
                neighbour_edge = self.KnowledgeBase_GetUnexploredNeighbours(edge,1,True)
                neighbour_update = []
                for n in neighbour_edge:
                    if not self.board.cell_array[n].Cell_IsFlaggedMine():
                        neighbour_update.append(n)

                # If indicator is < 40% of unexplored cells, it is a safe to chose the next node from the neighbours
                if len(neighbour_edge) and (indicator / len(neighbour_edge)) < 0.4:
                    safe_node = neighbour_update[random.randint(0,len(neighbour_update)-1)]
                    break

        if safe_node == -1 and explored_cells:
            node = explored_cells[-1]
            indicator = self.board.cell_array[node].Cell_getindicator()
            # If indicator is < 40% of unexplored cells, it is a safe to chose the next node from the neighbours
            if len(neighbour_cells) and (indicator / len(neighbour_cells)) < 0.4:
                safe_node = neighbour_cells[random.randint(0,len(neighbour_cells)-1)]

            # Choose from Second order neighbours
            #neighbours_sec = self.KnowledgeBase_GetUnexploredNeighbours(node,2,False)
            #if len(neighbours_sec) > 0 and len(neighbours_sec) >= 3:
            #    safe_node = neighbours_sec[random.randint(0,len(neighbours_sec)-1)]
            #else:
            #    # If there are few unexplored second order neighbours, choose randomly
            #    safe_node = self.KnowledgeBase_ChooseRandomNode(neighbours,neighbours_sec)

        # Try exploring the corner cells
        if safe_node == -1 and not self.board.cell_array[self.board.dim_y - 1].Cell_isexplored() and \
                not self.board.cell_array[self.board.dim_y - 1].Cell_IsFlaggedMine():
                safe_node = self.board.dim_y - 1

        if safe_node == -1 and not self.board.cell_array[self.board.dim_x * (self.board.dim_y - 1)].Cell_isexplored() and \
                not self.board.cell_array[self.board.dim_x * (self.board.dim_y - 1)].Cell_IsFlaggedMine():
                safe_node = self.board.dim_x * (self.board.dim_y - 1)

        if safe_node == -1 and not self.board.cell_array[(self.board.dim_x * self.board.dim_y) - 1].Cell_isexplored() and \
                not self.board.cell_array[(self.board.dim_x * self.board.dim_y) - 1].Cell_IsFlaggedMine():
                safe_node = (self.board.dim_x * self.board.dim_y) - 1

        if safe_node == -1:
            # Choose randomly
            safe_node = self.KnowledgeBase_ChooseRandomNode(edge_cells,neighbour_cells)
            
        return safe_node


# Start Minesweeper
type = 0
if type == 0:
    # Beginner
    dim_x = dim_y = 9
    num_mines = 10
elif type == 1:
    # Intermediate
    dim_x = dim_y = 16
    num_mines = 40
else:
    # Expert
    dim_x = 16
    dim_y = 30
    num_mines = 99

passed_count = 0
#for i in range(0,100):
B = BoardDesign(dim_x,dim_y,num_mines,0)
B.BoardDesign_CreateBoard()
B.BoardDesign_CreateMineIndicator()
B.PrintBoard()

master = Tk()
w = Canvas(master,width=2000,height=2000)
w.pack()
if dim_x!=dim_y:
    size_x = int(600 / dim_x)
    size_y = int(1300 / dim_y)
else:
    size_x = int(600 / dim_x)
    size_y = int(600 / dim_y)

for height in range(1,dim_x+1):
        for width in range(0,dim_y):
            w.create_rectangle((width * size_x)+size_x, size_y*height, (width*size_x)+(size_x*2), (size_y*height)+size_y,fill='#fff')

# Choose a corner as starting point(minimum unknowns on exploration)
start_point = 0
hit_mine, exploration_count, explored_cells = B.StartExploration(start_point,master,w)

if not hit_mine:
    passed_count += 1
# Display exploration path
#print("Explored cells")
#print(explored_cells)
print("hit mine - %d Exploration count = %d"%(hit_mine,exploration_count))

#print("Number of games solved - %d"%passed_count)
master.mainloop()

