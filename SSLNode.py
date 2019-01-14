class NodeSLL(object):
    '''
    Args:
        arg1 previousNode :NodeDLL= Reference to the previous node in the Doubly linked list
        arg2 payload :any: = The object being stored
        arg3 nextNode :NodeDLL: = Reference to the next node in the Doubly linked list
    Methods:
        Str Overloaded
        unpack(), retrieve the nodes payload
    '''


    def __init__(self, payload=None, nextNode=None):
        self._payload = payload
        self._next = nextNode

    def __str__(self):
        return 'Payload %s\nNext %s\n'%(self.unpack(), self._next.unpack())

    def unpack(self):
        return self._payload
        
class SinglyLinkedList(object):
    '''
    '###### UNFINISHED #########'
    Args:
        None
    Methods:
        get_current()
        remove_current()
        add_element()
        next_node()
        reset()
        length()
        mov_to_pos()
    '''

    def __init__(self):
        self._head = NodeSLL()
        self._tail = self._head
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
        if not self._temp._next is None:
            return self._temp
        else:
            raise StopIteration

    def get_current(self):
        # returns current node element payload. (None if empty or at head or tail)
        '''
        Returns:
            current node payload or none
        '''
        if self._tail is self._head:
            return None
        return self._tail.unpack()

    def remove_last(self):
        '''
        Rasies:
            IndexError if DLL self._size is less than zero 
        '''
        if self._size > 0:
            if self._head._next is self._tail:  #(not self._cursor is None)
                self._head._next = None
                self._tail = self._head
            else:
                for item in self:
                    if item._next is self._tail:
                        item._next = None
                        self._tail = item
                        break

    def remove_first(self):
        if self._size > 0:
            if self._head._next is self._tail:
                self._head._next = None
                self._tail = self._head
            else:
                x = self._head._next
                self._head._next = x._next 
                x._next = None
                x._payload = None

    def add_element(self, item):
        '''
        Args:
            arg1 item :obj: = object to add to list
        '''
        node = NodeSLL(item)
        if self._tail == self._head:
            self._head._next = node
        else:
            self._tail._next = node
        self._tail = node
        self._size += 1

    def length(self):
        return self._size

    # def move_to_pos(self, index=-1):  # Index[0:n] not Index[1:n]
        # # User can place object back into original position
        # if not ((type(index) is int) and index < self._size and index >= -1):
        #     raise IndexError('Invalid Index')

        # x = self._cursor.unpack()
        # self.remove_current()

        # if index > -1 and index < self._size -1:
        #     tempNode = NodeDLL(x)
        #     count = 0
        #     for item in self:
        #         if count == index:
        #             tempNode._next = item
        #             tempNode._previous = item._previous
        #             item._previous._next = tempNode
        #             item._previous = tempNode
        #             self._size += 1
        #             break
        #         count += 1

        # else:
        #     self.add_element(x)
