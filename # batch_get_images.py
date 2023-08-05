# batch_get_images.py
# Python 3 script to download all images from a given URL and save them in a specified folder
# use: python batch_get_images.py http://url.where.images.are folder_path

import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import time
import sys

def make_soup(url):
    headers = {'User-Agent': 'Magic Browser'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_unique_filename(directory, filename, extension):
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename + extension)):
        new_filename = f"{filename}_{counter}"
        counter += 1
    return new_filename + extension

def sanitize_filename(filename):
    # Remove characters that are not allowed in file names
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_images(url, folder_path):
    try:
        soup = make_soup(url)
        images = soup.find_all('img')
        print(f"{len(images)} images found.")
        print(f'Downloading images to {folder_path}.')

        item_id = os.path.basename(url)  # Extract the item ID from the URL

        for image in images:
            src = image.get('src')
            if src and not src.startswith('data:image'):  # Skip inline data images
                filename = image.get('alt', image.get('title', 'image')).strip()
                if is_valid_filename(filename):
                    extension = os.path.splitext(os.path.basename(src))[1]
                    filename = f"{item_id}_{sanitize_filename(filename)}"  # Append the item ID to the filename
                    filename = get_unique_filename(folder_path, filename, extension)
                    print(f'Getting: {filename}')
                    response = requests.get(urljoin(url, src), stream=True)
                    response.raise_for_status()
                    # Delay to avoid corrupted previews (optional, remove if not needed)
                    time.sleep(1)
                    with open(os.path.join(folder_path, filename), 'wb') as out_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            out_file.write(chunk)

            style = image.get('style')
            if style and 'background-image' in style:
                bg_image_url = style.split('url(')[-1].split(')')[0]
                filename = os.path.splitext(os.path.basename(bg_image_url))[0]
                if is_valid_filename(filename):
                    extension = os.path.splitext(os.path.basename(bg_image_url))[1]
                    filename = f"{item_id}_{sanitize_filename(filename)}"  # Append the item ID to the filename
                    filename = get_unique_filename(folder_path, filename, extension)
                    print(f'Getting: {filename} (from background-image)')
                    response = requests.get(urljoin(url, bg_image_url), stream=True)
                    response.raise_for_status()
                    # Delay to avoid corrupted previews (optional, remove if not needed)
                    time.sleep(1)
                    with open(os.path.join(folder_path, filename), 'wb') as out_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            out_file.write(chunk)

    except requests.exceptions.RequestException as e:
        print('An error occurred:', e)
    except Exception as e:
        print('An error occurred:', e)
    else:
        print('Done.')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python batch_get_images.py <URL> <folder_path>')
        sys.exit(1)

    url = sys.argv[1]
    folder_path = sys.argv[2]
    get_images(url, folder_path)
