class NodeDLL(object):
    '''
    Args:
        arg1 previousNode :NodeDLL= Reference to the previous node in the Doubly linked list
        arg2 payload :any: = The object being stored
        arg3 nextNode :NodeDLL: = Reference to the next node in the Doubly linked list
    Methods:
        Str Overloaded
        unpack(), retrieve the nodes payload
    '''

    def __init__(self, payload=None, previousNode=None, nextNode=None):
        self._previous = previousNode
        self._next = nextNode
        self._payload = payload

    def __str__(self):
        return 'Previous:%s Next:%s Payload:%s' % (type(
            self._previous), type(self._next), type(self._payload))

    def unpack(self):
        return self._payload


class DoublyLinkedList(object):
    '''
    Args:
        None
    Methods:
        get_current()
        remove_current()
        add_element()
        next_node()
        previous_node()
        reset()
        length()
        mov_to_pos()
    '''

    def __init__(self):
        self._head = NodeDLL()
        self._tail = NodeDLL()
        self._head._next, self._tail._previous = self._tail, self._head
        self._cursor = self._head
        self._size = 0

    def __repr__(self):
        return 'Length: %d\nCurrent: %s\n' % (self._size,
                                              self._cursor.unpack())

    #defines an iterator
    def __iter__(self):
        self._temp = self._head
        return self

    def __next__(self):
        self._temp = self._temp._next
        if not self._temp is self._tail:
            return self._temp
        else:
            raise StopIteration

    def get_current(self):
        # returns current node element payload. (None if empty or at head or tail)
        '''
        Returns:
            current node payload or none
        '''
        if self._cursor is self._head:
            return None
        return self._cursor.unpack()

    def remove_current(self):
        '''
        Rasies:
            IndexError if DLL self._size is less than zero 
        '''
        if not self._cursor is self._head:  #(not self._cursor is None)
            self._cursor._previous._next = self._cursor._next
            self._cursor._next._previous = self._cursor._previous

            x = self._cursor._previous
            self._cursor._previous, self._cursor._next = None, None
            self._cursor = x

            self._size -= 1
            self.next_node()
            #Unsure if should store ._next reference and delete self._cursor or if will be done by memory

        else:
            raise IndexError('List is empty')

    def add_element(self, item):
        '''
        Args:
            arg1 item :obj: = object to add to list
        '''
        node = NodeDLL(item)
        node._previous = self._tail._previous
        node._next = self._tail
        node._previous._next = node
        self._tail._previous = node

        self._size += 1

        if self._cursor is self._head:
            self.next_node()

    def next_node(self):
        if self._cursor is self._tail._previous:  # If you are at the last item go back to the first
            self.reset()

        else:
            self._cursor = self._cursor._next  # Select next item

    def previous_node(self):
        if not self._cursor is self._head:
            if self._cursor is self._head._next:
                self._cursor = self._tail._previous
            else:
                self._cursor = self._cursor._previous

    def reset(self):  # Sets cursor to the first item
        if self._size > 0:
            self._cursor = self._head._next
        else:
            self._cursor = self._head

    def length(self):
        return self._size

    def move_to_pos(self, index=-1):  # Index[0:n] not Index[1:n]
        # User can place object back into original position
        if not ((type(index) is int) and index < self._size and index >= -1):
            raise IndexError('Invalid Index')

        x = self._cursor.unpack()
        self.remove_current()

        if index > -1 and index < self._size -1:
            tempNode = NodeDLL(x)
            count = 0
            for item in self:
                if count == index:
                    tempNode._next = item
                    tempNode._previous = item._previous
                    item._previous._next = tempNode
                    item._previous = tempNode
                    self._size += 1
                    break
                count += 1

        else:
            self.add_element(x)