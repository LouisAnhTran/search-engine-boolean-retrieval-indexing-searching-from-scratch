import pickle

# Example data
my_dict_1 = {'name': 'John', 'age': 30, 'city': 'New York'}
my_dict_2 = {'name': 'nana', 'age': 26, 'city': 'New York'}
nana=[]
# Pickling and writing to a file
with open('example.txt', 'wb') as file:
    # Get the initial position of the cursor
    initial_position = file.tell()
    nana.append(initial_position)
    # Pickle and write the object to the file
    pickle.dump(my_dict_1, file)

    # Get the final position of the cursor
    initial_position = file.tell()
    nana.append(initial_position)
    
    pickle.dump(my_dict_2, file)


# Display the initial and final positions


# Opening the file again to demonstrate seek
with open('example.txt', 'rb') as file:
    # Seek to the initial position
    file.seek(nana[0])

    # Unpickling and reading from the file
    loaded_dict = pickle.load(file)
    print('loaded file: ',loaded_dict)

    file.seek(nana[1])
    loaded_dict = pickle.load(file)
    print('loaded file: ',loaded_dict)

# Display the loaded dictionary

# Output: {'name': 'John', 'age': 30, 'city': 'New York'}


# Opening the file again to demonstrate seek
with open('dictionary.txt', 'rb') as file:
    # Seek to the initial position

    # Unpickling and reading from the file
    loaded_dict = pickle.load(file)
    print('dictionary file: ',loaded_dict)

with open('postings.txt', 'rb') as file:
    # Seek to the initial position
    file.seek(2889)

    # Unpickling and reading from the file
    loaded_dict = pickle.load(file)
    print('loaded list: ',loaded_dict)


