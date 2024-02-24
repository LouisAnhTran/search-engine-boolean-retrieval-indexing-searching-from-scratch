import pickle

class Dictionary:
    def __init__(self,dict_file):
        self.dict_file=dict_file
        self.dictionary={'indexing':dict()}

    def insert_term_to_dictionary(self,term,doc_freq,offset):
        self.dictionary['indexing'][term]=(doc_freq,offset)

    def add_docids_to_dictionary(self,docids,offset):
        self.dictionary['docids']=(len(docids),offset)

    def save_dictionary_to_file(self):
        with open(self.dict_file,'wb') as file:
            pickle.dump(self.dictionary,file)
        file.close()

    def load_dictionary_from_file(self):
        with open(self.dict_file,'rb') as file:
            self.dictionary=pickle.load(file)
    
    def return_offset_based_on_term(self,term):
        return self.dictionary['indexing'][term][1] if term in self.dictionary['indexing'] else None
    
    def return_offset_for_all_docids(self):
        return self.dictionary['docids'][1]
    