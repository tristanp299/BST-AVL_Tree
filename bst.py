# Name: Tristan Pereira
# OSU Email: pereirtr
# Course: CS261 - Data Structures
# Assignment: Assignment 4 BST/AVL Tree Implementation
# Due Date: 07/26/2022
# Description: bst.py is a script that implements a binary search tree. There are methods that help manipulate the data and nodes associated with them.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """add function thats in a value and adds that value to the appropiate spot on the BST"""

        if self._root is None:
            self._root = BSTNode(value)
            return
        cur = self._root
        parent = None

        while (cur is not None):
            parent = cur
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right

        if value< parent.value:
            parent.left = BSTNode(value)
        else:
            parent.right = BSTNode(value)

    # def find_node(self, value):
    #
    #     cur = self._root
    #
    #     while(cur is not None):
    #         if cur.value == value:
    #             return True
            

    def remove(self, value: object) -> bool:
        """remove function takes in a value and removes that value from the BST"""

        # iterate through tree in search of value
        left_bool = False
        node_found = False
        parent = None
        cur = self._root

        while cur is not None and not node_found:
            if value == cur.value:
                node_found = True
              
            elif value < cur.value:
                parent = cur
                cur = cur.left
                left_bool = True
              
            else:
                parent = cur
                cur = cur.right
                left_bool = False
        
        # handle case where value was not found in BST
        if not node_found:
            return False
        
        # handle case where node to remove is root
        if cur.value == self._root.value:
            if self._root.left is None and self._root.right is None:
                self._root = None
                return True
            #No right subtree
            if self._root.right is None:
                self._root = self._root.left
                return True
            #has right subtree
            cur = self._root.right
            parent = self._root
            left_bool = False
            #find successor
            while (cur.left is not None):
                parent = cur
                cur = cur.left
                left_bool = True
            if left_bool:
                parent.left = cur.right
            else:
                parent.right = cur.right
            #replace leftmost child into root
            cur.left = self._root.left
            cur.right = self._root.right
            self._root = cur
            return True
        #if node is a leaf
        if cur.left is None and cur.right is None and left_bool:
            parent.left = None
            return True
        if cur.left is None and cur.right is None and not left_bool:
            parent.right = None
            return True

        #if node has left subtree
        if cur.right is None and left_bool:
            parent.left = cur.left
            return True
        if cur.right is None and not left_bool:
            parent.right = cur.left
            return True

        #right subtree == true
        left_bool_2 = False
        new_node = cur.right
        new_node_parent = cur
        while(new_node.left is not None):
            new_node_parent = new_node
            new_node = new_node.left
            left_bool_2 = True

        #fill open spot
        if left_bool_2:
            new_node_parent.left = new_node.right
        if not left_bool_2:
            new_node_parent.right = new_node.right
        #insert successor
        if left_bool:
            parent.left = new_node
            new_node.left = cur.left
            new_node.right = cur.right
            return True
        if not left_bool:
            parent.right = new_node
            new_node.left = cur.left
            new_node.right = cur.right
            return True


        # Please ignore commented below, many different methods both recursive and iterative,
        # tried and failed. They are the scars I wear proudly. In hindsight, I should've used those helper functions.

        #
        # # handle case where cur is a leaf
        # if cur.left is None and cur.right is None and left_bool:
        #     parent.left = None
        #     return True
        # if cur.left is None and cur.right is None and not left_bool:
        #       parent.right = None
        # return True
        #
        # # handle case where cur only has left subtree
        # if cur.right is None and left_bool:
        #     parent.left = cur.left
        #     return True
        # if cur.right is None and not left_bool:
        #     parent.right = cur.left
        #     return True
        #
        # # handle case where cur has a right subtree
        # # find left-most child from right subtree
        # left_bool_2 = False
        # replace_node = cur.right
        # replace_parent = cur
        #
        # while replace_node.left is not None:
        #     replace_parent = replace_node
        #     replace_node = replace_node.left
        #     left_bool_2 = True
        #
        # # fill open slot from removing new_cur
        # if left_bool_2:
        #     replace_parent.left = replace_node.right
        # if not left_bool_2:
        #     replace_parent.right = replace_node.right
        #
        # # insert left-most child from right subtree in open spot
        # if left_bool:
        #     parent.left = replace_node
        #     replace_node.left = cur.left
        #     replace_node.right = cur.right
        #     return True
        # if not left_bool:
        #     parent.right = replace_node
        #     replace_node.left = cur.left
        #     replace_node.right = cur.right
        #     return True
          
        # if self._root == None:
        #     return False
        # else:
        #     if cur == None:
        #         cur = self._root

        #     if value == self._root.value:
        #        if cur.left is None and cur.right is None:
        #            self._root = None
        #            return True
        #        elif cur.left is None:
        #            self._root = cur.right
        #            return True
        #        elif cur.right is None:
        #            self._root = cur.left
        #            return True
        #
        #     elif value == cur.value:
        #         if cur.left is None and cur.right is None:
        #             cur = None
        #             return True
        #         elif cur.left is None:
        #             parent = cur.right
        #             return True
        #         elif cur.right is None:
        #             parent = cur.left
        #             return True
        #
        #         else:
        #             while(cur.left is not None):
        #                 cur = cur.left
        #             parent = cur
        #             cur.right = self.remove(value, cur.right, parent)
        #
        #     elif value< cur.value:
        #         parent = cur
        #         cur.left = self.remove(value, cur.left, parent)
        #     else:
        #         parent = cur
        #         cur.right = self.remove(value, cur.right, parent)
        # return False




        # elif self._root.value == value:
        #     if self._root.right is None and self._root.left is None:
        #         self._root = None
        #         return True
        #     elif self._root.right is None and self._root.left is not None:
        #         self._root = self._root.left
        #         return True
        #     elif self._root.right is not None and self._root.left is None:
        #         self._root = self._root.right
        #         return True
        #     else:
        #         self._root = self._root.right
        #         return True



    # Consider implementing methods that handle different removal scenarios; #
    # you may find that you're able to use some of them in the AVL.          #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change these methods in any way you'd like.                            #

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has no subtrees (no left or right nodes)
        pass

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has a left or right subtree (only)
        pass

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)
        pass

    def contains(self, value: object) -> bool:
        """contains function takes in a value and returns True if the value is in the BST, otherwise returns False"""

        cur = self._root

        while (cur is not None):
            if value == cur.value:
                return True
            elif value< cur.value:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def inorder_traversal(self, inorder = None, cur = None) -> Queue:
        """inorder_traversal traverses through the BST and returns a Qeueue with the elements in inorder positions"""

        if cur is None and inorder is None:
            cur = self._root
            inorder = Queue()

        if self._root is None:
            return inorder
        # L N R
        if cur.left is not None:
            self.inorder_traversal(inorder, cur.left)

        inorder.enqueue(cur.value)

        if cur.right is not None:
            self.inorder_traversal(inorder, cur.right)

        return inorder


    def find_min(self) -> object:
        '''find_min function finds the minimum value in the BST and returns that object.'''

        if self._root is None:
            return None

        num = self._root

        while(num.left is not None and num.value>num.left.value):
            num = num.left

        return num.value

    def find_max(self) -> object:
        """find_max finds the maximum value in the BST and returns that object."""

        if self._root is None:
            return None

        num = self._root

        while(num.right is not None and num.value<num.right.value):
            num = num.right
        return num.value

    def is_empty(self) -> bool:
        """is_empty function returns True if the BST is empty, otherwise returns False"""
        if self._root is None:
            return True
        return False

    def make_empty(self) -> None:
        """make_empty functions turns the BST to None."""

        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())


    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
