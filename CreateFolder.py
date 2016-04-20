from mylib import *


def create_video_file(copy_folders=None, move_folders=None, popup=True, source_dir=os.getcwd()):
    count = 1

    for i in sorted(os.listdir(source_dir), reverse=True):
        if os.path.isdir(i):
            # file_name = os.path.splitext(file)[0]

            split = i.split('-', 1)

            if len(split) > 1:
                try:
                    count = int(split[0]) + 1
                    break
                except ValueError:
                    pass

    name = input('Enter Name:')
    folder_name = format_folder_name(count, name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if copy_folders is not None:
        for copy_folder in copy_folders:
            copyfiles(copy_folder, folder_name)

    if move_folders is not None:
        for move_folder in move_folders:
            movefiles(move_folder, folder_name)
    if popup:
        open_folder(folder_name)


def main():
    create_video_file()

