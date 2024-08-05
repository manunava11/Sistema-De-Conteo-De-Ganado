import os

# Define the range of folder numbers to modify
start_number = 1
end_number = 142

# Define the common prefix of the folder names
prefix = "DJIMini3Pro_Campo4_Dia1_Mañana_Cow"

# Define the path to the directory containing the folders
directory_path = r"C:\Users\Manuel\Desktop\Carpeta Visual\Data_SantaIsa_Dia1_Manana"

# Loop over the range of folder numbers
for number in range(start_number, end_number + 1):
    # Use os.path.join to construct the full paths to the folders
    current_folder_name = os.path.join(directory_path, f"{prefix}{number}")
    new_folder_name = os.path.join(directory_path, f"_{prefix}{number}")
    
    # Debug message to show the current folder being checked
    print(f"Checking for folder: {current_folder_name}")
    
    # Check if the current folder exists
    if os.path.exists(current_folder_name):
        # Rename the folder
        os.rename(current_folder_name, new_folder_name)
        print(f"Renamed {current_folder_name} to {new_folder_name}")
    else:
        print(f"Folder {current_folder_name} does not exist")

print("Folder renaming completed.")
