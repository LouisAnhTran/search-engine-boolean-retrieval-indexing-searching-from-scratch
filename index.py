#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
import gc

import config
from Dictionary import Dictionary
from PostingList import PostingsList
import utils
from Block import Block
from SinglePassInMemoryIndexing import SPIMI 

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    list_of_files=sorted(list(map(lambda x: int(x),os.listdir(in_dir)[:len(os.listdir(in_dir)) if not config.TESTING else config.TESTING_SIZE])))

    # print(list_of_files)

    # return 

    hashtable=dict()
    spimi=SPIMI()
    list_of_docids=list()

    for docid in list_of_files:
        list_of_docids.append(docid)
        with open(f'{in_dir}\{str(docid)}',"r") as file:
            print('I am reading docit',docid)
            content=file.read()
            tokens=[token for sent in nltk.sent_tokenize(content) for token in nltk.word_tokenize(sent)]
            # print('tokens list before stemming and case-folding',tokens)

            stop_words=set(stopwords.words('english'))

            tokens_with_no_stop_words=[token for token in tokens if token.lower() not in stop_words]
            stemmer = PorterStemmer()
            stemmed_and_case_folded_tokens=[stemmer.stem(token).lower() for token in tokens_with_no_stop_words]

            for token in stemmed_and_case_folded_tokens:
                if utils.get_memory_usage() <= config.MEMORY_LIMIT:
                    print("MEMORY USAGE ",utils.get_memory_usage())
                    if token not in hashtable:
                        hashtable[token]=[docid]
                    elif docid not in hashtable[token]:
                        hashtable[token].append(docid)
                else:
                    print("MEMORY SHOOT UP ",utils.get_memory_usage())
                    block=Block(sorted(list(hashtable.keys())),{term:sorted(posting_list) for term,posting_list in hashtable.items()})
                    spimi.add_block(block)
                    del block
                    hashtable={}
                    config.MEMORY_LIMIT+=config.MEMORY_TOLERANCE

            
    if hashtable:
        block=Block(sorted(list(hashtable.keys())),{term:sorted(posting_list) for term,posting_list in hashtable.items()})
        spimi.add_block(block)
        del block
        del hashtable

    print(spimi)

    consolidated_block=spimi.merge_blocks()

    # save dictionary and posting to disks 
    dictionary_object=Dictionary(out_dict)
    posting_object=PostingsList(out_postings)
    posting_object.save_posting_to_disk(consolidated_block,dictionary_object)
    posting_object.save_docids_to_disk(dictionary_object,list_of_docids)
    dictionary_object.save_dictionary_to_file()

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
