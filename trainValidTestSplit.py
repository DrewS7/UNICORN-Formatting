# From ChatGPT
import os
import shutil
import random


def move_files(source_dir, dest_dir1, dest_dir2, percentage1=20, percentage2=10):
    # Get list of files in source directory
    files = os.listdir(source_dir)
    num_files = len(files)

    # Calculate number of files to move to each destination directory
    num_files_dest1 = int(num_files * (percentage1 / 100))
    num_files_dest2 = int(num_files * (percentage2 / 100))

    # Randomly select files to move to each destination directory
    files_to_move_dest1 = random.sample(files, num_files_dest1)
    remaining_files = [file for file in files if file not in files_to_move_dest1]
    files_to_move_dest2 = random.sample(remaining_files, num_files_dest2)

    # Move files to destination directories
    for file_name in files_to_move_dest1:
        source_file = os.path.join(source_dir, file_name)
        dest_file = os.path.join(dest_dir1, file_name)
        shutil.move(source_file, dest_file)
        labelName = file_name.rstrip(".png") + ".txt"
        labelFile = "C:/Purdue/LeGrand/EOlabelsTrain/" + labelName
        labelDest = "C:/Purdue/LeGrand/EOlabelsValid/" + labelName
        # If there is a corresponding label for the image, move it to the same subset
        if os.path.isfile(labelFile):
            shutil.move(labelFile, labelDest)
        # print(f"Moved {file_name} to {dest_dir1}")

    for file_name in files_to_move_dest2:
        source_file = os.path.join(source_dir, file_name)
        dest_file = os.path.join(dest_dir2, file_name)
        shutil.move(source_file, dest_file)
        labelName = file_name.rstrip(".png") + ".txt"
        labelFile = "C:/Purdue/LeGrand/EOlabelsTrain/" + labelName
        labelDest = "C:/Purdue/LeGrand/EOlabelsTest/" + labelName
        if os.path.isfile(labelFile):
            shutil.move(labelFile, labelDest)
        # print(f"Moved {file_name} to {dest_dir2}")


if __name__ == "__main__":
    # This splits both images and labels
    source_directory = "C:/Purdue/LeGrand/EOimgsTrain/"
    destination_directory1 = "C:/Purdue/LeGrand/EOimgsValid/"
    destination_directory2 = "C:/Purdue/LeGrand/EOimgsTest/"

    move_files(source_directory, destination_directory1, destination_directory2)
