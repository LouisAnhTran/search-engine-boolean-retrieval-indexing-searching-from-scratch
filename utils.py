import psutil

def get_memory_usage():
    # Get the memory usage in bytes
    memory_info = psutil.virtual_memory()

    # Convert bytes to megabytes for a more human-readable format
    memory_used_mb = memory_info.used / (1024 ** 2)
    memory_total_mb = memory_info.total / (1024 ** 2)

    return memory_used_mb/memory_total_mb

def get_list_of_indexes_parenthesis(input_string):
    return [i for i in range(len(input_string)) if input_string[i]=='(' or input_string[i]==')']
