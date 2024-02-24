

class Node:
    def __init__(self,docid,skip_pointer=None):
        self.docid=docid
        self.skip_pointer=skip_pointer
        self.next=None

    def set_skip_pointer(self,next_pointer_node):
        '''
            Set skip pointer for a node

            Parameters:
            - next_pointer_node: Node
        '''
        self.skip_pointer=next_pointer_node

    def has_skip_pointer(self):
        return True if self.skip_pointer else False