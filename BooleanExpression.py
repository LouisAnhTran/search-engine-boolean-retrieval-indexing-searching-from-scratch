import re
from nltk.stem.porter import *

from Stack import Stack
import utils
from LinkedList import Node
from PostingList import PostingsList
from Dictionary import Dictionary

class Boolean:
    PRECEDENCE_ORDER={"NOT":2,"AND":1,"OR":3}
    NON_OPERANDS={"NOT","AND","OR","(",")"}

    def __init__(self,expression):
        self.expression=expression

    def tokenize_expr(self):
        '''
            Tokenizing the boolean query with stemming,case-folding,parathesis handling
        '''
        # pre-processing for queries with parenthesis for tokenization
        list_of_all_indexes=utils.get_list_of_indexes_parenthesis(self.expression)
        new_expression=""
        for i in range(len(self.expression)):
            if i not in list_of_all_indexes:
                new_expression+=self.expression[i]
            else:
                new_expression+=" "+self.expression[i]+" "
        self.expression=new_expression.split()
        # Stemming 
        stemmer=PorterStemmer()
        self.expression=[stemmer.stem(token).lower() if token not in Boolean.NON_OPERANDS else token for token in self.expression]

    def run_shunting_yard_algorithm_postfix(self):
        self.tokenize_expr()
        operator_stack=Stack()
        output_queue=Stack()

        for token in self.expression:
            if token not in self.NON_OPERANDS:
                output_queue.push(token)
            elif token == 'NOT':
                operator_stack.push(token)
            elif token in self.PRECEDENCE_ORDER.keys():
                while operator_stack.peek() and operator_stack.peek() in self.PRECEDENCE_ORDER and self.PRECEDENCE_ORDER[operator_stack.peek()]>=self.PRECEDENCE_ORDER[token]:
                    output_queue.push(operator_stack.pop())
                operator_stack.push(token)
            elif token == '(':
                operator_stack.push(token)
            elif token == ')':    
                while operator_stack.peek() != "(":
                    output_queue.push(operator_stack.pop())
                operator_stack.pop()
        
        while not operator_stack.is_empty:
            output_queue.push(operator_stack.pop())

        self.expression=output_queue.output_list()

    def implement_boolean_retrieval(self,dictionary:Dictionary,postingList: PostingsList):
        self.run_shunting_yard_algorithm_postfix()
        stack=Stack()
        while self.expression:
            pop_item=self.expression.pop(0)
            if pop_item not in Boolean.NON_OPERANDS:
                term=dictionary.return_offset_based_on_term(pop_item)
                if not term:
                    stack.push(None)
                    continue
                stack.push(postingList.load_posting_from_disk(term))
            else:
                if pop_item == 'AND':
                    first_posting_linked_list=stack.pop()
                    second_posting_linked_list=stack.pop()
                    stack.push(self.AND_operator(first_posting_linked_list,second_posting_linked_list))
                elif pop_item == 'OR':
                    first_posting_linked_list=stack.pop()
                    second_posting_linked_list=stack.pop()
                    stack.push(self.OR_operator(first_posting_linked_list,second_posting_linked_list))
                elif pop_item=='NOT':
                    posting_linked_list=stack.pop()
                    offset_for_docids=dictionary.return_offset_for_all_docids()
                    all_doc_ids=postingList.load_posting_from_disk(offset_for_docids)
                    stack.push(self.NOT_operator(posting_linked_list,all_doc_ids))
        
        result=stack.pop() # the only element left in the stack is the result for the query
        return PostingsList.convert_linked_list_to_string(result)
    
    @classmethod
    def implement_skip_pointer_techniques(self,first_head:Node,second_head:Node):
        result_head=Node(1) #
        run_head=result_head 
        while first_head and second_head:
            if first_head.docid==second_head.docid:
                run_head.next=Node(first_head.docid)
                run_head=run_head.next
                first_head=first_head.next
                second_head=second_head.next
            elif first_head.docid<second_head.docid:
                if first_head.has_skip_pointer() and first_head.skip_pointer.docid<=second_head.docid:
                    first_head=first_head.skip_pointer
                else:
                    first_head=first_head.next
            else:
                if second_head.has_skip_pointer() and second_head.skip_pointer.docid<=first_head.docid:
                    second_head=second_head.skip_pointer
                else:
                    second_head=second_head.next 
        return result_head.next if result_head.next else None
    
    def AND_operator(self,first_head:Node,second_head:Node):
        if not first_head or not second_head:
            return None
        result=Boolean.implement_skip_pointer_techniques(first_head,second_head)
        return None if not result else PostingsList.add_pointers_to_linked_list(result)
    
    def OR_operator(self,first_head:Node,second_head:Node):
      
        if not second_head and not first_head:
            return None
        elif not second_head:
            return first_head
        elif not first_head:
            return second_head
        
        result_head=Node(1) #
        run_head=result_head
        while first_head and second_head:
            if first_head.docid<second_head.docid:
                run_head.next=Node(first_head.docid)
                first_head=first_head.next
                run_head=run_head.next
            elif first_head.docid==second_head.docid:
                run_head.next=Node(first_head.docid)
                first_head=first_head.next
                second_head=second_head.next
                run_head=run_head.next
            else:
                run_head.next=Node(second_head.docid)
                second_head=second_head.next
                run_head=run_head.next
        if first_head:
            run_head.next=first_head
        if second_head:
            run_head.next=second_head
        
        return PostingsList.add_pointers_to_linked_list( result_head.next)
    

    def NOT_operator(self,head: Node,all_docs_id: list):
        if not head:
            return PostingsList.convert_posting_list_to_linked_list_and_add_skip_pointers(all_docs_id)
        converted_posting_list=PostingsList.convert_linked_list_to_posting_list(head)
        result=[docid for docid in all_docs_id if docid not in converted_posting_list]
        return PostingsList.convert_posting_list_to_linked_list_and_add_skip_pointers(result)

        

    