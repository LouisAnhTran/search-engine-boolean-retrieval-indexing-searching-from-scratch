This is the README file for A0290532J's submission
Email(s): e1325138@u.nus.edu

== Python Version ==

I'm using Python Version <3.10.7> for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

This assignment can be separated into two main phases, namely indexing and searching. I will go over each phase in great detail, explaining the different types of data structures used, as well as algorithms for various operations.


I. INDEXING:

1. Tokenization, Stemming, Stop Word Removals and constructing blocks:
    - Retrieve all docids from the input directory.
    - Initialize an empty hashtable.
    - Instantiate an SPIMI object from the SPIMI class.
    - Iterate through each docid, and open the corresponding document. For each document, perform the following steps:
        + Obtain the list of tokens using `sent_tokenize` and `word_tokenize` provided by NLTK.
        + Retrieve the list of stop words from NLTK.
        + Create a new list of tokens using list comprehension and applying these conditions: a token must not be in the stop word list, apply stemming, and case-folding to reduce the token to its lower case form.
        + Once a list of tokens is obtained in accordance with the requirements, iterate through each token. For each token, perform the following steps:
            - If the memory usage is within the expected range, update the hashtable with the term, docid pair.
            - If the memory usage exceeds our predefined limit, create sorted terms from the hashtable, instantiate the block with sorted terms and hashtable, write out the block to the hard disk, and add the block address to the SPIMI block list.
            - Clear the hashtable and delete the block instance to free up memory.

2. SinglePassInMemoryIndexing: This program utilizes Single-pass in-memory indexing to accelerate sorting and efficiently manage space complexity.

   - As we iterate through all documents and generate term, docid pairs, when the memory usage exceeds our predefined limit, we generate a block storing sorted terms and a hashtable (dictionary) following the lecture algorithm and write out the block to the hard disk.
   - Each block object has two variables, namely hashtable and sorted_terms.
   - After scanning through all documents, the SPIMI object has a block list variable, an array containing the addresses of all blocks on the hard disk.
   - Implement a 2-way block merging algorithm for merging all blocks:
       - Initialize the stack to store all intermediary merged blocks.
       - While the block list length is not 1:
       - Calculate n, the number of merging times, as the nearest whole number obtained by dividing the length of the block list by 2.
       - Repeat the following steps for n times:
           + Pop two blocks from the block list.
           + Perform merging for the two blocks.
           + Push the merged block to the stack.
       - If the block list is not empty, pop the block list and push the item to the stack.
   - After the while loop terminates, the block list contains only 1 item, the location of the final consolidated merged block on the hard disk.

3. Writing out Dictionary and Posting Lists to Hard Disk:
    - Instantiate a dictionary object from the Dictionary class.
    - Instantiate a posting list object from the PostingList class.
    - At this stage, we have constructed the single merged block with sorted terms and hashtable, and it is stored on the hard disk. 
    Notice: The dictionary to be loaded into memory for searching will look like:
    `{'docid': (number_of_docs, offset), 'index': {term: (document_frequency, offset)}}`, where the offset is the pointer to the corresponding posting list on the hard disk.
    - Iterate through the sorted terms. For each term:
        + Get the current pointer on the hard disk.
        + Retrieve the posting list from the hashtable.
        + Convert the posting list to a linked list with skip pointers.
        + Add the term to the dictionary as the key, with values being a tuple containing document frequency and a pointer to the posting list.
        + Write out the linked list with skip pointers to the hard disk.
    - Also, write out all docids to the hard disk and add the pointer to the dictionary.
    - At this point, we have successfully constructed the dictionary, with each term having a pointer to its respective posting list on the hard disk. Then, write out the dictionary to the hard disk to complete the indexing phase.

4. Convert the Posting List to Linked List and Implement Skip Pointers:
   For each posting list, we follow these steps:
   + Calculate the space to skip using the formula: sqrt(len(posting_list))
   + Initialize the head node with the node value being the first element of the posting list.
   + Initialize a variable `node` and set it to point to the head.
   + Initialize a variable `temp_node` and set it to point to `node`.
   + Scan through the posting list, starting from index 1:
        - Create a new node based on the item at index i, connect this node to the linked list by updating the current node's next pointer; the current node's next pointer will point to the newly created node.
        - Set `node` to `node.next`, meaning we shift our pointer or reference to the next node in the linked list.
        - Check if i%space_to_skip == 0:
            + Set `temp_node`'s skip pointer to point to `node`.
            + Then set `temp_node` equal to `node`, meaning `temp_node` now points to the current node.
    + After we finish scanning through the entire posting list, all we have to do is return the head node.

