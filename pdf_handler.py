import fitz
import os
from dotenv import load_dotenv

load_dotenv()

WORKING_PATH = os.environ.get('WORKING_PATH')
IMAGE_STORAGE = 'static/image_buffer'


def extract_from_local(address):
    output_folder = WORKING_PATH + IMAGE_STORAGE
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    os.chdir(output_folder)
    num_pages = 0
    with fitz.open(WORKING_PATH + r'presentations_buffer\\' + address) as pdf:
        num_pages = pdf.page_count

        for num in range(num_pages):
            page = pdf.load_page(num)
            pix = page.get_pixmap()
            output_image_path = os.path.join(
                output_folder, f"page_{num + 1}.png")

            # Save the image
            pix.save(output_image_path)
    return num_pages


def clean_local():
    directory = WORKING_PATH + IMAGE_STORAGE
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
        else:
            print(f"Skipped {file_path} (not a file)")


if __name__ == "__main__":
    address = 'analisis.pdf'
    print(WORKING_PATH + r'presentations_buffer\\' + address)
    extract_from_local(address)
    clean_local()
