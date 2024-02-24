from Block import Block

class SPIMI:
    def __init__(self):
        self.block_list=list()  # [location_block1,location_block2,....,location_block2]


    def add_block(self,block: Block):
        self.block_list.append(block.sort_and_write_out_block_to_disk())

    def __str__(self) -> str:
        return f'List of block {self.block_list}'
    
    def merge_blocks(self):
        '''
            Return a consolidated merged blocks using 2-way merge
        '''
        temp_stack_for_merging=list()
        while len(self.block_list) != 1:
            for _ in range(len(self.block_list)//2):
                first_block,second_block=Block.read_block_from_disk(self.block_list.pop()),Block.read_block_from_disk(self.block_list.pop())
                temp_stack_for_merging.append(first_block.merge(second_block))
            if self.block_list:
                temp_stack_for_merging.append(self.block_list.pop())
            self.block_list=temp_stack_for_merging
            temp_stack_for_merging=list()
        print(self.block_list)
        return Block.read_block_from_disk(self.block_list.pop())


