# batch_get_images.py

Python 3 script to download all images from a given URL and save them in a specified folder.

### Usage

```bash
python batch_get_images.py <URL> <folder_path>
```

### Description

This script allows you to download images from a webpage specified by the `<URL>` argument and save them in the `<folder_path>` directory on your local machine. It uses the Python `requests` library to fetch the webpage's HTML content and `BeautifulSoup` for parsing the HTML and extracting image URLs.

The script searches for `<img>` tags in the webpage and downloads images from their `src` attributes. It also checks for images set as background images in the inline CSS and downloads them as well.

### Functionality

- The script downloads all images found in the webpage, excluding inline data images.
- Filenames are generated based on the `alt` attribute of the `<img>` tag or the `title` attribute if the `alt` is missing. If both are unavailable, the filename is set to "image".
- Filenames are sanitized to remove characters not allowed in file names, ensuring compatibility with your operating system.
- Filenames are appended with an item ID extracted from the `<URL>` to avoid filename clashes.

### Dependencies

- Python 3
- `requests` library (install with `pip install requests`)
- `BeautifulSoup` library (install with `pip install beautifulsoup4`)

### Example Usage

```bash
python batch_get_images.py http://example.com/images folder_to_save_images
```

Note: If you encounter any issues, make sure you have the required libraries installed using `pip install requests beautifulsoup4`.

Please ensure you comply with the terms of service and copyright of the webpage from which you are downloading images. This script is intended for personal use or use with proper permissions from the website owners.
