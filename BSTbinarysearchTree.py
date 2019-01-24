import re

class NodeBST(object):
    '''
    Args:
        arg1 left :NodeBST: = left most object smaller than 
        arg2 right :NodeBST: = right hand side object greater than
        arg3 parent :NodeBST = parent is the node under which it is created
        arg4 payload :any: = The object being represented
    Methods:
        Add() - Add an item to the node
        _delete() - Set all attributes of the node to None
    '''

    def __init__(self, payload, parent):
        self._left = None
        self._right = None
        self._parent = parent
        self._payload = payload

    def __str__(self):
        return '%s' % (self._payload)

    def delete(self):
        self._left = None
        self._right = None
        self._parent = None
        self._payload = None

    def add(self, item):
        if self._payload < item:
            if not self._right:
                self._right = NodeBST(item, self)
                return True
            else:
                self._right.add(item)

        elif self._payload > item:
            if not self._left:
                self._left = NodeBST(item, self)
                return True
            else:
                self._left.add(item)

    def num_children(self):
        num = 0

        if self.left():
            num += 1

        if self.right():
            num += 1

        return num

    def has_right(self):
        return self._right != None

    def has_left(self):
        return self._left != None

    # def _balance(self):
    #     return self.left()._height() - self.right()._height()

    def _height(self):
        leftheight = -1
        rightheight = -1
        if self.has_left():
            leftheight = self.left()._height()
        if self.has_right():
            rightheight = self.right()._height()

        return (1 + max(leftheight, rightheight))

    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """
        if self._isthisapropertree() == False:
            print("ERROR: this is not a proper tree. +++++++++++++++++++++++")
        outstr = str(self._payload) + '(' + str(self._height()) + ')['
        if self._left:
            outstr = outstr + str(self._left._payload) + ' '
        else:
            outstr = outstr + '* '
        if self._right:
            outstr = outstr + str(self._right._payload) + ']'
        else:
            outstr = outstr + '*]'
        if self._parent:
            outstr = outstr + ' -- ' + str(self._parent._payload)
        else:
            outstr = outstr + ' -- *'
        print(outstr)
        if self._left:
            self._left._print_structure()
        if self._right:
            self._right._print_structure()

    def _isthisapropertree(self):
        """ Return True if this tree is a properly implemented tree. """
        ok = True
        if self._left:
            if self._left._parent != self:
                print('leftfalse')
                ok = False
            if self._left._isthisapropertree() == False:
                print('leftfalse')
                ok = False
        if self._right:
            if self._right._parent != self:
                print('rightfalse')
                ok = False
            if self._right._isthisapropertree() == False:
                print('rightfalse')
                ok = False
        if self._parent:
            if (self._parent._left != self and self._parent._right != self):
                print('parentfalse')
                ok = False
        return ok

    def get_payload(self):
        return self._payload

    def left(self):
        return self._left

    def right(self):
        return self._right

    def __iter__(self):
        def generator():
            if self._left:
                for child in self._left:
                    yield child

            yield self

            if self._right:
                for child in self._right:
                    yield child

        return generator()

    def __eq__(self, node):
        if not node:
            return False
        else:
            return (type(self) is NodeBST and self._payload is node._payload)

    def __gt__(self, node):
        if not node:
            return False
        else:
            return (type(self) is NodeBST and self._payload > node._payload)

    def __lt__(self, node):
        if not node:
            return False
        else:
            return (type(self) is NodeBST and self._payload < node._payload)


class BinarySearchTreeBST(object):
    def __init__(self):
        self._root = None
        self._size = 0

    def __str__(self):
        x = ''
        for item in self:
            x += str(item) + ' '

        return x

    def __iter__(self):
        return self.root().__iter__()

    def inorder(self, node):
        # Returns a list of all elements in order
        if node:
            x = []
            for item in node:
                x.append(item)
            return x

    def add(self, item):
        if item != None:
            if self._root != None:
                if self._root.add(item):
                    self._size += 1
            else:
                self._root = NodeBST(item, None)
                self._size += 1

    def _set_parent(self, pos, pos2=None):
        parent = self.parent(pos)

        if pos2 != None:
            pos2._parent = parent

        else:
            if pos.left() == pos2:
                pos._left = None
            else:
                pos._right = None

        if parent == None:
            self._root = pos2

        else:
            if parent > pos:
                parent._left = pos2

            else:
                parent._right = pos2

        pos.delete()

    def remove(self, item):
        # Rebuilds tree if removes root
        node = self.search(item)
        if node != None:
            output = node.get_payload()
            # Leaf node
            if not (node.has_left()) and not (node.has_right()):
                self._set_parent(node)

            # Semi Leaf
            elif (not node.has_left()) and node.has_right():
                self._set_parent(node, node.right())

            elif node.has_left() and (not node.has_right()):
                self._set_parent(node, node.left())

            # Internal node
            else:
                temp = node.left()
                while temp.has_right():  #._has_right():
                    temp = temp.right()

                hold = temp.get_payload()
                self.remove(temp.get_payload())
                node._payload = hold

            self._size -= 1
            return output

    # def rotate(self, pos1, pos2):
    # unfinished
    #     if pos2.get_payload() > pos1.get_payload():
    #         pos1, pos2 = pos2, pos1

    #     if pos1 != pos2:
    #         pos1._node._right = self.left(pos2)
    #         self.left(pos2)._node._parent = pos1._node
    #         pos2._node._left = pos1._node
    #         if self.parent(pos1) != None:
    #             pos2._node._parent = self.parent(pos1)._node
    #             self._set_parent(pos1, pos2._node)
    #                                 # if pos1 == self.left(self.parent(pos1)):
    #                                 #     pos1._node._parent._left = pos2._node
    #                                 # else:
    #                                 #     pos1._node._parent._right = pos2._node
    #         else:
    #             pos2._node._parent = None

    # pos1._node._parent = pos2._node

    def search(self, item, node=None):
        if item != None:
            if not self.root():
                return None
            if node == None:
                return self._search(item, self.root())
            else:
                return self._search(item, node)
        else:
            return None
            #raise TyperError

    def _search(self, item, node):
        if node is None:
            return None
        if node.get_payload() > item:
            return self._search(item, node.left())  # left

        elif node.get_payload() < item:
            return self._search(item, node.right())  # left
        else:
            return node

    def _stats(self):
        """ Return the basic stats on the node. """
        return ('size = ' + str(self._size) + '; height = ' + str(
            self.height(self._root)))

    def depth(self, node):
        if node:
            return self.height(node)
        return None

    def height(self, node):
        if node:
            return node._height()

        # leftheight = -1
        # rightheight = -1
        # if node._has_left():
        #     leftheight = self.height(node.left())
        # if node._has_right():
        #     rightheight = self.height(node.right())

        # return (1 + max(leftheight, rightheight))

    def root(self):
        return self._root

    def parent(self, node):
        if node != self.root():
            return node._parent
        return None

    def leaf(self, node):
        """ Return True if this node has no children. """
        return node.num_children() == 0

    def semileaf(self, node):
        """ Return True if this node has exactly one child. """
        return node.num_children() == 1

    def full(self, node):
        """ Return true if this node has two children. """
        return node.num_children() == 2

    def internal(self, node):
        """ Return True if this node has at least one child. """
        return not self.leaf(node)

    def isthisapropertree(self):
        return self.root()._isthisapropertree()

    def print_structure(self):
        return self.root()._print_structure()

    def size(self):
        return self._size


def test():
    tree = BinarySearchTreeBST()
    tree.add(3)
    for i in range(5, 0, -1):
        print('adding ' + '%i' % (i))
        tree.add(i)
    print('depth = ' + str(tree.depth(tree.root())))
    print(tree._stats())
    # print(tree.search(2))
    # print(tree)
    # print(tree._root)
    # print(tree._root._left)
    # print(tree._root._right)
    # print(tree._root._left._right)
    # print(tree._root._left._right._right)
    print()
    print(tree)
    tree.print_structure()
    print()
    tree.remove(3)
    print()
    tree.print_structure()
    print(tree.root())
    print(tree)


def _testadd():
    tree = BinarySearchTreeBST()
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
    tree = BinarySearchTreeBST()
    tree.add(1)
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


def wordbst(filename):
    file = open(filename, 'r')  # open the file
    fulltext = file.read()  # read it all into one big string
    stripped = re.sub('[^a-zA-Z\s]+', '',
                      fulltext)  # remove non-letters or -spaces
    wordlist = stripped.split(
    )  # split the string on white space into words in a list
    print(len(wordlist), 'words in total')
    bst = BinarySearchTreeBST()
    for word in wordlist:
        bst.add(word)
    return bst


def test_books():
    filenames = [
        'testfile.txt', 'drMoreau.txt', 'frankenstein.txt', 'dracula.txt'
    ]
    words = ['blood', 'screaming', 'science']
    for name in filenames:
        print('Reading file', name)
        tree = wordbst(name)
        print('bst has stats', tree._stats())
        for word in words:
            node = tree.search(word)
            if node:
                # print(word, ': (', node._stats(), ')')
                print(node)
            else:
                print(word, 'is not in', name)
        print('\n\n')


if __name__ == '__main__':
    # test()
    # print('\n\n\n\n\n\n')
    # _test()
    # print('\n\n\n\n\n\n')
    # _testadd()
    test_books()