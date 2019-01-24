import re
import math


class NodeAVL():
    def __init__(self, payload, parent=None):
        '''
            Arguments:
             Parent ;NodeAVL;
             Left Child ;NodeAVL;
             Right Child ;NodeAVL;
             Payload ;NodeAVL;
        '''
        self._parent = parent
        self._leftChild = None
        self._rightChild = None
        self._payload = payload
        self._height = 0

    def __str__(self):
        return '%s(%i)' % (self._payload, self._height)

    def __repr__(self):
        return '%s(%i)' % (self._payload, self._height)

    def __iter__(self):
        def generator():
            if self._leftChild:
                for child in self._leftChild:
                    yield child

            yield self

            if self._rightChild:
                for child in self._rightChild:
                    yield child

        return generator()

    # Parent properties
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, temp):
        self._parent = temp

    # leftChild properties
    @property
    def leftChild(self):
        return self._leftChild

    @leftChild.setter
    def leftChild(self, temp):
        self._leftChild = temp

    # rightChild properties
    @property
    def rightChild(self):
        return self._rightChild

    @rightChild.setter
    def rightChild(self, temp):
        self._rightChild = temp

    # payload properties
    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, temp):
        self._payload = temp

    # def __eq__(self, node):
    #     if not node:
    #         return False
    #     else:
    #         return (type(self) is NodeAVL and self._payload is node._payload)

    # def __gt__(self, node):
    #     if not node:
    #         return False
    #     else:
    #         return (type(self) is NodeAVL and self._payload > node._payload)

    # def __lt__(self, node):
    #     if not node:
    #         return False
    #     else:
    #         return (type(self) is NodeAVL and self._payload < node._payload)

    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """
        if self._isthisapropertree() == False:
            print("ERROR: this is not a proper tree. +++++++++++++++++++++++")
        outstr = str(self._payload) + '(' + str(self._height) + ')['
        if self._leftChild:
            outstr = outstr + str(self._leftChild._payload) + ' '
        else:
            outstr = outstr + '* '
        if self._rightChild:
            outstr = outstr + str(self._rightChild._payload) + ']'
        else:
            outstr = outstr + '*]'
        if self._parent:
            outstr = outstr + ' -- ' + str(self._parent._payload)
        else:
            outstr = outstr + ' -- *'
        print(outstr)
        if self._leftChild:
            self._leftChild._print_structure()
        if self._rightChild:
            self._rightChild._print_structure()

    def _isthisapropertree(self):
        """ Return True if this tree is a properly implemented tree. """
        ok = True
        if self._leftChild:
            if self._leftChild._parent != self:
                print('leftChildfalse')
                ok = False
            if self._leftChild._isthisapropertree() == False:
                print('leftChildfalse')
                ok = False
        if self._rightChild:
            if self._rightChild._parent != self:
                print('rightChildfalse')
                ok = False
            if self._rightChild._isthisapropertree() == False:
                print('rightChildfalse')
                ok = False
        if self._parent:
            if (self._parent._leftChild != self
                    and self._parent._rightChild != self):
                print('parentfalse')
                ok = False
        return ok


class TreeAVL(object):
    def __init__(self):
        self._root = None
        self._size = 0

    def __str__(self):
        x = ''
        for item in self:
            x += str(item) + ' '
        return x

    def __iter__(self):
        return self._root.__iter__()

    def inorder(self, node):
        # Returns a list of all elements in order
        if node:
            x = []
            for item in node:
                x.append(item)
                # yield item
            return x

    def add(self, payload, root=None):
        # Insert new node into the tree
        node = NodeAVL(payload)

        # If the tree is empty then assign new node to root

        if payload is not None:
            node.payload = payload

        if self._root is None:
            self._root = node
            self._size += 1
            return

        if root == None:
            root = self._root

        search_queue = [root]
        index = 0
        while search_queue:
            if payload < search_queue[index].payload:
                if search_queue[index]._leftChild:
                    search_queue.append(search_queue[index]._leftChild)
                    index += 1
                else:
                    search_queue[index]._leftChild = node
                    node._parent = search_queue[index]
                    self.recalculateAscendantHeight(search_queue)
                    self._size += 1
                    break

            elif payload > search_queue[index].payload:
                if search_queue[index]._rightChild:
                    search_queue.append(search_queue[index]._rightChild)
                    index += 1
                else:
                    search_queue[index]._rightChild = node
                    node._parent = search_queue[index]
                    self.recalculateAscendantHeight(search_queue)
                    self._size += 1
                    break

            if search_queue[index]._payload == payload:
                break

    def recalculateAscendantHeight(self, search_queue):
        for n in reversed(search_queue):

            n._height = max(
                self.height(n._leftChild), self.height(n._rightChild)) + 1

            balance = self.getBalance(n)
            if balance > 1 or balance < -1:
                self.balance(n, balance)

    def search(self, value):
        # Wrapper method of _search
        if self._root:
            node = self._search(value, self._root)
            if node:
                return node

        return None

    def _search(self, value, node):
        # Private method called by search() to find a specific node in a tree or NONE
        if not node:
            return None
        else:
            if node._payload == value:
                return node
            elif value < node.payload:
                return self._search(value, node.leftChild)

            return self._search(value, node._rightChild)

    def __getitem__(self, value):
        return self.search(value)

    def height(self, node):
        if node is None:
            return -1
        return node._height

    def remove(self, value, start=None):
        if self._root is None:
            return

        # Find node to remove and place it in start
        if start is None:
            start = self._root

        if value < start._payload:
            self.remove(value, start._leftChild)

        elif value > start._payload:
            self.remove(value, start._rightChild)

        else:
            # Leaf Node
            if (start._leftChild is None and start._rightChild is None):
                if start._parent._leftChild == start:
                    start._parent._leftChild = None
                else:
                    start._parent._rightChild = None

            # Internal Node
            elif (start._leftChild != None and start._rightChild != None):
                temp = start._leftChild
                while temp._rightChild != None:
                    temp = temp._rightChild
                start._payload = temp._payload
                if temp._parent._leftChild == temp:
                    temp._parent._leftChild = None
                else:
                    temp._parent._rightChild = None
                start = temp._parent

            # Semi-Leaf Node
            else:
                if start._leftChild is None:
                    subtree = start._rightChild
                else:
                    subtree = start._leftChild

                if start._parent != None:
                    if start._parent._leftChild == start:
                        start._parent._leftChild = subtree
                    else:
                        start._parent._rightChild = subtree
                    subtree._parent = start._parent
                else:
                    subtree._parent = start._parent

                if start == self._root:
                    self._root = subtree
                    start = self._root

            # Recalculates Heights after removal is done
            start._height = max(
                self.height(start._leftChild), self.height(
                    start._rightChild)) + 1

            newTemp = start
            while newTemp._parent != None:
                newTemp = newTemp._parent
                newTemp._height = max(
                    self.height(newTemp._leftChild),
                    self.height(newTemp._rightChild)) + 1

            balance = self.getBalance(start)
            self.balance(start, balance)
            self._size -= 1

    def rotateRight(self, node):
        left = node._leftChild
        node._leftChild = left._rightChild
        if left._rightChild != None:
            left._rightChild._parent = node

        left._parent = node._parent

        if node._parent != None:
            if node._parent._leftChild == node:
                node._parent._leftChild = left
            else:
                node._parent._rightChild = left

        left._rightChild = node
        node._parent = left

        left._rightChild._height = max(
            self.height(node._leftChild), self.height(node._rightChild)) + 1
        node._parent._height = max(
            self.height(left._leftChild), self.height(left._rightChild)) + 1

        if node == self._root:
            self._root = left

    def rotateLeft(self, node):
        right = node._rightChild
        node._rightChild = right._leftChild
        if right._leftChild != None:
            right._leftChild._parent = node

        right._parent = node._parent

        if node._parent != None:
            if node.parent._leftChild == node:
                node.parent._leftChild = right
            else:
                node.parent._rightChild = right

        right._leftChild = node
        node._parent = right

        right._leftChild._height = max(
            self.height(node._leftChild), self.height(node._rightChild)) + 1
        node._parent._height = max(
            self.height(right._leftChild), self.height(right._rightChild)) + 1

        if node == self._root:
            self._root = right

    def balance(self, node, balance):
        # determines which balances should be done if any
        '''
            1. Left subtree = -1 or Right subtree = +1
            2. Height of left child of given subtree
        '''
        if balance < -1:
            if node._rightChild != None:
                if self.highestChild(node._rightChild):
                    self.rotateRight(node._rightChild)
                    self.rotateLeft(node)
                else:
                    self.rotateLeft(node)

        elif balance > 1:
            if node._leftChild != None:
                if self.highestChild(node._leftChild):
                    self.rotateRight(node)
                else:
                    self.rotateLeft(node._leftChild)
                    self.rotateRight(node)

    # Determine the highest child of a node, Return True if left, False if Right
    def highestChild(self, node):
        if node != None:
            if (node._leftChild._height if node._leftChild else -1) > (
                    node._rightChild._height if node._rightChild else -1):
                return True
            return False

    def getBalance(self, node):
        if node == None:
            return 0

        return (node._leftChild._height if node._leftChild else
                -1) - (node._rightChild._height if node._rightChild else -1)

    def isthisapropertree(self):
        return self._root._isthisapropertree()

    def print_structure(self):
        return self._root._print_structure()

    def _stats(self):
        """ Return the basic stats on the node. """
        return ('size = ' + str(self._size) + '; height = ' + str(
            self.height(self._root)))


# Test Block for AVL Tree
if __name__ == '__main__':

    def _testadd():
        tree = TreeAVL()
        print('> adding mushroom')
        tree.add('mushroom')
        tree.print_structure()
        print('> adding greenbean')
        tree.add('greenbean')
        tree.print_structure()
        print('> adding radish')
        tree.add('radish')
        tree.print_structure()
        print('> adding pea')
        tree.add('pea')
        tree.print_structure()
        print('> adding pepper')
        tree.add('pepper')
        tree.print_structure()
        print('> adding parsnip')
        tree.add('parsnip')
        tree.print_structure()
        return tree

    def _test():
        tree = TreeAVL()
        print('adding', 3)
        tree.add(3)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 4)
        tree.add(4)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 5)
        tree.add(5)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 3)
        tree.remove(3)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 4)
        tree.remove(4)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 1)
        tree.add(1)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 5)
        tree.remove(5)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 0)
        tree.add(0)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 0)
        tree.remove(0)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 2)
        tree.add(2)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 2)
        tree.remove(2)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 6)
        tree.add(6)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 1)
        tree.remove(1)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 2)
        tree.add(2)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 4)
        tree.add(4)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 3)
        tree.add(3)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 5)
        tree.add(5)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 2)
        tree.remove(2)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 4)
        tree.remove(4)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 3)
        tree.remove(3)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 5)
        tree.remove(5)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 12)
        tree.add(12)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 8)
        tree.add(8)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 9)
        tree.add(9)
        print('Ordered:', tree)
        tree.print_structure()
        print('adding', 7)
        tree.add(7)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 12)
        tree.remove(12)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 8)
        tree.remove(8)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 9)
        tree.remove(9)
        print('Ordered:', tree)
        tree.print_structure()
        print('removing', 7)
        tree.remove(7)
        print('Ordered:', tree)
        tree.print_structure()
        print(tree)

    # def wordbst(filename):
    #     file = open(filename, 'r')  # open the file
    #     fulltext = file.read()  # read it all into one big string
    #     stripped = re.sub('[^a-zA-Z\s]+', '',
    #                       fulltext)  # remove non-letters or -spaces
    #     wordlist = stripped.split(
    #     )  # split the string on white space into words in a list
    #     print(len(wordlist), 'words in total')
    #     bst = TreeAVL()
    #     for word in wordlist:
    #         bst.add(word)
    #     return bst

    # def test_books():
    #     filenames = [
    #         'testfile.txt', 'drMoreau.txt', 'frankenstein.txt', 'dracula.txt'
    #     ]
    #     words = ['blood', 'screaming', 'science']
    #     for name in filenames:
    #         print('Reading file', name)
    #         tree = wordbst(name)
    #         print('bst has stats', tree._stats())
    #         for word in words:
    #             node = tree.search(word)
    #             if node:
    #                 # print(word, ': (', node._stats(), ')')
    #                 print(node)
    #             else:
    #                 print(word, 'is not in', name)
    #         print('\n\n')

    # _testadd()
    # print('\n\n\n\n\n\n')
    # _test()
    # print('\n\n\n\n\n\n')
    test_books()
