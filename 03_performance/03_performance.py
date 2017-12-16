# write the most effective code for a generation md5 of 100 binary files
# A size of every file more than 4TBytes

import os
from hashlib import md5
from multiprocessing import Pool

# MD5 has 128-byte digest blocks
BLOCK_SIZE = 128 * 512
FILES_DIR = 'large_files'

def get_file_md5(path):
    hasher = md5()
    with open(path, 'rb') as large_file:
        while True:
            data = large_file.read(BLOCK_SIZE)
            if not data:
                break
            hasher.update(data)

    print('{}: {}'.format(path, hasher.hexdigest()))


if __name__ == "__main__":
    files_found = []
    for root, dirs, files in os.walk(FILES_DIR):
        for file_name in files:
            files_found.append(os.path.join(FILES_DIR, file_name))

    p=Pool()
    p.map(get_file_md5, files_found)
    p.close()
