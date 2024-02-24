class Stack:
    def __init__(self):
        self.__items = []
        
    def push(self, item):
        self.__items.append(item)
        pass

    def pop(self):
        if self.is_empty:
            return None
        return self.__items.pop(self.size-1)

    def peek(self):
        if self.is_empty:
            return None
        return self.__items[self.size-1]
    
    def output_list(self):
        return [item for item in self.__items]

    @property
    def is_empty(self):
        return self.size==0

    @property
    def size(self):
        return len(self.__items)