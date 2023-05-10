import os
import wget
from bs4 import BeautifulSoup
import requests
import zipfile
import subprocess

url = 'https://unofficialpi.org/Distros/OctoPi/'
ext = 'zip'

def listFD(url, ext=''):
    page = requests.get(url).text
    #print (page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

# URL of the remote directory containing the zip file
directory_url = "https://unofficialpi.org/Distros/OctoPi/"

# Specific name that the zip file starts with
prefix = "octopi-bullseye-arm64-"

# Download directory where the zip file will be saved
download_dir = "./"

# Retrieve the list of files in the remote directory
file_list = listFD(url, ext)
print ("file list of url is : ", file_list)

# Filter the file list to find the zip file starting with the specific name
matching_files = [filename for filename in file_list if prefix in filename and filename.endswith(".zip")]

print (matching_files)
if matching_files:
    # Get the first matching file
    zip_file_url = matching_files[0]

    print ("zip_file_url = ", zip_file_url)

    zip_name = zip_file_url.rsplit('/', 1)[-1]
    print ("zip_name = ", zip_name)
    # Download the zip file to the download directory
    #wget.download(zip_file_url, os.path.join(download_dir, zip_name))

    # Print the downloaded file path
    print("\nDownloaded:", os.path.join(download_dir, zip_name))

    extract_folder = './workspace'  # Folder where the file will be extracted
    new_file_name = 'input.img'  # New name for the extracted file

    # Extract the contents of the zip file
    with zipfile.ZipFile(os.path.join(download_dir, zip_name), 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Rename the extracted file
    img_names = [s for s in os.listdir(extract_folder) if s.endswith('.img')]
    if not img_names:
        print ("no images found!!!")
        exit(1)

    extracted_file_path = os.path.join(extract_folder, img_names[0])
    print ("extracted_file_path", extracted_file_path)
    new_file_path = os.path.join(extract_folder, new_file_name)
    print ("new file path = ", new_file_path)
    os.rename(extracted_file_path, new_file_path)

    print("File extracted and renamed successfully.")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(script_directory)
    docker_command = f"docker run --rm --privileged -v {script_directory}/workspace:/CustoPiZer/workspace ghcr.io/octoprint/custopizer:latest"
    print("docker cmd = ", docker_command)
    # Run the Docker command
    subprocess.run(docker_command, shell=True)

else:
    print("No matching zip file found.")

