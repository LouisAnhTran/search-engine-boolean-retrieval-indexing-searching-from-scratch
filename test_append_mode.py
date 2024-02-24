import pickle
my_dict_1 = {'name': 'John', 'age': 30, 'city': 'New York'}
my_dict_2 = {'name': 'nana', 'age': 26, 'city': 'New York'}
nana=[]  

# Pickling and writing to a file
with open('example.txt', 'ab') as file:
    # Get the initial position of the cursor
    position = file.tell()
    nana.append(position)
    # Pickle and write the object to the file
    pickle.dump(my_dict_1, file)

# Pickling and writing to a file
with open('example.txt', 'ab') as file:
    # Get the final position of the cursor
    position = file.tell()
    nana.append(position)
    pickle.dump(my_dict_2, file)

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