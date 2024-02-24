

# [0, 3718, 4434, 5362]


from SinglePassInMemoryIndexing import SPIMI

spimi=SPIMI()

spimi.block_list=[0, 48, 3357, 5202]

obj=spimi.merge_blocks()

print(obj)

print('len of terms ',len(obj.sorted_terms))

