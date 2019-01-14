from sys import getsizeof
from math import ceil

'''
Queue Implementation using an array
'''
class Queue():
    def __init__(self):
        self._body = [None] * 10
        self._head = 0  #index of first element, unless empty, and then 0 by default
        self._tail = 0  #index of free cell for next element
        self._size = 0  #number of elements in the queue

    def __str__(self):
        output = '<-'
        i = self._head
        if self._head < self._tail:
            while i < self._tail:
                output = output + str(self._body[i]) + '-'
                i = i + 1
        else:
            while i < len(self._body):
                output = output + str(self._body[i]) + '-'
                i = i + 1
            i = 0
            while i < self._tail:
                output = output + str(self._body[i]) + '-'
                i = i + 1
        output = output + '<'
        output = output + '     ' + self.status()
        return output

    def get_size(self):
        return getsizeof(self._body)

    def status(self):
        return ('Head:' + str(self._head) + '; tail:' + str(self._tail) +
                '; size:' + str(self._size))

    def grow(self):
        old_body = self._body
        self._body = [None] * (2 * self._size)
        for i in range(self._size):
            pos = (self._head + i) % self._size  # Using modulo operator
            self._body[i] = (old_body[pos])
        self._head = 0
        self._tail = self._size

    def reclaim(self):
        old_body = self._body
        self._body = [None] * ceil(0.5 * self._size)
        for i in range(self._size):
            pos = (self._head + i) % self._size  # Using modulo operator
            self._body[i] = (old_body[pos])
        self._head = 0
        self._tail = self._size


    def enqueue(self, item):
        if self._size == 0:
            self._body[0] = item  #assumes an empty queue has head at 0
            self._size = 1
            self._tail = 1
        else:
            self._body[self._tail] = item
            self._size = self._size + 1
            if self._size == len(self._body):  #list is now full
                self.grow()  #so grow it ready for next enqueue
            elif self._tail == len(
                    self._body) - 1:  #no room at end, but must be at front
                self._tail = 0
            else:
                self._tail = self._tail + 1

    def dequeue(self):
        if self._size == 0:  #empty queue
            return None
        item = self._body[self._head]
        self._body[self._head] = None
        if self._size == 1:  #just removed last element, so rebalance
            self._head = 0
            self._tail = 0
            self._size = 0
        elif (self.get_size() / self.length()) < 0.3:
            self.reclaim()
        elif self._head == len(
                self._body) - 1:  #if the head was the end of the list
            self._head = 0  #we must have wrapped round, so point to start
            self._size = self._size - 1
        else:
            self._head = self._head + 1  #just move the pointer on one cell
            self._size = self._size - 1
        #we haven't changed the tail, so nothing to do
        return item

    def length(self):
        return self._size

    def first(self):
        return self._body[self._head]  # will return None if queue is empty

    def is_empty(self):
        return self._size == 0
