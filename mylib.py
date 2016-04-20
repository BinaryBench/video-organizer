import os
import sys
import itertools
import subprocess
import platform
import shutil


def format_folder_name(number, name):
    return format_number(number) + "-" + format_name(name)


def format_number(number):
    number = str(number)
    loop_times = 3 - len(number)
    for _ in itertools.repeat(None, loop_times):
        number = "0" + number
    return number


def format_name(name):
    return str(name).title()


def reformat(name):
    if os.path.isdir(name):
        # file_name = os.path.splitext(file)[0]
        split = name.split('-', 1)

        if len(split) > 1:
            try:
                number = int(split[0])
                new_dir = format_folder_name(number, split[1])

                # print(new_dir)

                return new_dir
            except ValueError:
                pass
    return None


def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def copyfiles(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)

    if not os.path.isdir(src):
        copyfile(src, os.path.join(dst, os.path.basename(src)))
        return

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        copyfile(s, d)
        '''
        if os.path.isdir(s):
            shutil.copytree(s, get_file_name(d), symlinks, ignore)
        else:
            copyfile(s, d)'''


def copyfile(src, dst):
    try:
        if os.path.isdir(dst):
            dst = os.path.join(dst, get_file_name(os.path.basename(src)))
        shutil.copyfile(src, get_file_name(dst))
    except PermissionError:
        print("unable to copy: " + src)


def movefiles(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    if not os.path.isdir(src):
        movefile(src, dst)
        return

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        movefile(s, d)

def movefile(src, dst):
    shutil.move(src, get_file_name(dst))

def get_file_name(file):
    if not os.path.exists(file):
        return file

    filename, file_extension = os.path.splitext(file)

    ii = 1
    while True:
        new_name = filename + "_" + str(ii) + file_extension
        if not os.path.exists(new_name):
            return new_name
        ii += 1


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