II. SEARCHING:
1. Parsing boolean query and performing Boolean retrieval using stacks:
+ Read the dictionary into memory from the hard disk.
+ Read the file containing all the queries. For each query, implement the following steps:
    - Implement tokenization for the query with stemming and case-folding.
    - Parse the boolean query using the Shunting Yard algorithm to obtain the list of operands and operators. Let's denote this list as the expression list.
    - Implement the boolean retrieval after the parsing step:
        + Initialize a stack.
        + While the expression list is not empty:
            - Pop the item at index 0 of the list.
            - If the item is an operand, based on the item, read the linked list from the hard disk using the dictionary and push it onto the stack.
            - If the item is an operator:
                + First case: Operator = AND:
                    - Pop two linked lists from the top of the stack.
                    - Implement logic for the AND operator to obtain the result, add pointers to the result, and push it onto the stack.
                + Second case: Operator = OR:
                    - Pop two linked lists from the top of the stack.
                    - Implement logic for the OR operator to obtain the result, add pointers to the result, and push it onto the stack.
                + Third case: Operator = NOT:
                    - Pop only one linked list from the top of the stack.
                    - Implement logic for the NOT operator to obtain the result, add pointers to the result, and push it onto the stack.
        + When the while loop terminates, it means the expression list is empty, guaranteeing that we have performed the necessary operations for the given operands and operators. Simultaneously, the stack contains only one item left, and this is our final result for this boolean query.

2. Implement Skip Pointer Algorithm for AND Operator:
   + We carefullly followed the algorithm described in the lecture.
   + The only difference is that the result linked list initially has no pointers. Therefore, additional steps were taken to add the pointers accordingly before pushing it onto the stack.

3. Notice for NOT Operator:
   + The NOT operator requires all docids of our collection.
   + Hence, we need to read the list of docids into memory from the hard disk using the offset stored in the memory dictionary.
   + To facilitate the NOT operator implementation, we convert the linked list to a posting list. Then, based on the term posting list and the list of all docids, we simply use list comprehension to obtain the docids that appear only in the all docids list but not in the term posting list.
   + After that, we convert the posting list to a linked list and add the skip pointers accordingly.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

In order to implement Indexing and Searching tasks, I have created a couple of files for storing intermediarty data.

blocks.txt: This file stores all the blocks on the hard disk before merging.
index.py: Contains logic to carry out the indexing task.
search.py: Contains logic to perform searching for Boolean retrieval.
SinglePassInMemoryIndexing.py: A class defined to manage all blocks and perform block merging algorithms.
Stack.py: A class defined for the stack data structure. (This assignment extensively uses stacks for various algorithms, such as block merging, parsing Boolean queries, etc.)
utils.py: Contains helper functions defined for repetitive tasks.
Linkedlist.py: This file contains the definition of the modified linked list data structure with the introduction of new variables and functions. Linked lists were used to implement posting list traversal with skip pointers.
config.py: Stores variables and constants controlling the behavior of the program.
Block.py: A class defined to seamlessly manage blocks.
BooleanExpression.py: A class defined to manage Boolean queries and implement Boolean operations, such as Boolean queries tokenization, Shunting-yard algorithm for parsing Boolean queries, AND, OR, NOT operator implementation, etc.
dictionary.txt: A file to store the dictionary on the hard disk.
postings.txt: A file to store posting lists on the hard disk.
Dictionary.py: A class defined to manage dictionary operations, storage, writing out to the hard disk, loading from the hard disk to memory for searching.
PostingList.py: A class defined to manage PostingList objects in a standardized and organized manner for operations such as writing out posting lists to the hard disk, reading in a posting list for a specific term from the hard disk to memory for searching.
README.txt: Provides additional information about the assignment, such as algorithm and steps elaboration, files submitted, student declaration, references, etc.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0290532J, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[x] I/We, A0290532J, did not follow the class rules regarding homework
assignment, because of the following reason:

I adhered strictly to the course policy, assignment guidelines, and class rules in order to complete this assignment.

We suggest that we should be graded as follows:

My assignment should be graded based on:

Code correctness, readability, and scalability
Adherence to submission instructions and guidelines
Accurate application and implementation of concepts and algorithms covered in lectures.

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Learning pickle: 
1. https://docs.python.org/3.7/library/pickle.html
Shunting yard algorithm for parse boolean queries: 
1. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
2. https://brilliant.org/wiki/shunting-yard-algorithm/

