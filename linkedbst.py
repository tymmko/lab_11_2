"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import random
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)
    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            stri = ""
            if node != None:
                stri += recurse(node.right, level + 1)
                stri += "| " * level
                stri += str(node.data) + "\n"
                stri += recurse(node.left, level + 1)
            return stri

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root

        while node is not None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right
        return None
    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return None
        node = self._root
        while True:
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    self._size += 1
                    break
                else:
                    node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(item)
                    self._size += 1
                    break
                else:
                    node = node.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newitem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top: 
                rig = height1(top.right)
                lef = height1(top.left)
                return max(rig, lef) + 1
            return 0
        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() < 2 * log(self._size + 1) - 1 else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high
        :param low:
        :param high:
        :return:
        '''
        all_elems = self.inorder()
        elem_predecessor = self.predecessor(low)
        elem_successor = self.successor(high)
        if elem_predecessor is None:
            elem_predecessor = low
        list_output = []
        add_to_list = False
        for elem in all_elems:
            if elem == elem_predecessor:
                add_to_list = True
            if add_to_list:
                if elem_successor is not None and elem >= elem_successor:
                    break
                list_output.append(elem)
        if elem_predecessor == low:
            return list_output
        return list_output[1:]

    def rebalance_help(self, stack):
        '''helper methond for rebalance'''
        middle_elem = len(stack)//2
        if stack:
            self.add(stack[middle_elem])
            stack.pop(middle_elem)
            self.rebalance_help(stack[middle_elem:])
            self.rebalance_help(stack[:middle_elem])
        return None

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        new_array = list(self.inorder())
        self.clear()
        self.rebalance_help(new_array)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        all_elems = self.inorder()
        for elem in all_elems:
            if elem > item:
                return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        cur = None
        all_elems = self.inorder()
        for elem in all_elems:
            if elem < item:
                cur = elem
            else:
                return cur

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        with open(path) as file:
            word_list = file.read().splitlines()
    
        rand_words = random.sample(word_list, 10000)

        def search_10000_words():
            '''
            час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику
            '''
            start = time.time()
            for word in rand_words:
                rand_words.index(word)
            end = time.time()
            return end - start

        def search_binary_tree():
            '''
            час пошуку 10000 випадкових слів у словнику, 
            який представлений у вигляді бінарного дерева пошуку
            '''
            tree = LinkedBST()
            for elem2 in rand_words:
                tree.add(elem2)

            start2 = time.time()
            for word in rand_words:
                tree.find(word)
            finish2 = time.time()
            return finish2 - start2
            
        def find_word_mixed_list():
            '''
            час пошуку 10000 випадкових слів у словнику, 
            який представлений випадково у вигляді бінарного дерева пошуку
            '''
            tree = LinkedBST()
            for word in rand_words:
                tree.add(word)
            start_time = time.time()

            for word in word_list:
                tree.find(word)
            end_time = time.time()
            return end_time - start_time

        def search_rebalanced_tree():
            '''
            час пошуку 10000 випадкових слів у словнику, 
            який представлений у вигляді бінарного дерева пошуку 
            після його балансування
            '''
            tree = LinkedBST()
            for word in rand_words:
                tree.add(word)

            tree.rebalance()
            start_time = time.time()

            for word in rand_words:
                tree.find(word)

            return time.time() - start_time

        print('час пошуку 10000 випадкових слів у впорядкованому за \
абеткою словнику -->', search_10000_words())
        print('час пошуку 10000 випадкових слів у словнику, який представлений \
у вигляді бінарного дерева пошуку -->', search_binary_tree())
        print('час пошуку 10000 випадкових слів у словнику, який представлений \
випадково у вигляді бінарного дерева пошуку -->', find_word_mixed_list())
        print('час пошуку 10000 випадкових слів у словнику, який представлений у \
вигляді бінарного дерева пошуку після його балансування -->', search_rebalanced_tree())

if __name__ == '__main__':
    tree = LinkedBST()
    tree.demo_bst('words.txt')


