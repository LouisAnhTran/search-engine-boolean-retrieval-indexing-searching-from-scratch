#!/usr/bin/python3
import re
import nltk
import sys
import getopt

from Dictionary import Dictionary
from PostingList import PostingsList
from BooleanExpression import Boolean

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below
    dictionary=Dictionary(dict_file)
    dictionary.load_dictionary_from_file()
    postings_list=PostingsList(postings_file)
    with open(results_file,'w') as output_file:
        with open(queries_file,'r') as queries_file:
            lines=queries_file.readlines()
            for line in lines:
                # print('the current line => ',line)
                line=line.strip()
                boolean=Boolean(line)
                result=boolean.implement_boolean_retrieval(dictionary,postings_list)
                # output=line+" "+"=>"+" "+result+"\n"
                output=result+"\n"
                output_file.write(output)


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
