import os
import main

sourceFile = open('log.txt', 'w', 'utf8')
my_dir = 'D:\\PICTURES'

for filename in main.iterate_sub_dir(my_dir):
    index=0
    if '(' and ')' in filename:
        os.remove(os.path.join(my_dir, filename))
        print('File %s removed!' % os.path.basename(filename), file=sourceFile)
        print('File %s HAS special symbols!' % os.path.basename(filename), file=sourceFile)
        print('-' * 30)
    else:
        print('File %s HAS NOT special symbols!' % os.path.basename(filename), file=sourceFile)
        print('-' * 30)
sourceFile.close()
