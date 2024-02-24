import pickle
from PostingList import PostingsList
from BooleanExpression import Boolean

with open('dictionary.txt','rb') as file:
    file.seek(0)
    loaded_file=pickle.load(file)
    print(loaded_file)
    print('number of terms: ',len(loaded_file['indexing'].keys()))

print("test posting list")
with open('postings.txt','rb') as file:
    # 52001 => said
    # 1083 => ,
    file.seek(1083)
    loaded_file_1=pickle.load(file)
    print(", posting list ",PostingsList.convert_linked_list_to_posting_list(loaded_file_1))
    file.seek(52001)
    loaded_file_2=pickle.load(file)
    print("said posting list ",PostingsList.convert_linked_list_to_posting_list(loaded_file_2))
    # loaded_file=pickle.load(file)
    # print('posting list: ',loaded_file)
    # print('test skip pointer ',loaded_file.skip_pointer.has_skip_pointer())
    # print('posting list: ',PostingsList.convert_linked_list_to_posting_list(loaded_file))
    test_boolean=Boolean('nana')
    print('test OR ',PostingsList.convert_linked_list_to_posting_list(test_boolean.OR_operator(loaded_file_1,loaded_file_2)))

    file.seek(63903)
    loaded_file_3=pickle.load(file)
    print('print all docs id ',loaded_file_3)
    print('test NOT ',PostingsList.convert_linked_list_to_posting_list(test_boolean.NOT_operator(loaded_file_1,loaded_file_3)))
