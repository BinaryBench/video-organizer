# from mylib import *
import os
import shutil
import glob
import platform
import subprocess
import sys
import argparse


def create_video_folder(name="Untitled", copy_globs=None, move_globs=None, popup=False, dir=os.getcwd()):

    count = 1
    for i in sorted(os.listdir(dir), reverse=True):
        if os.path.isdir(i):
            # file_name = os.path.splitext(file)[0]
            split = i.split('-', 1)

            if len(split) > 1:
                try:
                    count = int(split[0]) + 1
                    break
                except ValueError:
                    pass

    #name = input('Enter Name:')
    video_dir = format_folder_name(count, name)

    if not os.path.exists(video_dir):
        os.makedirs(video_dir)

    if copy_globs is not None:
        for copy_glob in copy_globs:
            for file in glob.glob(copy_glob):
                shutil.copy(file, video_dir)

    if move_globs is not None:
        for move_glob in move_globs:
            for file in glob.glob(move_glob):
                shutil.move(file, video_dir)

    if popup:
        open_folder(video_dir)


def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def format_folder_name(number, name):
    return format_number(number) + "-" + format_name(name)


def format_number(number):
    return str(number).zfill(3)


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

if __name__ == '__main__':
    ask = 'ask'
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", help='video name')
    parser.add_argument('-c', "--copy_globs", help='blobs to copy into the video folder')
    parser.add_argument('-m', "--move_globs", help='blobs to move into the video folder')
    parser.add_argument('-p', "--popup", help='Whether or not to open the folder when complete')
    parser.add_argument('-d', "--dir", help='The directory to create the video folder')
    args = parser.parse_args()

    data = {}

    if args.name is not None:
        if args.name == ask:
            args.name = input("Enter name:")
        data['name'] = args.name

    if args.copy_globs is not None:
        if args.copy_globs == ask:
            args.copy_globs = input("Enter copy globs:")
        data['copy_globs'] = args.copy_globs.split(',')

    if args.move_globs is not None:
        if args.move_globs == ask:
            args.move_globs = input("Enter move globs:")
        data['move_globs'] = args.move_globs.split(',')

    if args.popup is not None:
        if args.popup == ask:
            args.popup = input('Popup? [y/n]:')
        data['popup'] = args.popup.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']

    if args.dir is not None:
        if args.dir == ask:
            args.dir = input("Enter dir:")
        data['dir'] = args.dir

    create_video_folder(**data)
