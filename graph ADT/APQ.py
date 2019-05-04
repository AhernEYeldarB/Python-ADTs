class Node:
    '''
    Node object in an Adaptable Priority Queue

    Attributes:
        Key = Quantative data type, used to determine position  in list( Works with numerical data types ) 
        Value = The value the node is storing in the list
        Index = the position of the item in the array
    '''

    def __init__(self, key, value, i):
        self._key = key  # Key = Weight
        self._value = value  # Value = Vertex/Object
        self._index = i

    def __str__(self):
        return (
            '{Key=%s' % str(self._key) + ' ' + 'Value=%s' % str(self._value) +
            ' ' + 'Index=%s' % str(self._index) + '}')
        # str(self._key) + '\t' + str(self._value) + '\t' + str(self._index))

    def __repr__(self):
        return (
            '[Key=%s' % str(self._key) + ' ' + 'Value=%s' % str(self._value) +
            ' ' + 'Index=%s' % str(self._index) + ']')
        # return (
        #     'Key=%s'%str(self._key) + '\t' + 'Value=%s:'%str(self._value) + '\t' + 'Index=%s'%str(self._index))

    def __eq__(self, temp):
        return self._key == temp._key

    def __lt__(self, temp):
        return self._key < temp._key

    def __gt__(self, temp):
        return self._key > temp._key

    def _clear(self):
        self._key = None
        self._value = None
        self._index = None

    def getKey(self):
        return self._key

    def left(self):
        # Return index of left Child
        return 2 * self._index + 1

    def right(self):
        # Return index of Right Child
        return 2 * self._index + 2

    def parent(self):
        # Return index of Parent
        return (self._index // 2)


class APQ(object):
    '''
    Adaptable Priority Queue implemented as an array based Min-Heap

    Attributes:
        None

    Methods:
        add(self, key, value) = Add a Node to the APQ

        getKey(self, element) = Return the key of a node object

        isEmpty(self) = Return True if length is zero, false otherwise

        length(self) = Return (int) length of list

        min(self) = Return a reference to the min object (Top of heap)

        remove(self) = Remove an object from the APQ and return it

        removeMin(self) = Remove the Top object from the APQ and return it

        updateKey(self, element, newKey) = Change the key of a node and rebalace accordingly 

    '''
    def __init__(self):
        self._body = []
        self._length = 0

    def __str__(self):
        outstring = 'APQ->{'
        for item in self._body:
            outstring += item.__str__()
            outstring += '\t'

        outstring += '}'
        return outstring

    def add(self, key, value):
        # Create a Node object and add it to the queue
        newNode = Node(key, value, self.length())
        self._body.append(newNode)
        self._length += 1

        self._bubbleUp(newNode)

        return newNode

    def _bubbleUp(self, node):
        # Maintain the Heap Structure, If parent is smaller swap positions
        while self._body[node.parent()] > node:
            # Get parent
            parent = node.parent()

            # Swap list Positions
            self._swap(node._index, parent)

    def min(self):
        # Min object is index 0 
        return self._body[0]

    def removeMin(self):
        # Swap first and last elements, pop the last element and bubble down the new position 0 to maintain Heap
        return self.remove(0)

    def isEmpty(self):
        return self._length == 0

    def length(self):
        return self._length

    def updateKey(self, element, newKey):
        element._key = newKey
        # Check parent first
        self._bubbleUp(element)
        # Loop through to check each child until both are less than or list index error
        self._bubbleDown(element)

    def _bubbleDown(self, element):
        if self.length == 0:
            return

        leftChild = element.left()
        rightChild = element.right()
        current = element._index
        # swap = min(leftChild, rightChild); if swap < current
        while rightChild < self.length():
            if self._body[leftChild]._key < self._body[
                    rightChild]._key < element._key:
                self._swap(leftChild, current)

            elif self._body[rightChild]._key < element._key:
                self._swap(rightChild, current)

            else:
                return

            leftChild = element.left()
            rightChild = element.right()
            current = element._index

    def _swap(self, indexA, indexB):
        # Pass in two node indeces to swap
        elementA = self._body[indexA]
        elementB = self._body[indexB]

        self._body[indexA], self._body[indexB] = self._body[
            indexB], self._body[indexA]

        #swap index
        elementA._index, elementB._index = elementB._index, elementA._index

    def getKey(self, element):
        return element.key()
        # return self._body[element.i]._key

    def remove(self, index):
        self._swap(self._body[index]._index, self._body[-1]._index)

        outNode = self._body.pop()
        self._length -= 1
        if self.length() == 0:
            return outNode
        self._bubbleDown(self._body[index])

        return outNode


if __name__ == "__main__":
    apq = APQ()
    apq.add(10, 'John')
    apq.add(11, 'Alex')
    apq.add(7, 'Brian')
    apq.add(6, 'James')
    print(apq)
    apq.updateKey(apq._body[0], 15)
    print(apq)
    apq.removeMin()
    print(apq)
    print('\n\n\n')
    # apq.inorder()