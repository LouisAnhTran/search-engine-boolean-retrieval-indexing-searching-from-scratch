import psutil

def get_memory_usage():
    # Get the memory usage in bytes
    memory_info = psutil.virtual_memory()

    # Convert bytes to megabytes for a more human-readable format
    memory_used_mb = memory_info.used / (1024 ** 2)
    memory_total_mb = memory_info.total / (1024 ** 2)

    print(f"Used Memory: {memory_used_mb:.2f} MB")
    print(f"Total Memory: {memory_total_mb:.2f} MB")
    print(f'Usage percentage: {memory_used_mb/memory_total_mb} %')

if __name__ == "__main__":
    get_memory_usage()