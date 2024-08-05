import os
import shutil
import logging
from huggingface_hub import hf_hub_download, login

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token and model name
token = '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'
model_name = 'Proyecto-Sistema-de-Conteo-de-Ganado/CattleDetectionModel_YOLOv8x_v1.0'

# Ensure the model folder exists
model_folder = '/app/model'
os.makedirs(model_folder, exist_ok=True)
logger.info(f'Created model folder: {model_folder}')

# Define the destination file path in the model folder
destination_file_path = os.path.join(model_folder, 'cattle_v8x.pt')

# Check if the model file already exists
if os.path.isfile(destination_file_path):
    logger.info(f'Model file already exists: {destination_file_path}')
else:
    # Login to Hugging Face
    login(token=token)
    logger.info('Logged in to Hugging Face')

    # Download the model file to a temporary location
    temp_file_path = hf_hub_download(repo_id=model_name, filename='cattle_v8x.pt')
    logger.info(f'Downloaded model to temporary path: {temp_file_path}')

    # Copy the file to the model folder
    shutil.copy2(temp_file_path, destination_file_path)
    logger.info(f'Copied model file to: {destination_file_path}')

    # Change the permissions of the destination file
    os.chmod(destination_file_path, 0o777)
    logger.info(f'Changed permissions for: {destination_file_path}')

    # Optionally remove the temporary file
    os.remove(temp_file_path)
    logger.info(f'Removed temporary file: {temp_file_path}')