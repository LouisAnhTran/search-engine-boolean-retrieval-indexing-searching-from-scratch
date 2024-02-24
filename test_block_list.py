import pickle
# Opening the file again to demonstrate seek
with open('blocks.txt', 'rb') as file:
    # Seek to the initial position
    file.seek(0)

    # Unpickling and reading from the file
    loaded_dict = pickle.load(file)
    print('loaded file: ',loaded_dict)
