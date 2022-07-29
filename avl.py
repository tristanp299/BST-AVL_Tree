# Name: Tristan Pereira
# OSU Email: pereirtr
# Course: CS261 - Data Structures
# Assignment: Assignment 4 BST/AVL Tree Implementation
# Due Date: 07/26/2022
# Description: avl.py contains two classes AVLNode and AVL. This script implements an AVL Tree with methods to manipulate nodes inside the tree.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #
    def find(self, node: AVLNode, value: object) -> AVLNode:
        '''find function takes in a node and a value as a paremter, searches for that node and then returns it '''
        
        if node is not None:
            if node.value > value:
                if node.left is not None:
                    return self.find(node.left, value)
                else:
                    return node
            else:
                if node.value == value:
                    return node
                elif node.right is not None:
                    return self.find(node.right, value)
                else:
                    return node

    def add(self, value: object) -> None:
        '''add function places a new AVL node into the appropriate spot in the AVL Tree'''
        
        node = AVLNode(value)
        if self._root is None:
            self._root = node
            return

        parent = self.find(self._root, value)

        if parent.value == value: 
            return
        if parent.value > value:
            parent.left = node
        else:
            parent.right = node
            
        node.parent = parent
        self._update_height(node)
        self._rebalance(node)

    def remove(self, value: object) -> bool:
        '''remove function takes in a value and removes that node from AVL tree. If node is removed it returns True, otherwise returns False'''
        
        if self._root is None:
            return False
        if not self.contains(value):
            return False
        node = self.find(self._root, value)
        parent = node.parent

        #removes if node is the root
        if node == self._root:
            #if leaf
            if node.left is None and node.right is None:
                self._root = None
                return True
            elif node.left is None:
                self._root = self._root.right
            elif node.right is None:
                self._root = self._root.left
            else:#
                #if there are two subtrees.
                inorder_succ = self._root.right
                #finds inorder successor
                while inorder_succ.left is not None:
                    inorder_succ = inorder_succ.left
                inorder_succ.left = self._root.left
                inorder_succ.left.parent = inorder_succ
                parent = None
                
                if inorder_succ.parent is not self._root:
                    parent = inorder_succ.parent
                    parent.left = inorder_succ.right

                    if parent.left is not None:
                        parent.left.parent = parent
                    inorder_succ.right = self._root.right
                    inorder_succ.right.parent = inorder_succ

                else:
                    inorder_succ.right = self._root.right.right
                    if inorder_succ.right is not None:
                        inorder_succ.right.parent = inorder_succ
                self._root = inorder_succ
                self._root.parent = None

                if parent is not None:
                    self._update_height(parent)
                    self._rebalance(parent)
                    return True

            self._root.parent = None
            self._update_height(self._root)
            self._rebalance(self._root)
            return True

        elif node.left is None and node.right is None:

            if node == parent.left:
                parent.left = None
            else:
                parent.right = None
            self._update_height(parent)
            self._rebalance(parent)
            return True
        elif node.left is None:

            if node == parent.left:
                parent.left = node.right
            else:
                parent.right = node.right
            node.right.parent = parent
            self._update_height(parent)
            self._rebalance(parent)
            return True

        elif node.right is None:

            if node == parent.left:
                parent.left = node.left
            else:
                parent.right = node.left
            node.left.parent = parent
            self._update_height(parent)
            self._rebalance(parent)
            return True
        else:
            self._remove_two_subtrees(parent, node)
            return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        '''_remove_two_subtrees removes a node if there are two subtrees as child nodes. This function only works if removed node is not root.'''

        parent = remove_parent
        node = remove_node
        inorder_succ = node.right

        #finds the successor for removed node
        while inorder_succ.left is not None:
            inorder_succ = inorder_succ.left

        inorder_succ.left = node.left
        inorder_succ.left.parent = inorder_succ
        inorder_succ_parent = None

        if inorder_succ.parent is not node:
            inorder_succ_parent = inorder_succ.parent
            inorder_succ.parent.left = inorder_succ.right

            if inorder_succ_parent.left is not None:
                inorder_succ_parent.left.parent = inorder_succ_parent

        if node.right.value != inorder_succ.value:
            inorder_succ.right = node.right
        else:
            inorder_succ.right = node.right.right

        if inorder_succ.right is not None:
            inorder_succ.right.parent = inorder_succ

        if parent.left.value == node.value:
            parent.left = inorder_succ
        else:
            parent.right = inorder_succ

        inorder_succ.parent = parent

        if inorder_succ_parent is not None:
            self._update_height(inorder_succ_parent)
            self._rebalance(inorder_succ_parent)

        else:
            self._update_height(inorder_succ)
            self._rebalance(inorder_succ)

        return inorder_succ

    def _balance_factor(self, node: AVLNode) -> int:
        '''_balance_factor function takes in a node and returns the balance factor of the node.'''

        lheight = 0
        rheight = 0

        if node.right is not None:
            rheight = node.right.height
        if node.left is not None:
            lheight = node.left.height

        return rheight - lheight

    def _get_height(self, node: AVLNode) -> int:
        '''_get_height function takes in node and returns the height of the node.'''

        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        '''_rotate_left functions takes in a node and rotates it left along the AVL tree structure and returns the node with updated parents and child nodes.'''

        parent = None

        if node.parent is not None:
            parent = node.parent

        node_right = node.right
        node.right = node_right.left

        if node.right is not None:
            node.right.parent = node

        node_right.left = node

        if parent is None:
            
            self._root = node_right
            self._root.parent = None

        else:
            node_right.parent = parent

            if parent.right == node:
                parent.right = node_right
            else:
                parent.left = node_right

        node.parent = node_right
        self._update_height(node)
        return node

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        '''_rotate_right functions takes in a node as a parameter and rotates it right along the AVL tree. It returns the node with updated parents and children'''
        parent = None
        
        if node.parent is not None:
            parent = node.parent
            
        node_left = node.left
        node.left = node_left.right
        
        if node.left is not None:
            node.left.parent = node
            
        node_left.right = node
        
        if parent is None:
            self._root = node_left
            self._root.parent = None
        else:
            node_left.parent = parent
            if parent.right == node:
                parent.right = node_left
            else:
                parent.left = node_left
                
        node.parent = node_left
        self._update_height(node)
        return node



    def _update_height(self, node: AVLNode) -> None:
        '''update_height function takes in a node as a parameter and updates the height information of that node after a AVL tree operation.'''
        #double subtrees
        if node.left is not None and node.right is not None:
            if node.left.height > node.right.height:
                node.height = node.left.height + 1
            else:
                node.height = node.right.height + 1
        #leaf
        elif node.left is None and node.right is None:
            node.height = 0
        #no left subtree
        elif node.left is None:
            node.height = node.right.height + 1
        #no right subtree
        elif node.right is None:
            node.height = node.left.height + 1
        
        #traces up the tree and updates
        while node.parent is not None:

            parent = node.parent
            #double subtrees
            if parent.left is not None and parent.right is not None:
                if parent.left.height > parent.right.height:
                    parent.height = parent.left.height + 1
                else:
                    parent.height = parent.right.height + 1
            #no right subtree
            elif parent.right is None:
                parent.height = parent.left.height + 1
            #no left subtree
            else:
                parent.height = parent.right.height + 1
                
            node = node.parent

    def _rebalance(self, node: AVLNode) -> None:
        '''_rebalance function takes a node and checks for unbalanaced subtrees, the function will then do a single or double rotation based off the balance.'''

        if node is not None:
            #rebalance if two subtrees
            node_balance = self._balance_factor(node)


            # if node_balance < -1:
            #     node_left_balance_factor = self._balance_factor(node.left)
            #
            #     if node_left_balance_factor < 0:
            #         self._rotate_right(node)
            #
            #     elif node_left_balance_factor > 0:
            #
            #
            #         self._rotate_left(node.left)
            #         self._rotate_right(node)
            #
            # elif node_balance > 1:
            #
            #     node_right_balance_factor = self._balance_factor(node.right)
            #
            #     if node_right_balance_factor < 0:
            #
            #         self._rotate_right(node.right)
            #         self._rotate_left(node)
            #
            #     elif node_right_balance_factor > 0:
            #
            #         self._rotate_left(node)

            if node.left is not None and node.right is not None:
                node_balance = self._balance_factor(node)
                # right heavy
                if node_balance == 2:
                    # L - Single Rotate
                    r_node_balance = self._balance_factor(node.right)
                    if node.right.left is None or (node.right.right is not None and r_node_balance >= 0):
                        self._rotate_left(node)
                    # RL - Double Rotate
                    else:
                        self._rotate_right(node.right)
                        self._rotate_left(node)
                # left heavy
                elif node_balance == -2:
                    # L - Single Rotate
                    l_node_balance = self._balance_factor(node.left)
                    if node.left.right is None or (node.left.left is not None or l_node_balance <= 0):
                        self._rotate_right(node)
                    # LR - Double Rotate
                    else:
                        self._rotate_left(node.left)
                        self._rotate_right(node)
                # one subtree
            elif node.right is None and node.height == 2:
                # R - One rotation
                l_node_balance = self._balance_factor(node.left)
                if node.left.right is None or (node.left.left is not None and l_node_balance <= 0):
                    self._rotate_right(node)
                # LR - Doubel Rotation
                else:
                    self._rotate_left(node.left)
                    self._rotate_right(node)

            elif node.left is None and node.height == 2:
                # L - One Rotation
                r_node_balance = self._balance_factor(node.right)
                if node.right.left is None or (node.right.right is not None and r_node_balance >= 0):
                    self._rotate_left(node)
                # RL - Double Rotation
                else:
                    self._rotate_right(node.right)
                    self._rotate_left(node)

            self._rebalance(node.parent)

            # if node.left is not None and node.right is not None:
            #     node_balance = self._balance_factor(node)
            #     #right heavy
            #     if node_balance == 2:
            #         #L - Single Rotate
            #         if node.right.left is None:
            #             self._rotate_left(node)
            #         #RL - Double Rotate
            #         else:
            #             self._rotate_right(node.right)
            #             self._rotate_left(node)
            #     #left heavy
            #     elif node_balance == -2:
            #         #L - Single Rotate
            #         if node.left.right is None:
            #             self._rotate_right(node)
            #         #LR - Double Rotate
            #         else:
            #             self._rotate_left(node.left)
            #             self._rotate_right(node)
            # #one subtree
            # elif node.right is None and node.height == 2:
            #     #R - One rotation
            #     if node.left.right is None:
            #         self._rotate_right(node)
            #     #LR - Doubel Rotation
            #     else:
            #         self._rotate_left(node.left)
            #         self._rotate_right(node)
            #
            # elif node.left is None and node.height == 2:
            #     #L - One Rotation
            #     if node.right.left is None
            #         self._rotate_left(node)
            #     #RL - Double Rotation
            #     else:
            #         self._rotate_right(node.right)
            #         self._rotate_left(node)
            #
            # self._rebalance(node.parent)


        # ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
