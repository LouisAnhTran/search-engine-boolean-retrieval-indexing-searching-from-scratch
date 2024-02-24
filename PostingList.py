import pickle
import math

from Dictionary import Dictionary
from LinkedList import Node
from Block import Block

class PostingsList:
    def __init__(self,posting_file):
        self.posting_file=posting_file
        self.dictionary=dict()

    def save_posting_to_disk(self,consolidated_block: Block,dictionary: Dictionary):
        with open(self.posting_file,'wb') as file:
            for term in consolidated_block.sorted_terms:
                offset=file.tell()
                posting_list=consolidated_block.hashtable.get(term)
                document_frequency=len(posting_list)
                dictionary.insert_term_to_dictionary(term,document_frequency,offset)
                linked_list=PostingsList.convert_posting_list_to_linked_list_and_add_skip_pointers(posting_list)
                pickle.dump(linked_list,file)
        file.close()

    def save_docids_to_disk(self,dictionary: Dictionary,docids):
        with open(self.posting_file,'ab') as file:
           offset=file.tell()
           dictionary.add_docids_to_dictionary(docids,offset)
           pickle.dump(docids,file)
        file.close()

    def load_posting_from_disk(self,offset):
        with open(self.posting_file,'rb') as file:
            file.seek(offset)
            return pickle.load(file)
        
    @classmethod
    def convert_posting_list_to_linked_list_and_add_skip_pointers(self,posting_list):
        '''
        Return a linked list with skip pointers from a posting list

        Parameters:
        - posting_list: List
        '''
        space_to_skip=int(math.sqrt(len(posting_list)))
        head=Node(posting_list[0])
        node=head
        temp_node=node
        for i in range(1,len(posting_list)):
            node.next=Node(posting_list[i])
            node=node.next
            if i%space_to_skip==0:
                temp_node.set_skip_pointer(node)
                temp_node=node
        return head
    
    @classmethod
    def convert_linked_list_to_posting_list(self,head: Node):
        result=[]
        while head:
            result.append(head.docid)
            head=head.next
        return result
    
    @classmethod
    def add_pointers_to_linked_list(self,head: Node):
        '''
            Return a linked list with skip pointers

            Parameters:
            - head: Node
        '''
        converted_posting_list=PostingsList.convert_linked_list_to_posting_list(head)
        # print("converted_posting_list ",converted_posting_list)
        converted_linked_list_with_pointers=PostingsList.convert_posting_list_to_linked_list_and_add_skip_pointers(converted_posting_list)
        return converted_linked_list_with_pointers
    
    @classmethod
    def convert_linked_list_to_string(self,head):
        posting_list=PostingsList.convert_linked_list_to_posting_list(head)
        return ' '.join(list(map(str,posting_list)))