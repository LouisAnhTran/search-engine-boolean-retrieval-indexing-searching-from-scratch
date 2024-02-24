import pickle

import config

class Block:
    '''
    This class defined to manage block
    '''

    def __init__(self,sorted_term,hashtable):
        self.hashtable=hashtable
        self.sorted_terms=sorted_term

    def sort_and_write_out_block_to_disk(self):
        block={"sorted_terms":self.sorted_terms,"hash_table":self.hashtable}
        print("sorted_term ",self.sorted_terms)
        print('hash table ',self.hashtable)
        offset=0
        with open(config.TEMP_FILE_FOR_BLOCK, 'ab') as file:
            offset=file.tell()
            pickle.dump(block,file)
        return offset
    
    def merge(self,block):
        '''
            Merge two blocks

            Parameters:
            - block: Block

            Return: return offset of merged block
        '''
        new_sorted_terms=sorted(list(set(self.sorted_terms).union(set(block.sorted_terms))))
        new_hashtable={term:sorted(list(set(self.hashtable.get(term,[])).union(set(block.hashtable.get(term,[]))))) for term in new_sorted_terms}
        merge_block=Block(new_sorted_terms,new_hashtable)
        return merge_block.sort_and_write_out_block_to_disk()
    

    def __str__(self) -> str:
        return f'sorted_terms: {self.sorted_terms} \n hashtable: {self.hashtable}'
    
    @classmethod
    def read_block_from_disk(self,offset):
        '''
            Read block from hard-disk to memory given the offset

            Parameters:
            - offset: integer

            Return:
            - Block object
        '''
        with open(config.TEMP_FILE_FOR_BLOCK, 'rb') as file:
            file.seek(offset)
            loaded_block=pickle.load(file)
        return Block(loaded_block['sorted_terms'],loaded_block['hash_table'])


        
