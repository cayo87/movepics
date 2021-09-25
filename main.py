import exifread
import os
import time
import shutil
import fnmatch

my_dir = 'E:\\OneDrive\\Apps\\Google'
dest_dir = 'D:\\PICTURES'
matches = ['.jpg', '.jpeg', '.mp4', '.mov', '.arw', '.heic', '.avi', '.3gp', ',nef', '.png', '.cr2']
logFile = open('log_main.txt', 'w', 'utf8')


# Iterate all files in a directory


def iterate_dir(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


# Iterate all files in a directory and subdirectories
def iterate_sub_dir(path):
    index = 0
    for root, subdirectories, files in os.walk(path):
        for item in fnmatch.filter(files, "*"):
            item_path = os.path.join(root, item)
            index += 1
            print('File No.%s : %s' % (index, item_path), file=logFile)
            yield item_path


def unique(path):
    base, extn = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = base + " (" + str(counter) + ")" + extn
        counter += 1
    return path


def if_exist_add_index(f_name, ori_dir, dest_dir):
    if not os.path.exists(os.path.join(dest_dir, f_name)):
        # os.rename(f_name)
        shutil.move(os.path.join(ori_dir, f_name), dest_dir)
    else:
        n_name = os.path.basename(unique(os.path.join(dest_dir, f_name)))
        # n_name=os.path.basename
        os.rename(f_name, n_name)
        shutil.move(os.path.join(ori_dir, n_name), dest_dir)


for filename in iterate_sub_dir(my_dir):
    with open(os.path.join(my_dir, filename), 'rb') as f:
        try:
            extension = os.path.splitext(filename)[1]
            # Check if destination directory not exist -> create
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            # Check if file extension not supported -> skipped
            if not extension.lower() in matches:
                print(filename + ' has unsupported extension %s -> skipped' % extension, file=logFile, file=logFile)
                continue
            # If file extension is supported -> proceed
            else:
                # Read EXIF information of the file
                exif = exifread.process_file(f)
                f.close()
                # Check if EXIF does not have EXIF DateTimeOriginal property -> skipped, move to Unclassified folder
                if 'EXIF DateTimeOriginal' not in str(exif):
                    print('This file DOESN\'T has tags DateTimeOriginal -> moved to Unclassified folder', file=logFile)
                    if not os.path.exists(os.path.join(dest_dir, 'Unclassified')):
                        # Check if Unclassified folder not exist -> create
                        os.mkdir(os.path.join(dest_dir, 'Unclassified'))
                        # Move the none DateTimeOriginal file to Unclassified folder
                        shutil.move(os.path.join(my_dir, filename), os.path.join(dest_dir, 'Unclassified'))
                    else:
                        # Move the none DateTimeOriginal file to Unclassified folder if folder Unclassified was created
                        # shutil.move(filename, os.path.join(dest_dir, 'Unclassified'))
                        if_exist_add_index(filename, os.path(my_dir), os.path.join(dest_dir, 'Unclassified'))
                        print('This file EXIST in destination folder but it was indexed', file=logFile)
                    continue
                # Check if EXIF has EXIF DateTimeOriginal property -> proceed
                print('%s has tags DateTimeOriginal' % filename, file=logFile)
                # Get EXIF DateTimeOriginal value
                exif_date = exif['EXIF DateTimeOriginal']
                # Convert into a time object
                str_date = time.strptime(str(exif_date), '%Y:%m:%d %H:%M:%S')
                # Create a new name with format of DateTimeOriginal as YYYYMMDD_HHMMSS.extension
                new_name = str(str_date.tm_year) + str(f"{str_date.tm_mon:02d}") + str(
                    f"{str_date.tm_mday:02d}") + '_' + str(f"{str_date.tm_hour:02d}") + str(
                    f"{str_date.tm_min:02d}") + str(
                    f"{str_date.tm_sec:02d}") + extension
                # Create path to store new name files
                PATH = os.path.join(dest_dir, str(str_date.tm_year))
                PATH_FULL = os.path.join(PATH, str(f"{str_date.tm_mon:02d}"))
                # Check if paths are not exist -> create
                if not os.path.exists(PATH):
                    os.mkdir(PATH)
                    print('Made new dir YEAR %s successful' % PATH, file=logFile)
                elif not os.path.exists(PATH_FULL):
                    os.mkdir(PATH_FULL)
                    print('Made new dir MONTH %s successful' % PATH_FULL, file=logFile)
                else:
                    # If paths are created -> proceed
                    print(PATH_FULL + ' is OK', file=logFile)
                    # Rename the file to new name
                    os.rename(os.path.join(my_dir, filename), os.path.join(my_dir, new_name))
                    print('File %s changed name to %s ' % (filename, new_name), file=logFile)
                    # Check if new name is not exist in destination folder -> move
                    if not os.path.exists(os.path.join(PATH_FULL, new_name)):
                        print('File %s NOT EXIST in %s ' % (new_name, PATH_FULL), file=logFile)
                        shutil.move(os.path.join(my_dir, new_name), PATH_FULL)
                        print('Moved %s to %s successful' % (new_name, PATH_FULL), file=logFile)
                    else:
                        # If new name is exist in destination folder -> add index in new name
                        print('File %s is EXIST in %s' % (new_name, PATH_FULL), file=logFile)
                        new_name_tmp = unique(os.path.join(PATH_FULL, new_name))
                        new_name_index = os.path.basename(new_name_tmp)
                        print('Added index for %s to %s : ' % (new_name, new_name_index), file=logFile)
                        # Rename new file with index
                        os.rename(os.path.join(my_dir, new_name), os.path.join(my_dir, new_name_index))
                        # Move new file with index to destination folder
                        shutil.move(os.path.join(my_dir, new_name_index), PATH_FULL)
                        print('Moved %s to %s successful' % (new_name_index, PATH_FULL), file=logFile)
                    print('=' * 50, file=logFile)
        except Exception as e:
            print('EXCEPTION!!!', file=logFile)
            print(e, file=logFile)
logFile.close()
