import os
import random

MULTI_PASS_COUNT = 3  # Fixed number of passes

def wipe_file(file_path):
    """Overwrite a file MULTI_PASS_COUNT times and then delete it."""
    if not os.path.isfile(file_path):
        return False
    
    length = os.path.getsize(file_path)
    try:
        with open(file_path, "r+b") as f:
            for _ in range(MULTI_PASS_COUNT):
                f.seek(0)
                f.write(os.urandom(length))  # overwrite with random bytes
                f.flush()
                os.fsync(f.fileno())
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error wiping {file_path}: {e}")
        return False

def wipe_files(path):
    """Recursively wipe files/folders with MULTI_PASS_COUNT passes."""
    if os.path.isfile(path):
        wipe_file(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                wipe_file(os.path.join(root, file))
