# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


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
    def find(self, node, value, tof=True):
        """
        Takes in a value and returns the node which match the value. If false it will
        return the parent node or the node if already exists.
        """
        if node is not None:
            if node.value > value:
                if node.left is not None:
                    return self.find(node.left, value, tof)
                else:
                    return node
            else:
                if not tof and node.value == value:
                    return node
                elif node.right is not None:
                    return self.find(node.right, value, tof)
                else:
                    return node

    def add(self, value: object) -> None:
        """
        Adds a node containing value to the AVL tree, if it doesn't already exist
        """
        node = AVLNode(value)
        if self._root is None:
            self._root = node
            return
        # from this point on we are dealing with thing with parents
        parentNode = self.find(self._root, value, False)

        if parentNode.value == value: # duplicates begone
            return
        if parentNode.value > value:
            parentNode.left = node
        else:
            parentNode.right = node
        node.parent = parentNode
        self._update_height(node)
        self._rebalance(node)

    def remove(self, value: object) -> bool:

        if self._root is None:
            return False
        node = self.find(self._root, value, False)
        parent = node.parent
        if node == self._root:
            if node.left is None and node.right is None:
                self._root = None
                return True
            elif node.left is None:
                self._root = self._root.right
            elif node.right is None:
                self._root = self._root.left
            else:
                succ = self._root.right
                while succ.left is not None:
                    succ = succ.left
                succ.left = self._root.left
                succ.left.parent = succ
                parent = None
                if succ.parent is not self._root:
                    parent = succ.parent
                    parent.left = succ.right
                    if parent.left is not None:
                        parent.left.parent = parent
                    succ.right = self._root.right
                    succ.right.parent = succ
                else:
                    succ.right = self._root.right.right
                    if succ.right is not None:
                        succ.right.parent = succ
                self._root = succ
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

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:

        parent = remove_parent
        node = remove_node
        succ = node.right
        while succ.left is not None:
            succ = succ.left
        succ.left = node.left
        succ.left.parent = succ
        succParent = None
        if succ.parent is not node:
            succParent = succ.parent
            succ.parent.left = succ.right
            if succParent.left is not None:
                succParent.left.parent = succParent
        if node.right != succ:
            succ.right = node.right
        else:
            succ.right = node.right.right
        if succ.right is not None:
            succ.right.parent = succ
        if parent.left == node:
            parent.left = succ
        else:
            parent.right = succ
        succ.parent = parent
        if succParent is not None:
            self._update_height(succParent)
            self._rebalance(succParent)
        else:
            self._update_height(succ)
            self._rebalance(succ)
        return succ

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #

    def _balance_factor(self, node: AVLNode) -> int:

        lheight = 0
        rheight = 0

        if node.right is not None:
            rheight = node.right.height
        if lheight is not None:
            lheight = node.left.height

        return rheight - lheight

    def _get_height(self, node: AVLNode) -> int:

        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Takes in a node and performs a left rotation assuming that all pre-conditions
        are met. Updates the parent for all nodes involved.
        """
        # you got to think of this like a linked list
        parent = None

        if node.parent is not None:
            parent = node.parent

        rightNode = node.right
        node.right = rightNode.left

        if node.right is not None:
            node.right.parent = node

        rightNode.left = node

        if parent is None:
            self._root = rightNode
            self._root.parent = None

        else:
            rightNode.parent = parent
            if parent.right == node:
                parent.right = rightNode
            else:
                parent.left = rightNode

        node.parent = rightNode
        self._update_height(node)
        return node

    def _rotate_right(self, node: AVLNode) -> AVLNode:

        parent = None
        if node.parent is not None:
            parent = node.parent
        leftNode = node.left
        node.left = leftNode.right
        if node.left is not None:
            node.left.parent = node
        leftNode.right = node
        if parent is None:
            self._root = leftNode
            self._root.parent = None
        else:
            leftNode.parent = parent
            if parent.right == node:
                parent.right = leftNode
            else:
                parent.left = leftNode
        node.parent = leftNode
        self._update_height(node)
        return node



    def _update_height(self, node: AVLNode) -> None:

        if node.left is not None and node.right is not None:
            if node.left.height > node.right.height:
                node.height = node.left.height + 1
            else:
                node.height = node.right.height + 1
        elif node.left is None and node.right is None:
            node.height = 0
        elif node.left is None:
            node.height = node.right.height + 1
        elif node.right is None:
            node.height = node.left.height + 1

        while node.parent is not None:
            # parents are at least of height one
            parent = node.parent
            left, right = parent.left, parent.right
            if parent.left is not None and parent.right is not None:
                if parent.left.height > parent.right.height:
                    parent.height = parent.left.height + 1
                else:
                    parent.height = parent.right.height + 1
            elif parent.right is None:
                parent.height = parent.left.height + 1
            else:
                parent.height = parent.right.height + 1
            node = node.parent

    def _rebalance(self, node: AVLNode) -> None:
        """
                Takes in a node and rebalances the node starting from that node and all parents involved
                Everything below that node is assumed to already be balanced.
                """
        # we are starting from the node we just added in, so everything below 
        # that is already balanced, so we don't need to worry, so we really 
        # should care about the case where node.left and node.right are both not
        # None
        if node is not None:
            if node.left is not None and node.right is not None:
                height = node.right.height - node.left.height
                if height == 2:  # right heavy, now need to check if it is right right or right left
                    if node.right.left is None or (
                            node.right.right is not None and node.right.left.height <= node.right.right.height):
                        self._rotate_left(node)
                    else:  # right left 
                        self._rotate_right(node.right)  # this extra step is required to make it right right heavy
                        self._rotate_left(node)
                elif height == -2:  # left heavy, now need to check if it is left left or left right
                    if node.left.right is None or (
                            node.left.left is not None or node.left.left.height >= node.left.right.height):
                        self._rotate_right(node)
                    else:  # left right, rotate left first then right 
                        self._rotate_left(node.left)  # this extra step is required to make it left left heavy
                        self._rotate_right(node)
            elif node.right is None and node.height == 2:
                # we need to make sure that it is left left 
                if node.left.right is None or (
                        node.left.left is not None and node.left.left.height >= node.left.right.height):
                    self._rotate_right(node)
                else:
                    self._rotate_left(node.left)  # this extra step is required to make it left left heavy
                    self._rotate_right(node)
            elif node.left is None and node.height == 2:
                # we need to make sure that it is right right 
                if node.right.left is None or (
                        node.right.right is not None and node.right.right.height >= node.right.left.height):
                    self._rotate_left(node)
                else:
                    self._rotate_right(node.right)  # this extra step is required to make it right right heavy
                    self._rotate_left(node)
            self._rebalance(node.parent)


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
