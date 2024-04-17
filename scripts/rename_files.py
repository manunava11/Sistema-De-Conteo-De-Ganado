import os

def rename_files(directory_path):
    # Get the list of files in the directory
    #files = os.listdir(directory_path)

    # Sort the files
    #files.sort(key=lambda x: int(x.split()[1]))

    # Counter for numbering files
    count = 1

    # Iterate through the files and rename them
    for number in range(5, 135):
        # Construct the new file name with a numeric prefix
        #if number != 11:
        new_name = f"vid_el_talar_front_{number + 2}.mov"

            # Full paths for old and new names
        old_path = os.path.join(directory_path, f"Vaca {number}.mov")
        new_path = os.path.join(directory_path, new_name)

            # Rename the file
        os.rename(old_path, new_path)
        count += 1

if __name__ == "__main__":
    # Replace 'your_directory_path' with the path to your directory
    directory_path = "/Users/ramirososa/Desktop/Vacas final Campo Omar copy"

    # Call the function to rename files
    rename_files(directory_path)
