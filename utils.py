import shutil
from datetime import datetime
import fnmatch
import os

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H%M%S")


def get_time_now_to_str():
    datetimeobj = datetime.now()
    timetostr = datetimeobj.strftime('%Y%m%d_%H%M%S')
    return timetostr


def unique(path):
    base, extn = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = base + " (" + str(counter) + ")" + extn
        counter += 1
    return path


def iterate_sub_dir(path):
    index = 0
    for root, subdirectories, files in os.walk(path):
        for item in fnmatch.filter(files, "*"):
            item_path = os.path.join(root, item)
            index += 1
            print('File No.%s : %s' % (index, item))
            print('PATH: %s' % item_path)
            yield item_path


def if_exist_add_index(f_name, ori_dir, dest_dir):
    if not os.path.exists(os.path.join(dest_dir, f_name)):
        shutil.move(os.path.join(ori_dir, f_name), dest_dir)
    else:
        n_name = os.path.basename(unique(os.path.join(dest_dir, f_name)))
        os.rename(f_name, n_name)
        shutil.move(os.path.join(ori_dir, n_name), dest_dir)


def check_file_ext(f_path, l_support):
    ext = os.path.splitext(f_path)[1]
    if not ext.lower() in l_support:
        return False
        print('FALSE')
    else:
        return True
        print('TRUE')
